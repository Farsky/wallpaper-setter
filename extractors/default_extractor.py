from typing import List

from scrapy import Selector

from config import get_config


def extract_images(html: str) -> List[str]:
    # Extract image URLs
    selector = Selector(text=html)
    image_urls = selector.css("img::attr(src)").getall()

    config = get_config()

    # Filter premium images
    filtered_image_urls = filter(lambda url: "premium_photo" in url, image_urls)

    # Do not reuse previous image
    # TODO: Cache more used images
    if config.last_image is not None:
        filtered_image_urls = filter(
            lambda url: url not in config.last_image, filtered_image_urls
        )

    return list(filtered_image_urls)
