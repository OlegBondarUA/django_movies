import requests
from bs4 import BeautifulSoup


def urls_films():
    page = 1
    while True:
        response = requests.get('https://uakino.club/filmy/page/' + str(page))
        soup = BeautifulSoup(response.content, 'html.parser')

        items_list = soup.find_all('div', class_="movie-item short-item")
        links = []
        if len(items_list):
            for urls in items_list:
                url = urls.find('a', class_="movie-title").get('href').strip()
                links.append(url)
            print(links)
            with open('links.txt', 'a') as file:
                for line in links:
                    file.write(line + '\n')
            page += 1
        else:
            break


def main():

    urls_films()


if __name__ == '__main__':
    main()

