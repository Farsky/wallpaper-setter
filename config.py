import os


class Config:
    def __init__(self):
        self.cache_expiry = int(os.environ.get("CACHE_EXPIRY"))
        self.local_image = os.environ.get("LOCAL_IMAGE")
        self.cache_file = os.environ.get("CACHE_FILE")
        self.image_source = os.environ.get("IMAGE_SOURCE")
        self.last_fetch_time = os.environ.get("LAST_FETCH_TIME")
        self.last_image = os.environ.get("LAST_IMAGE")

        if self.image_source is None or self.image_source == "":
            raise ValueError("IMAGE_SOURCE is not set")

        if self.last_fetch_time is None or self.last_fetch_time == "":
            self.last_fetch_time = 0
        else:
            self.last_fetch_time = int(self.last_fetch_time)


_config = Config()


def get_config() -> Config:
    global _config
    return _config


def update_config(**kwargs):
    if len(kwargs) == 0:
        return

    global _config

    for key, value in kwargs.items():
        match key:
            case "last_fetch_time":
                _config.last_fetch_time = int(value)
            case "last_image":
                _config.last_image = str(value)

    with open(
        file=".env",
        mode="w",
        encoding="utf-8",
    ) as file:
        for key, value in _config.__dict__.items():
            file.write(f"{key}={value or ''}\n")

    print(f"Configuration updated with {kwargs}")
