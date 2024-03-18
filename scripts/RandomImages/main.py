import time
from datetime import datetime
import argparse
import requests
import os

class ImageSearcher:
    # Setting API token
    def __init__(self, token, timeout = 10, divide = 'days'):
        self.token     = token
        self.timeout   = timeout
        self.divide_by = divide

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
        folder = os.getcwd() + "/images"
        def_folder = folder
        write_info = open(os.getcwd() + "/posts.log", "a", encoding="utf-8")

        if os.path.isdir(folder) == False:
            os.mkdir(folder)

        if self.divide_by == 'days' or self.divide_by == 'days_posts':
            date = datetime.now()
            folder += '/{0}-{1}-{2}'.format(str(date.month), str(date.day), date.year)
            def_folder = folder
        elif self.divide_by == 'posts':
            pass
        else:
            pass

        if os.path.isdir(folder) == False:
            os.mkdir(folder)

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
                
                photo = attachment['photo']['sizes'][-1]['url']
                image = requests.get(photo)
                if self.divide_by == 'posts' or self.divide_by == 'days_posts':
                    folder = def_folder + '/' + str(item['from_id']) + "_" + str(item['id'])
                    if os.path.isdir(folder) == False:
                        os.mkdir(folder)
                
                # Writing file
                out = open(folder + '/' + os.path.basename(photo.split('?')[0]), "wb")
                out.write(image.content)
                out.close()

                print('Downloaded ' + photo + ', sleeping for ' + str(self.timeout) + ' seconds\n')
                time.sleep(self.timeout)

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

        write_info.close()


parser = argparse.ArgumentParser(prog='Random VK Images', description='Downloads random VK images from global search.')
parser.add_argument('--token', type=str, help='VKAPI token.', default='')
parser.add_argument('--images_timeout', type=int, help='Timeout between downloading image in seconds (2 by default).', default=2)
parser.add_argument('--timeout', type=int, help='Timeout between Newsfeed.get method call in seconds (10 by default).', default=10)
parser.add_argument('--query', type=str, help='(Optional) Query param for Newsfeed.get method. Empty by default.', default='')
parser.add_argument('--count', type=int, help='Count of posts. 100 by default.', default=100)
parser.add_argument('--divide_by', type=str, help='Attachment division mode: \'days\', \'posts\', \'days_posts\', \'no\'', default='no')

args = parser.parse_args()

while True:
    has = ' has:photo'
    images = ImageSearcher(token=args.token, timeout=args.images_timeout, divide=args.divide_by)
    images.execute(q=args.query + has, count=args.count)

    time.sleep(args.timeout)
