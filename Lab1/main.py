import os
import requests
import shutil
from bs4 import BeautifulSoup as BS


def dataset_create(name1,name2):
    """
    Проверяет существование папки dataset.
    Cоздает папку dataset и ее подпапки.
    """
    try:
        os.mkdir("dataset")
        os.mkdir(f"dataset/{name1}")
        os.mkdir(f"dataset/{name2}")
    except OSError:
        shutil.rmtree("dataset")
        os.mkdir("dataset")


def store_image(image_url, index, path):
    """
   Сохраняет полученное изображение в подпапку dataset и дает ему название согласно индексу.
    """
    saved_image = requests.get(f"https:{image_url}").content
    file = f"{path}/{index:04d}.jpg"
    with open(file, "wb") as save:
        save.write(saved_image)
        save.close()


def download_images(name, n, path):
    """
    Получает html код страницы.
    Через цикл сохраняет N изображений в папку с помощью функции store_image.
    """
    index = 1
    page = 0
    html = requests.get(f"{URL}search?p={page}&text={name}&lr=51&rpt=image", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"})
    soup = BS(html.text, 'lxml')
    all_images = soup.findAll("img")
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
    URL = "https://yandex.ru/images/"
    dataset_create("tiger", "leopard")
    tiger_path = os.path.join('dataset', 'tiger')
    os.mkdir(tiger_path)
    leopard_path = os.path.join('dataset', 'leopard')
    os.mkdir(leopard_path)
    download_images("tiger", 999, tiger_path)
    download_images("leopard", 999, leopard_path)
    print("Изображения сохранены!")