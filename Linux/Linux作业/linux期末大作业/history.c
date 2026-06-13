#include "history.h"

void history_command(char *cmdline) {
    static int history_count = 0;
    if (history_count < MAX_HISTORY) {
        strcpy(history[history_count++], cmdline);
    } else {
        for (int i = 0; i < MAX_HISTORY - 1; i++) {
            strcpy(history[i], history[i + 1]);
        }
        strcpy(history[MAX_HISTORY - 1], cmdline);
    }
}

void print_history() {
    for (int i = 0; i < MAX_HISTORY; i++) {
        if (history[i][0]!= '\0') {
            printf("%d %s", i + 1, history[i]);
        }
    }
}