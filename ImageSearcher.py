import requests
import os
import time

class ImageSearcher:
    # Setting API token
    def __init__(self, token, timeout = 10):
        self.token   = token
        self.timeout = timeout

    # Running search by photos
    def execute(self, q = "", count = 100):
        print('Starting searching next ' + str(count) + ' posts')
        req = requests.get('https://api.vk.com/method/newsfeed.search?q=' + q + "&count" + str(count) + "&v=5.131&access_token=" + self.token)

        response = req.json()['response']
        items = response['items']
        totalPhotos = []

        write_info = open(os.getcwd() + "\\info.txt", "a", encoding="utf-8")

        for item in items:
            attachments = item['attachments']

            # Logging
            write_info.write('\nLogged post ' + str(item['from_id']) + "_" + str(item['id'])
            + '\n'
            + 'Original text: ' + item['text']
            + '\n'
            + 'Attachments count: ' + str(len(attachments))
            + '\n')

            for attachment in attachments:
                if attachment['type'] != 'photo':
                    continue

                totalPhotos.append(attachment['photo']['sizes'][-1]['url'])
                write_info.write(
                      '\nPhotos:'
                    + '\nId: '   + str(attachment['photo']['owner_id']) + "_" + str(attachment['photo']['id'])
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

        print('Found ' + str(len(totalPhotos)) + ' photos')

        for photo in totalPhotos:
            image = requests.get(photo)

            # Writing file
            out = open(os.getcwd() + "\\pics\\" + os.path.basename(photo.split('?')[0]), "wb")
            out.write(image.content)
            out.close()

            print('Downloaded ' + photo + ', sleeping for ' + str(self.timeout) + ' seconds')
            time.sleep(self.timeout)

        write_info.close()
