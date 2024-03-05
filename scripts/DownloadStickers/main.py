import argparse
import requests
import os
import time

sticks_directory = os.getcwd() + "\\stickers"

parser = argparse.ArgumentParser(prog='Download VK Stickers', description='Downloads stickers from VK in given range.')
parser.add_argument('--start', type=int, help='Start from number', default=1)
parser.add_argument('--end', type=int, help='End on this number', default=100)
parser.add_argument('--size', type=int, help='Image size: 128, 256 or 512 (default).', default=512)
parser.add_argument('--timeout', type=int, help='Timeout between downloads in seconds.', default=4)

args = parser.parse_args()

if os.path.isdir(sticks_directory) == False:
    os.mkdir(sticks_directory)

if (args.size in [128, 256, 512]) == False:
    print('Invalid size.')
    exit()

for sticker in range(args.start, args.end):
    try:
        path = ("https://vk.com/sticker/1-" + str(sticker) + "-" + str(args.size) + ".png")
        
        picture = requests.get(path)

        out = open(sticks_directory + "\\" + str(sticker) + ".png", "wb")
        out.write(picture.content)
        out.close()

        print(path + " downloaded")
    except:
        print("Didn't downloaded :(")

    time.sleep(args.timeout)