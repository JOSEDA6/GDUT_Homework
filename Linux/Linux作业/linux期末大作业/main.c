#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <limits.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <errno.h>

#include "builtin_commands.h"
#include "command_execution.h"
#include "history.h"
#include "error_logging.h"
#include "alias.h"

#define MAXLINE 1024
#define MAX_HISTORY 100

int main() {
    char cmdline[MAXLINE];

    print_welcome();

    while (1) {
        char cwd[PATH_MAX];
        getcwd(cwd, sizeof(cwd));
        print_prompt(cwd);

        if (fgets(cmdline, MAXLINE, stdin) == NULL) {
            break;
        }

        if (cmdline[0] == '\n') {
            continue;
        }

        history_command(cmdline);
        eval(cmdline);
    }

    printf("######### Quiting shelldemo ############\n");
    return 0;
}