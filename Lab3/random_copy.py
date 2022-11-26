import os
import shutil
import random
from main import Annotation


def random_copy_element(obj: type(Annotation), n: int, index: int, dataset_path: str) -> None:
    """
    Копирует элемент из Dataset в Dataset2, дает ему случайный индекс(от 0 до 10000), меняет его название и добавляет в
    новую аннотацию.
    :param obj: Объект класса Annotation
    :param n: Число вхождений. Нужен, чтобы постоянно не записывалась строчка: "Абсолютный путь, Относительный путь,
        Название класса".
    :param index: Индекс изображения.
    :param dataset_path: Путь к исходному датасету.
    """
    while True:
        rand_index = random.randint(0, 10000)
        if not os.path.isfile(os.path.join(obj.directory_path, f"{rand_index:05d}.jpg")):
            shutil.copy(os.path.join(dataset_path, obj.class_name, f"{index:04d}.jpg"), obj.directory_path)
            os.rename(os.path.join(obj.directory_path, f"{index:04d}.jpg"), os.path.join(obj.directory_path,
                                                                                    f"{rand_index:05d}.jpg"))
            obj.add(obj.directory_path, f"{rand_index:05d}.jpg", n)
            break

