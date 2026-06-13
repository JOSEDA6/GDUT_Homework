#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <limits.h>
#include <dirent.h>
#include <sys/stat.h>
#include <time.h>
#include <sys/utsname.h>
#define MAXLINE 1024
#define MAX_HISTORY 100


extern int history_count;
extern char *history[MAX_HISTORY];

// cd2
void cd2(int argc, char *argv[]) {
    if (argc > 1) {
        if (chdir(argv[1])!= 0) {
            perror("cd");
        }
    } else {
        char *home = getenv("HOME");
        if (home!= NULL) {
            if (chdir(home)!= 0) {
                perror("cd");
            }
        } else {
            fprintf(stderr, "HOME environment variable not set\n");
        }
    }
}

// pwd2
void pwd2() {
    char cwd[PATH_MAX];
    if (getcwd(cwd, sizeof(cwd))!= NULL) {
        printf("Your work path is %s\n", cwd);
    } else {
        perror("pwd2");
    }
}

// echo2
void echo2(int argc, char *argv[]) {
    for (int j = 1; j < argc; j++) {
        printf("%s ", argv[j]);
    }
    printf("\n");
}

// ls2
void ls2() {
    DIR *d;
    struct dirent *dir;
    d = opendir(".");
    if (d) {
        while ((dir = readdir(d))!= NULL) {
            printf("%s\n", dir->d_name);
        }
        closedir(d);
    } else {
        perror("ls2");
    }
}

// touch2
void touch2(int argc, char *argv[]) {
    for (int j = 1; j < argc; j++) {
        FILE *file = fopen(argv[j], "a");
        if (file) {
            fclose(file);
        } else {
            perror("touch2");
        }
    }
}

// cat2
void cat2(int argc, char *argv[]) {
    for (int j = 1; j < argc; j++) {
        FILE *file = fopen(argv[j], "r");
        if (file) {
            char line[MAXLINE];
            while (fgets(line, sizeof(line), file)) {
                printf("%s", line);
            }
            fclose(file);
        } else {
            perror("cat2");
        }
    }
}

// cp2，复制文件内容
void cp2(int argc, char *argv[]) {
    if (argc == 3) {
        FILE *src = fopen(argv[1], "r");
        FILE *dest = fopen(argv[2], "w");
        if (src && dest) {
            char line[MAXLINE];
            while (fgets(line, sizeof(line), src)) {
                fputs(line, dest);
            }
            fclose(src);
            fclose(dest);
        } else {
            perror("cp2");
        }
    } else {
        printf("Usage: cp2 source_file destination_file\n");
    }
}

// rm2，删除文件
void rm2(int argc, char *argv[]) {
    for (int j = 1; j < argc; j++) {
        if (remove(argv[j])!= 0) {
            perror("rm2");
        }
    }
}

// rename2
void rename2(int argc, char *argv[]) {
    if (argc == 3) {
        if (rename(argv[1], argv[2])!= 0) {
            perror("rename2");
        }
    } else {
        printf("Usage: rename2 old_name new_name\n");
    }
}



// history2
void history2() {
    for (int i = 0; i < history_count; i++) {
        printf("%d %s\n", i + 1, history[i]);
    }
}

// quit函数
void quit(int argc, char *argv[]) {
    exit(0);
}

