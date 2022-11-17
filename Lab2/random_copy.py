import os
import shutil
import random
import main
from main import Annotation
import copy_dataset


def random_copy_element(obj: type(Annotation), N: int, index: int) -> None:
    """
    Копирует элемент из Dataset в Dataset2, дает ему случайный индекс(от 0 до 10000), меняет его название и добавляет в
    новую аннотацию.
    :param obj: Объект класса Annotation
    :param N: Число вхождений. Нужен, чтобы постоянно не записывалась строчка: "Абсолютный путь, Относительный путь,
        Название класса".
    :param index: Индекс изображения.
    """
    rand_index = random.randint(0, 10000)
    shutil.copy(os.path.join("dataset", obj.class_name, f"{index:04d}.jpg"), obj.directory)
    os.rename(os.path.join(obj.directory, f"{index:04d}.jpg"), os.path.join(obj.directory, f"{rand_index:05d}.jpg"))
    obj.add(os.path.abspath(obj.directory), f"{rand_index:05d}.jpg", N)


if __name__ == "__main__":
    N = 0
    copy_dataset.create_dataset("dataset2")
    main.check_file("dataset2")
    for class_name in main.CLASSES:
        for index in range(999):
            random_copy_element(Annotation("dataset2", class_name), N, index)
            N += 1