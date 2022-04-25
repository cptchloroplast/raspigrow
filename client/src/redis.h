#define REDIS_PORT 6379

void initRedis();
void publishRedis(char* channel, const char* message);