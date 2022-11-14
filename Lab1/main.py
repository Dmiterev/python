import os
import requests
import shutil
from bs4 import BeautifulSoup as BS
HEADERS={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/80.0.3987.163 Safari/537.36"}


def dataset_create() -> None:
    """
    Проверяет существование папки dataset.
    Cоздает папку dataset и ее подпапки.
    """
    try:
        if not os.path.isdir("dataset"):
            os.mkdir("dataset")
        else:
            shutil.rmtree("dataset")
            os.mkdir("dataset")
    except OSError as err:
        print(f"Возникла ошибка!!{err}")



def store_image(image_url: str, index: int, path: str) -> None:
    """
   Сохраняет полученное изображение в подпапку dataset и дает ему название согласно индексу.

   :param image_url: ссылка на изображение
   :param index: индекс изображения
   :param path: путь к папке
    """
    saved_image = requests.get(f"https:{image_url}").content
    file = f"{path}/{index:04d}.jpg"
    with open(file, "wb") as save:
        save.write(saved_image)
        save.close()


def download_images(name: str, n: int, path: str, url = "https://yandex.ru/images/") -> None:
    """
    Получает html код страницы.
    Через цикл сохраняет N изображений в папку с помощью функции store_image.

    :param name: название поискового запроса
    :param n: число изображений, которое нужно сохранить
    :param path: путь к папке
    :param URL: адрес страницы, с которой будут парситься изображения
    """
    index = 1
    page = 0
    html = requests.get(f"{url}search?p={page}&text={name}&lr=51&rpt=image", HEADERS)
    soup = BS(html.text, 'lxml')
    all_images = soup.findAll("img")
    os.mkdir(path)
    while (True):
        for image in all_images:
            if index > n:
                break
            image_url = image.get("src")
            if image_url != "":
                store_image(image_url, index, path)
                index += 1
            print(f"Сохранено {index} изображений с запросом {name}")
        page += 1
        break


if __name__ == "__main__":
    dataset_create()
    tiger_path = os.path.join('dataset', 'tiger')
    leopard_path = os.path.join('dataset', 'leopard')
    download_images("tiger", 999, tiger_path)
    download_images("leopard", 999, leopard_path)
    print("Изображения сохранены!")