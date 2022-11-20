import os
import shutil
import random
from main import Annotation
import copy_dataset
import main


def random_copy_element(obj: type(Annotation), n: int, index: int) -> None:
    """
    Копирует элемент из Dataset в Dataset2, дает ему случайный индекс(от 0 до 10000), меняет его название и добавляет в
    новую аннотацию.
    :param obj: Объект класса Annotation
    :param n: Число вхождений. Нужен, чтобы постоянно не записывалась строчка: "Абсолютный путь, Относительный путь,
        Название класса".
    :param index: Индекс изображения.
    """
    while True:
        rand_index = random.randint(0, 10000)
        if not os.path.isfile(os.path.join(obj.directory, f"{rand_index:05d}.jpg")):
            shutil.copy(os.path.join("dataset", obj.class_name, f"{index:04d}.jpg"), obj.directory)
            os.rename(os.path.join(obj.directory, f"{index:04d}.jpg"), os.path.join(obj.directory,
                                                                                    f"{rand_index:05d}.jpg"))
            obj.add(os.path.abspath(obj.directory), f"{rand_index:05d}.jpg", n)
            break


if __name__ == "__main__":
    n = 0
    copy_dataset.create_dataset("dataset2")
    main.check_file("dataset2")
    for class_name in main.CLASSES:
        for index in range(999):
            random_copy_element(Annotation("dataset2", class_name), n, index)
            n += 1
