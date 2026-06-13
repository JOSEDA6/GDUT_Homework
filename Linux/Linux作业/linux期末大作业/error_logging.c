#include "error_logging.h"

void log_error(const char *cmd, const char *error_msg) {
    char log_path[PATH_MAX];
    snprintf(log_path, sizeof(log_path), "%s/.shelldemo_err.log", getenv("HOME"));

    FILE *log_file = fopen(log_path, "a");
    if (log_file == NULL) {
        perror("Failed to open log file");
        return;
    }

    fprintf(log_file, "Command: %s\nError: %s\n\n", cmd, error_msg);
    fclose(log_file);
}