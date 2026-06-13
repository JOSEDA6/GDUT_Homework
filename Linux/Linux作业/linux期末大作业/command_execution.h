int execute_external_command(char **argv, int redirect_fd, int pipeFlag);
char *get_command_path(char *command);
void execute_pipeline(char *cmd1, char *cmd2);