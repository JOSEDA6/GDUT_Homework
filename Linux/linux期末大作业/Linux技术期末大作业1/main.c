   #include <stdio.h>
   #include <string.h>
   #include <stdlib.h>
   #include <sys/types.h>
   #include <sys/wait.h>
   #include <unistd.h>
   #include <limits.h>
   #include "shell_functions.h"
   #include <time.h>
   #include <sys/utsname.h>

   #define MAXLINE 1024
   #define MAX_COMMAND_LENGTH 100
   #define MAX_HISTORY 100

   int history_count = 0;
   char *history[MAX_HISTORY];

   int main() {

       char command[MAX_COMMAND_LENGTH];
       char *argv[MAX_COMMAND_LENGTH];
       int argc;

       print_welcome();
       menu();

       while (1) {
           char cwd[PATH_MAX];
           getcwd(cwd, sizeof(cwd));
           print_prompt(cwd);

           if (fgets(command, MAX_COMMAND_LENGTH, stdin) == NULL) {
               // 处理 Ctrl + D 等退出情况
               printf("\n");
               exit(0);
           }

           // 去除换行符
           command[strcspn(command, "\n")] = '\0';

           // 保存历史命令
           if (history_count < MAX_HISTORY) {
               history[history_count++] = strdup(command);
           }

           argc = 0;
           argv[argc] = strtok(command, " ");
           while (argv[argc]!= NULL) {
               argc++;
               argv[argc] = strtok(NULL, " ");
           }

           if (argc == 0) {
               continue;
           }

           int i;
           for (i = 0; i < argc; i++) {
               if (strcmp(argv[i], "|") == 0) {
                   if (i > 0 && i + 1 < argc) {
                       return my_pipe(argv[i - 1], argv[i + 1]);
                   } else {
                       fprintf(stderr, "Invalid pipe command\n");
                       return -1;
                   }
               }
           }

           // 如果不是管道操作，按原逻辑处理
           if (strcmp(argv[0], "cd2") == 0) {
               cd2(argc, argv);
           } else if (strcmp(argv[0], "pwd2") == 0) {
               pwd2();
           } else if (strcmp(argv[0], "echo2") == 0) {
               echo2(argc, argv);
           } else if (strcmp(argv[0], "ls2") == 0) {
               ls2();
           } else if (strcmp(argv[0], "touch2") == 0) {
               touch2(argc, argv);
           } else if (strcmp(argv[0], "cat2") == 0) {
               cat2(argc, argv);
           } else if (strcmp(argv[0], "cp2") == 0) {
               cp2(argc, argv);
           } else if (strcmp(argv[0], "rm2") == 0) {
               rm2(argc, argv);
           } else if (strcmp(argv[0], "rename2") == 0) {
               rename2(argc, argv);
           } else if (strcmp(argv[0], "history2") == 0) {
               history2();
           } else if (strcmp(argv[0], "quit") == 0) {
               quit(argc, argv);
           } else {
               char error_msg[MAXLINE] = "Command not found";
               record_error(command, error_msg);
               fprintf(stderr, "Command not found\n");
           }
       }

       return 0;
   }

   void print_welcome() {
       printf("######## Welcometoshelldemo! #############\n");
   }

   void print_prompt(const char *cwd) {
       printf("[%s]>> ", cwd);
       fflush(stdout);
   }