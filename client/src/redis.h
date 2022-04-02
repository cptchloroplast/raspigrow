#define PORT 6789

void initRedis();
void publishRedis(char* channel, char* message);