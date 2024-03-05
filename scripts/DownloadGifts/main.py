import argparse
import requests
import os
import time

gift_directory = os.getcwd() + "\\gifts"

parser = argparse.ArgumentParser(prog='Download VK Gifts', description='Downloads gifts from VK in given range.')
parser.add_argument('--start', type=int, help='Start from number', default=1)
parser.add_argument('--end', type=int, help='End on this number', default=100)
parser.add_argument('--timeout', type=int, help='Timeout between downloads in seconds.', default=4)

args = parser.parse_args()

if os.path.isdir(gift_directory) == False:
    os.mkdir(gift_directory)

for gift in range(args.start, args.end):
    try:
        path = ("https://vk.com/images/gift/" + str(gift) + "/256.jpg")
        
        picture = requests.get(path)

        out = open(gift_directory + "\\" + str(gift) + ".jpg", "wb")
        out.write(picture.content)
        out.close()

        print(path + " downloaded")
    except:
        print("Didn't downloaded :(")

    time.sleep(args.timeout)