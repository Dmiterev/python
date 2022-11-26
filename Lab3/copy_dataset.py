import os
import shutil
from main import Annotation, remove_annotation, CLASSES


def create_dataset(directory_path: str) -> None:
    """
    Создание нового Датасета и проверка его существования.
    :param directory_path: Путь к директории.
    """
    try:
        if not os.path.isdir(directory_path):
            os.mkdir(directory_path)
        else:
            shutil.rmtree(directory_path)
            os.mkdir(directory_path)
    except OSError as err:
        print(f"Возникла ошибка!!{err}")


def copy_element(obj: type(Annotation), n: int, index: int, dataset_path: str) -> None:
    """
    Переносит элемент из dataset в dataset1, меняет его название и добавляет в новую аннотацию.
    :param obj: Объект класса Annotation.
    :param n: Число вхождений. Нужен, чтобы постоянно не записывалась строчка: "Абсолютный путь, Относительный путь,
        Название класса".
    :param index: Индекс изображения.
    :param dataset_path: Путь к исходному датасету.
    """
    shutil.copy(os.path.join(dataset_path, obj.class_name, f"{index:04d}.jpg"), obj.directory_path)
    os.rename(os.path.join(obj.directory_path, f"{index:04d}.jpg"),
              os.path.join(obj.directory_path, f"{obj.class_name}_{index:04d}.jpg"))
    obj.add(os.path.abspath(obj.directory_path), f"{obj.class_name}_{index:04d}.jpg", n)

