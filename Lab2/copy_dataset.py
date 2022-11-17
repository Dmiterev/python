import os
import shutil
from Lab2 import main
from main import Annotation


def create_dataset(directory: str) -> None:
    """
    Создание нового Датасета и проверка его существования.
    """
    try:
        if not os.path.isdir(directory):
            os.mkdir(directory)
        else:
            shutil.rmtree(directory)
            os.mkdir(directory)
    except OSError as err:
        print(f"Возникла ошибка!!{err}")


def copy_element(obj: type(Annotation), n: int, index: int) -> None:
    """
    Переносит элемент из dataset в dataset1, меняет его название и добавляет в новую аннотацию.
    :param obj: Объект класса Annotation.
    :param n: Число вхождений. Нужен, чтобы постоянно не записывалась строчка: "Абсолютный путь, Относительный путь,
        Название класса".
    :param index: Индекс изображения.
    """
    shutil.copy(os.path.join("dataset", obj.class_name, f"{index:04d}.jpg"), obj.directory)
    os.rename(os.path.join(obj.directory, f"{index:04d}.jpg"),
              os.path.join(obj.directory, f"{obj.class_name}_{index:04d}.jpg"))
    obj.add(os.path.abspath(obj.directory), f"{obj.class_name}_{index:04d}.jpg", n)


if __name__ == "__main__":
    n = 0
    create_dataset("dataset1")
    main.check_file("dataset1")
    for class_name in main.CLASSES:
        for index in range(999):
            copy_element(Annotation("dataset1", class_name), n, index)
            n += 1
