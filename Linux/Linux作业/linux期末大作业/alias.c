#include "alias.h"

#define MAX_ALIAS_COUNT 50
#define MAX_ALIAS_LENGTH 50

typedef struct {
    char alias[MAX_ALIAS_LENGTH];
    char command[MAX_ALIAS_LENGTH];
} Alias;

Alias aliases[MAX_ALIAS_COUNT];
int alias_count = 0;

void add_alias(const char *alias_name, const char *command) {
    if (alias_count < MAX_ALIAS_COUNT) {
        strcpy(aliases[alias_count].alias, alias_name);
        strcpy(aliases[alias_count].command, command);
        alias_count++;
    } else {
        fprintf(stderr, "Too many aliases. Cannot add more.\n");
    }
}

char *get_command_from_alias(const char *command) {
    for (int i = 0; i < alias_count; i++) {
        if (strcmp(command, aliases[i].alias) == 0) {
            return aliases[i].command;
        }
    }
    return NULL;
}