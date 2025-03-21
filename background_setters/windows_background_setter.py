import ctypes
import os

import requests

from config import get_config, update_config

# Constants for setting the wallpaper
SPI_SETDESKWALLPAPER = 20  # Action to change wallpaper
SPIF_UPDATEINIFILE = 0x01  # Update user profile
SPIF_SENDWININICHANGE = 0x02  # Notify change to system


def set_wallpaper(image_url: str):
    config = get_config()

    with requests.get(image_url, stream=True) as response:
        response.raise_for_status()
        with open(config.local_image, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        str(os.path.abspath(config.local_image)),
        SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE,
    )

    update_config(last_image=image_url)