// record_error函数
void record_error(const char *command, const char *error_message) {
    char *home = getenv("HOME");
    if (home == NULL) {
        return;
    }

    char log_path[PATH_MAX];
    snprintf(log_path, sizeof(log_path), "%s/.shelldemo_err.log", home);

    FILE *fp = fopen(log_path, "a");
    if (fp == NULL) {
        return;
    }

    fprintf(fp, "Command: %s\nError Message: %s\n\n", command, error_message);

    fclose(fp);
}

   int access_external_program(const char *command) {
       char *path = getenv("PATH");
       char *path_copy = strdup(path);
       char *dir = strtok(path_copy, ":");
       char full_path[PATH_MAX];
       int status;

       while (dir!= NULL) {
           snprintf(full_path, PATH_MAX, "%s/%s", dir, command);
           printf("Checking %s\n", full_path);
           if (access(full_path, X_OK) == 0) {
               pid_t pid = fork();
               if (pid == 0) {
                   execl(full_path, command, NULL);
                   perror("execl");
                   _exit(1);
               } else if (pid > 0) {
                   waitpid(pid, &status, 0);
                   return status;
               } else {
                   perror("fork");
                   return -1;
               }
           }
           dir = strtok(NULL, ":");
       }
       free(path_copy);
       return -1;
   }

   int redirect_output(const char *command, const char *filename, int append) {
       pid_t pid = fork();
       if (pid == 0) {
           int flags = O_CREAT;
           if (append) {
               flags |= O_APPEND;
           } else {
               flags |= O_TRUNC;
           }
           flags |= O_WRONLY;
           int fd = open(filename, flags, 0644);
           if (fd == -1) {
               perror("open");
               _exit(1);
           }
           dup2(fd, 1);
           close(fd);
           execlp(command, command, NULL);
           perror("execlp");
           _exit(1);
       } else if (pid > 0) {

           int status;
           waitpid(pid, &status, 0);
           return status;
       } else {
           perror("fork");
           return -1;
       }
   }

      int my_pipe(const char *command1, const char *command2) {
       int pipefd[2];
       pid_t pid1, pid2;

       if (pipe(pipefd) == -1) {
           perror("pipe");
           return -1;
       }

       pid1 = fork();
       if (pid1 == 0) {
           close(pipefd[0]);
           dup2(pipefd[1], 1);
           close(pipefd[1]);
           execlp(command1, command1, NULL);
           perror("execlp1");
           _exit(1);
       } else if (pid1 > 0) {
           pid2 = fork();
           if (pid2 == 0) {
               close(pipefd[1]);
               dup2(pipefd[0], 0);
               close(pipefd[0]);
               execlp(command2, command2, NULL);
               perror("execlp2");
               _exit(1);
           } else if (pid2 > 0) {
               close(pipefd[0]);
               close(pipefd[1]);
               int status1, status2;
               waitpid(pid1, &status1, 0);
               waitpid(pid2, &status2, 0);
               return status1 + status2;
           } else {
               perror("fork2");
               return -1;
           }
       } else {
           perror("fork1");
           return -1;
       }
   }

void display_threads_of_process(int pid) {
         char path[256];
         snprintf(path, sizeof(path), "/proc/%d/task", pid);
         DIR *dir = opendir(path);
         if (dir) {
             struct dirent *entry;
             while ((entry = readdir(dir))!= NULL) {
                 if (entry->d_type == DT_DIR && entry->d_name[0]!= '.') {
                     printf("Thread ID: %s\n", entry->d_name);
                 }
             }
             closedir(dir);
         } else {
             perror("opendir");
         }
     }

// 菜单函数
void menu() {
    time_t now;
    struct tm *tm_info;
    char date_str[100];
    time(&now);
    tm_info = localtime(&now);

    strftime(date_str, sizeof(date_str), "%Y/%m/%d", tm_info);
    printf("当前系统日期：%s\n", date_str);
    printf("请选择功能（输入对应数字）：\n");
    printf("1) 显示所有线程\n");
    printf("2) 显示当前用户\n");
    printf("3) 显示当前目录中的文件\n");
    printf("4) 显示计算机的名称\n");
    printf("5) 显示内核版本\n");
    char input[10];
    fgets(input, sizeof(input), stdin);

    input[strcspn(input, "\n")] = '\0';
    int choice = atoi(input);
    switch (choice) {
        case 1:
            int pid = getpid();
        	display_threads_of_process(pid);

            break;
        case 2:

                char *user = getenv("USER");
        if (user!= NULL) {
            printf("当前用户：%s\n", user);
        }
        break;
        case 3:
            ls2();
        break;
        case 4:
        {
            struct utsname uts;
            if (uname(&uts) == 0) {
                printf("计算机的名称：%s\n", uts.nodename);
            }
        }
        break;
        case 5:
        {
            struct utsname uts;
            if (uname(&uts) == 0) {
                printf("内核版本：%s\n", uts.release);
            }
        }
        break;
        
    }
}

