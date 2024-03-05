import time
import argparse
import requests
import os

class ImageSearcher:
    # Setting API token
    def __init__(self, token, timeout = 10):
        self.token   = token
        self.timeout = timeout

    # Running search by photos
    def execute(self, q = "", count = 100):
        print('Starting searching next ' + str(count) + ' posts')
        req = (requests.get('https://api.vk.com/method/newsfeed.search?q=' + requests.utils.quote(q) + "&count=" + str(count) + "&v=5.131&access_token=" + self.token)).json()

        if('error' in req):
            print('\n\n\n\nVK returned an error: \nCode: ' + str(req['error']['error_code']) + '\nMessage: ' + req['error']['error_msg'] + '\n\n\n\n')
            exit(0)

        response = req['response']
        items = response['items']
        totalPhotos = []

        write_info = open(os.getcwd() + "\\posts.log", "a", encoding="utf-8")

        if os.path.isdir(os.getcwd() + "\\images") == False:
            os.mkdir(os.getcwd() + "\\images")

        for item in items:
            attachments = item['attachments']

            # Logging
            write_info.write('\nLogged post ' + str(item['from_id']) + "_" + str(item['id'])
            + '\n'
            + 'Original text: ' + item['text']
            + '\n'
            + 'Attachments count: ' + str(len(attachments))
            + '\n'
            + '\nPhotos:')

            for attachment in attachments:
                if attachment['type'] != 'photo':
                    continue

                totalPhotos.append(attachment['photo']['sizes'][-1]['url'])
                write_info.write(
                      '\nId: '   + str(attachment['photo']['owner_id']) + "_" + str(attachment['photo']['id'])
                    + '\n'
                    + 'Date: ' + str(attachment['photo']['date'])
                    + '\n'
                    + 'URL: '  + attachment['photo']['sizes'][-1]['url']
                    + '\n'
                    + '_________________'
                )

            write_info.write('\n'
                             +
                             '________________________________________\n')

        print('Found ' + str(len(totalPhotos)) + ' photos. Downloading...\n')
        print('_________________________________\n')

        for photo in totalPhotos:
            image = requests.get(photo)

            # Writing file
            out = open(os.getcwd() + "\\images\\" + os.path.basename(photo.split('?')[0]), "wb")
            out.write(image.content)
            out.close()

            print('Downloaded ' + photo + ', sleeping for ' + str(self.timeout) + ' seconds\n')
            time.sleep(self.timeout)

        write_info.close()


parser = argparse.ArgumentParser(prog='Random VK Images', description='Downloads random VK images from global search.')
parser.add_argument('--token', type=str, help='VKAPI token.', default='')
parser.add_argument('--images_timeout', type=int, help='Timeout between downloading image in seconds (2 by default).', default=2)
parser.add_argument('--timeout', type=int, help='Timeout between Newsfeed.get method call in seconds (10 by default).', default=10)
parser.add_argument('--query', type=str, help='(Optional) Query param for Newsfeed.get method. Empty by default.', default='')
parser.add_argument('--count', type=int, help='Count of posts. 100 by default.', default=100)

args = parser.parse_args()

while True:
    images = ImageSearcher(token=args.token, timeout=args.images_timeout)
    images.execute(q=args.query + " has:photo", count=args.count)

    time.sleep(args.timeout)
