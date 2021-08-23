from bs4 import BeautifulSoup
import os
import asyncio
from aiohttp import ClientSession


main_url = "https://earthview.withgoogle.com/"
loop = asyncio.get_event_loop()
lock = asyncio.Lock()
checkCount = 0


async def DownloadImage(url: str, Count: int):
    async with ClientSession() as session:
        async with session.get(url) as resp:
            with open(f"{Count}.png", "wb") as file:
                file.write(await resp.read())
            print(f"write image {Count}")


async def makeRequest(Count: int):
    global checkCount
    async with ClientSession() as session:
        async with session.get(f"{main_url}/{Count}") as resp:
            if not resp.status == 200:
                return

            async with lock:
                checkCount += 1

            print(f"Found: {Count}")
            ImageElement = BeautifulSoup(await resp.text(), "html.parser").find(class_="photo-view--active")
            await DownloadImage(ImageElement["src"], Count)


async def main():
    global checkCount
    print("earthview with google batch downloader")
    
    starts = int(input("starts at: "))
    stops = int(input("stops at: "))

    try:
        os.mkdir("images")
    except:
        print('folder "images" already exists')
    finally:
        os.chdir("images")

    await asyncio.gather(*[makeRequest(count) for count in range(starts, stops+1)])
    print(f"{checkCount}/{stops - starts} check")
    loop.stop()


if __name__ == "__main__":
    loop.create_task(main())
    loop.run_forever()
