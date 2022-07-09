from src.settings import Settings


class Worker:
    settings: Settings

    def __init__(self, settings: Settings):
        self.settings = settings

    def start(self):
        print("start")


if __name__ == "__main__":
    settings = Settings()
    worker = Worker(settings)
    worker.start()
