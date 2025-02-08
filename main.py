from datetime import datetime
from random import randint
from urllib import request

from background_setters import windows_background_setter
from config import get_config, update_config
from extractors import default_extractor


def main():
    try:
        # Fetch HTML
        html = try_get_html()

        # Use your own extractor if you want
        image_urls = default_extractor.extract_images(html)

        # Get a random image
        url_index = randint(0, len(image_urls) - 1)
        image_url = image_urls[url_index]
        print(f"Selected image: {image_url}")

        # TODO: Set wallpaper on other devices
        windows_background_setter.set_wallpaper(image_url)
    except Exception as e:
        # Print error message if wallpaper change fails
        print(f"Error changing wallpaper: {e}")


def try_get_html() -> str:
    config = get_config()

    now = int(datetime.now().timestamp())

    # Get new HTML if cache expires
    expires = config.last_fetch_time < now - config.cache_expiry
    if expires:
        new_html = request.urlopen(config.image_source).read().decode("utf-8")

        with open(
            file=config.cache_file,
            mode="w",
            encoding="utf-8",
        ) as file:
            file.write(new_html)

        update_config(last_fetch_time=now)

        return new_html

    # Get HTML from cache
    with open(file=config.cache_file, encoding="utf-8") as file:
        return file.read()


if __name__ == "__main__":
    main()
