import os, requests,shutil
from bs4 import BeautifulSoup as BS

def dataset_create(name1,name2):
    """
    Проверяет существование папки dataset.
    Cоздает папку dataset и ее подпапки.
    """
    try:
        os.mkdir("dataset")
    except:
        shutil.rmtree("dataset")
        os.mkdir("dataset")
    os.makedirs(f"dataset/{name1}")
    os.makedirs(f"dataset/{name2}")

def store_image(image_url, name, index):
    """
   Сохраняет полученное изображение в подпапку dataset и дает ему название согласно индексу.
    """
    saved_image = requests.get(f"https:{image_url}").content
    store = open(f"dataset/{name}/{index:04d}.jpg", "wb")
    store.write(saved_image)
    store.close()

def download_images(name, N):
    """
    Получает html код страницы.
    Через цикл сохраняет N изображений в папку с помощью функции store_image.
    """
    index = 0
    page = 0
    html = requests.get(f"{URL}search?p={page}&text={name}&lr=51&rpt=image",Headers)
    soup = BS(html.text, 'lxml')
    all_images = soup.findAll("img")
    while  (index <= N):
        for image in all_images:
            if (index > N):
                break
            image_url = image.get("src")
            if (image_url != ""):
                store_image(image_url, name, index)
                index += 1
        page += 1

if __name__ == "__main__":
    Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}
    URL = "https://yandex.ru/images/"
    dataset_create("tiger", "leopard")
    download_images("tiger",999)
    download_images("leopard",999)
    print("Изображения сохранены!")