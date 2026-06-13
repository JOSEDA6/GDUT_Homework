#include "command_execution.h"

int execute_external_command(char **argv, int redirect_fd, int pipeFlag) {
    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        return -1;
    }

    if (pid == 0) {
        if (redirect_fd!= -1) {
            dup2(redirect_fd, STDOUT_FILENO);
            close(redirect_fd);
        }
        if (execvp(argv[0], argv) < 0) {
            perror("execvp");
            log_error(argv[0], strerror(errno));
            exit(1);
        }
    }

    if (!pipeFlag) {
        wait(NULL);
    }

    return 0;
}

char *get_command_path(char *command) {
    char *path_env = getenv("PATH");
    char *token = strtok(path_env, ":");
    static char full_path[PATH_MAX];

    while (token!= NULL) {
        snprintf(full_path, sizeof(full_path), "%s/%s", token, command);
        if (access(full_path, X_OK) == 0) {
            return full_path;
        }
        token = strtok(NULL, ":");
    }
    return NULL;
}

void execute_pipeline(char *cmd1, char *cmd2) {
    int pipe_fds[2];
    pid_t pid1, pid2;

    if (pipe(pipe_fds) == -1) {
        perror("pipe");
        return;
    }

    if ((pid1 = fork()) == 0) {
        dup2(pipe_fds[1], STDOUT_FILENO);
        close(pipe_fds[0]);
        close(pipe_fds[1]);
        char *argv1[MAXLINE / 2];
        char *token = strtok(cmd1, " ");
        int i = 0;
        while (token!= NULL) {
            argv1[i++] = token;
            token = strtok(NULL, " ");
        }
        argv1[i] = NULL;
        execvp(argv1[0], argv1);
        perror("execvp");
        log_error(cmd1, strerror(errno));
        exit(1);
    }

    if ((pid2 = fork()) == 0) {
        dup2(pipe_fds[0], STDIN_FILENO);
        close(pipe_fds[1]);
        close(pipe_fds[0]);
        char *argv2[MAXLINE / 2];
        char *token = strtok(cmd2, " ");
        int i = 0;
        while (token!= NULL) {
            argv2[i++] = token;
            token = strtok(NULL, " ");
        }
        argv2[i] = NULL;
        execvp(argv2[0], argv2);
        perror("execvp");
        log_error(cmd2, strerror(errno));
        exit(1);
    }

    close(pipe_fds[0]);
    close(pipe_fds[1]);
    wait(NULL);
    wait(NULL);
}