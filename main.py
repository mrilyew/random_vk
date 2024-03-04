from ImageSearcher import ImageSearcher
from Settings import Settings
import time

settings = Settings().get()

while True:
    images = ImageSearcher(settings['vkapi_token'], settings['timeout_between_images'])
    images.execute(q=settings['query'] + "has:photo", count=settings['count'])

    time.sleep(settings['timeout'])
