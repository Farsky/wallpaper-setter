from datetime import datetime
from random import choice
from urllib import request

from background_setters import windows_background_setter
from config import get_config, update_config
from extractors import default_extractor


def main():
    try:
        html = _try_get_html()
        image_urls = default_extractor.extract_images(html)

        if not image_urls:
            raise ValueError("No images found")

        image_url = choice(image_urls)
        print(f"Selected image: {image_url}")

        windows_background_setter.set_wallpaper(image_url)
    except Exception as e:
        print(f"Error changing wallpaper: {e}")


def _try_get_html() -> str:
    config = get_config()

    now = int(datetime.now().timestamp())
    if now - config.last_fetch_time > config.cache_expiry:
        with request.urlopen(config.image_source) as response:
            new_html = response.read().decode("utf-8")
        with open(config.cache_file, "w", encoding="utf-8") as file:
            file.write(new_html)
        update_config(last_fetch_time=now)

    with open(config.cache_file, encoding="utf-8") as file:
        return file.read()


if __name__ == "__main__":
    main()
