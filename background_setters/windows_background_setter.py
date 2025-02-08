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

    response = requests.get(image_url)
    if response.status_code != 200:
        raise ConnectionError(f"Failed to download image: {image_url}")

    with open(file=config.local_image, mode="wb") as file:
        file.write(response.content)

    wallpaperp_full_path = f"{os.getcwd()}/{config.local_image}"

    # Call Windows API to change wallpaper
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        wallpaperp_full_path,
        SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE,
    )

    update_config(last_image=image_url)
