
#ifndef SHELL_FUNCTIONS_H
#define SHELL_FUNCTIONS_H

// 各个功能函数声明
void menu();
void cd2(int argc, char *argv[]);
void pwd2();
void echo2(int argc, char *argv[]);
void ls2();
void touch2(int argc, char *argv[]);
void cat2(int argc, char *argv[]);
void cp2(int argc, char *argv[]);
void rm2(int argc, char *argv[]);
void rename2(int argc, char *argv[]);
void history2();
void quit(int argc, char *argv[]);

void print_welcome();
void print_prompt(const char *cwd);
void record_error(const char *command, const char *error_message);
int access_external_program(const char *command);
int redirect_output(const char *command, const char *filename, int append);
int my_pipe(const char *command1, const char *command2);

#endif
