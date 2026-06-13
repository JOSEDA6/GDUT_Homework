void handleCd(const char *arg, char *currentPath);
void handleEcho(const char *arg, int redirect_fd);
void handlePwd(int redirect_fd);
void handleLs(int redirect_fd);
void handleTouch(const char *arg);
void handleCat(const char *arg, int redirect_fd);
void handleCp(const char *arg1, const char *arg2);
void handleRm(const char *arg, int recursive);
void handleRename(const char *arg1, const char *arg2);