import os


class Config:
    def __init__(self):
        self.cache_expiry: int = self._get_env_var("CACHE_EXPIRY", 43200, int)
        self.local_image: str = self._get_env_var("LOCAL_IMAGE", "wallpaper.jpg")
        self.cache_file: str = self._get_env_var("CACHE_FILE", "cache.html")
        self.image_source: str = self._get_env_var("IMAGE_SOURCE", required=True)
        self.last_fetch_time: int = self._get_env_var("LAST_FETCH_TIME", 0, int)
        self.last_image: str = self._get_env_var("LAST_IMAGE")

        if self.image_source is None or self.image_source == "":
            raise ValueError("IMAGE_SOURCE is not set")

        if self.last_fetch_time is None or self.last_fetch_time == "":
            self.last_fetch_time = 0
        else:
            self.last_fetch_time = int(self.last_fetch_time)

    def _get_env_var(self, key: str, default=None, type=str, required=False):
        value = os.environ.get(key, default)

        if required and value is None:
            raise ValueError(f"{key} is not set")
        try:
            return type(value)
        except ValueError:
            raise ValueError(f"Invalid value for {key}")


_config = Config()


def get_config() -> Config:
    global _config
    return _config


def update_config(**kwargs):
    if len(kwargs) == 0:
        return

    global _config

    # Update _config attributes directly if they exist
    for key, value in kwargs.items():
        match key:
            case "last_fetch_time":
                _config.last_fetch_time = int(value)
            case "last_image":
                _config.last_image = str(value)

    # Write updated config to .env file
    with open(".env", "w", encoding="utf-8") as file:
        file.writelines(
            f"{key}={value or ''}\n" for key, value in _config.__dict__.items()
        )

    print(f"Configuration updated with {kwargs}")
