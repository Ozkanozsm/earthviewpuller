import requests
from bs4 import BeautifulSoup
import os

print("earthview with google batch downloader")
main_url = "https://earthview.withgoogle.com/"
starts = int(input("starts at: "))
stops = int(input("stops at: "))
check_count = 0

try:
    os.mkdir("images")
except:
    print('folder "images" already exists')
finally:
    os.chdir("images")

for i in range(starts, stops + 1):
    page = requests.get(main_url + str(i))
    print(i, end=": ")
    if page.status_code == 200:
        photo = BeautifulSoup(page.content, "html.parser").findAll("img", class_="photo-view--active")[0]
        photo_url = photo.attrs["src"]
        dosya = open("{}.jpg".format(i), "wb")
        dosya.write(requests.get(photo_url).content)
        dosya.close()
        print("check")
        check_count += 1
    else:
        print("nope")

print("{}/{} check".format(check_count, stops - starts + 1))
