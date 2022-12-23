from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import requests, lxml, re, json, urllib.request
from bs4 import BeautifulSoup

from kinozal.models import Film

TIME_OUT = 10


def worker(queue: Queue):
    while True:

        movie = queue.get()

        print('[WORKING ON]', movie.title_en)

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
            }

            params = {
                "q": f"{movie.title_en} 4k background",
                "tbm": "isch",
                "hl": "en",
                "gl": "us",
                "ijn": "0"
            }

            html = requests.get("https://www.google.com/search", params=params,
                                headers=headers)
            soup = BeautifulSoup(html.text, "lxml")

            all_script_tags = soup.select("script")

            matched_images_data = "".join(
                re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags))
            )

            matched_images_data_fix = json.dumps(matched_images_data)
            matched_images_data_json = json.loads(matched_images_data_fix)
            matched_google_image_data = re.findall(
                r'\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}',
                matched_images_data_json)
            matched_google_images_thumbnails = ", ".join(
                re.findall(
                    r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                    str(matched_google_image_data))).split(", ")
            thumbnails = [
                bytes(bytes(thumbnail, "ascii").decode("unicode-escape"),
                      "ascii").decode("unicode-escape") for thumbnail in
                matched_google_images_thumbnails
            ]
            removed_matched_google_images_thumbnails = re.sub(
                r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                "", str(matched_google_image_data))
            matched_google_full_resolution_images = re.findall(
                r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]",
                removed_matched_google_images_thumbnails)
            full_res_images = [
                bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode(
                    "unicode-escape") for img in
                matched_google_full_resolution_images
            ]

            url_img = []
            for index, (metadata, thumbnail, original) in enumerate(
                    zip(soup.select(".isv-r.PNCib.MSM1fd.BUooTd"), thumbnails,
                        full_res_images), start=1):
                google_images = {
                    "title":
                        metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")[
                            "title"],
                    "link":
                        metadata.select_one(".VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")[
                            "href"],
                    "source": metadata.select_one(".fxgdke").text,
                    "thumbnail": thumbnail,
                    "original": original
                }
                url_img.append(google_images['original'])
            with requests.Session() as session:
                img_response = session.get(url_img[0], timeout=TIME_OUT)
            image_name = f'{movie.title_en}.jpg'.replace(' ', '-')
            if img_response.content:
                print('ok')
            with open(f'media/background/{image_name}', 'wb') as file:
                file.write(img_response.content)
                print('done')

            movie.background = f'background/{image_name}'
            movie.save()

            print('DONE!!!', url_img[0])


        except Exception as error:
            print('Error', error)

        if queue.qsize() == 0:
            break


def main():
    films = Film.objects.exclude(title_en='all')


    queue = Queue()

    for item in films:
        queue.put(item)

    max_worker = 10
    with ThreadPoolExecutor(max_workers=max_worker) as executor:
        for _ in range(max_worker):
            executor.submit(worker, queue)


if __name__ == '__main__':
    main()
