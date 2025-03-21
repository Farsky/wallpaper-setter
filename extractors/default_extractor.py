from typing import List

from scrapy import Selector

from config import get_config


def extract_images(html: str) -> List[str]:
    # Extract image URLs
    selector = Selector(text=html)
    image_urls = selector.css("img::attr(src)").getall()

    config = get_config()

    # Filter premium images and do not reuse previous image
    return [
        url
        for url in image_urls
        if "premium_photo" in url
        and (config.last_image is None or url != config.last_image)
    ]
