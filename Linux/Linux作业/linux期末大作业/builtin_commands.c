#include "builtin_commands.h"

void handleCd(const char *arg, char *currentPath) {
    if (arg == NULL || strcmp(arg, "") == 0) {
        char *homeDir = getenv("HOME");
        if (homeDir!= NULL) {
            strcpy(currentPath, homeDir);
        }
    } else {
        if (chdir(arg) == 0) {
            getcwd(currentPath, PATH_MAX);
        } else {
            printf("Directory not found.\n");
            log_error("cd2", "Directory not found.");
        }
    }
}

void handleEcho(const char *arg, int redirect_fd) {
    if (redirect_fd!= -1) {
        int temp_fd = dup(STDOUT_FILENO);
        dup2(redirect_fd, STDOUT_FILENO);
        close(redirect_fd);
        if (arg!= NULL) {
            printf("%s\n", arg);
        } else {
            printf("\n");
        }
        dup2(temp_fd, STDOUT_FILENO);
        close(temp_fd);
    } else {
        if (arg!= NULL) {
            printf("%s\n", arg);
        } else {
            printf("\n");
        }
    }
}

void handlePwd(int redirect_fd) {
    char cwd[PATH_MAX];
    if (getcwd(cwd, sizeof(cwd))!= NULL) {
        if (redirect_fd!= -1) {
            int temp_fd = dup(STDOUT_FILENO);
            dup2(redirect_fd, STDOUT_FILENO);
            close(redirect_fd);
            printf("%s\n", cwd);
            dup2(temp_fd, STDOUT_FILENO);
            close(temp_fd);
        } else {
            printf("%s\n", cwd);
        }
    } else {
        perror("pwd2");
        log_error("pwd2", strerror(errno));
    }
}

void handleLs(int redirect_fd) {
    DIR *d;
    struct dirent *dir;
    d = opendir(".");
    if (d) {
        if (redirect_fd!= -1) {
            int temp_fd = dup(STDOUT_FILENO);
            dup2(redirect_fd, STDOUT_FILENO);
            close(redirect_fd);
            while ((dir = readdir(d))!= NULL) {
                printf("%s\n", dir->d_name);
            }
            dup2(temp_fd, STDOUT_FILENO);
            close(temp_fd);
        } else {
            while ((dir = readdir(d))!= NULL) {
                printf("%s\n", dir->d_name);
            }
        }
        closedir(d);
    } else {
        perror("ls2");
        log_error("ls2", strerror(errno));
    }
}

void handleTouch(const char *arg) {
    if (arg!= NULL) {
        FILE *file = fopen(arg, "a");
        if (file) {
            fclose(file);
        } else {
            perror("touch2");
            log_error("touch2", strerror(errno));
        }
    } else {
        fprintf(stderr, "Missing file name for touch.\n");
    }
}

void handleCat(const char *arg, int redirect_fd) {
    if (arg!= NULL) {
        FILE *file = fopen(arg, "r");
        if (file) {
            char line[MAXLINE];
            int lineNumber = 1;
            if (redirect_fd!= -1) {
                int temp_fd = dup(STDOUT_FILENO);
                dup2(redirect_fd, STDOUT_FILENO);
                close(redirect_fd);
                while (fgets(line, sizeof(line), file)) {
                    printf("%d %s", lineNumber++, line);
                }
                dup2(temp_fd, STDOUT_FILENO);
                close(temp_fd);
            } else {
                while (fgets(line, sizeof(line), file)) {
                    printf("%d %s", lineNumber++, line);
                }
            }
            fclose(file);
        } else {
            perror("cat2");
            log_error("cat2", strerror(errno));
        }
    } else {
        fprintf(stderr, "Missing file name for cat.\n");
    }
}

void handleCp(const char *arg1, const char *arg2) {
    if (arg1 == NULL || arg2 == NULL) {
        fprintf(stderr, "Missing file names for cp.\n");
        return;
    }
    FILE *src = fopen(arg1, "r");
    FILE *dest = fopen(arg2, "w");
    if (src && dest) {
        char line[MAXLINE];
        while (fgets(line, sizeof(line), src)) {
            fputs(line, dest);
        }
        fclose(src);
        fclose(dest);
    } else {
        perror("cp2");
        log_error("cp2", strerror(errno));
    }
}

void handleRm(const char *arg, int recursive) {
    if (arg == NULL) {
        fprintf(stderr, "Missing file name for rm.\n");
        return;
    }
    if (recursive) {
        char command[MAXLINE];
        snprintf(command, MAXLINE, "rm -r %s", arg);
        if (system(command) == -1) {
            perror("Error removing directory");
            log_error("rm2 -r", strerror(errno));
        }
    } else {
        if (remove(arg) == -1) {
            perror("Error removing file");
            log_error("rm2", strerror(errno));
        }
    }
}

void handleRename(const char *arg1, const char *arg2) {
    if (arg1 == NULL || arg2 == NULL) {
        fprintf(stderr, "Missing file names for rename.\n");
        return;
    }
    if (rename(arg1, arg2) == -1) {
        perror("Error renaming file");
        log_error("rename2", strerror(errno));
    }
}