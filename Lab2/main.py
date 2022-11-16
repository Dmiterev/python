import csv
import os

CLASSES = ["tiger", "leopard"]


def check_file(directory: str) -> None:
    """
    Проверяет существование файла annotation.csv.
    """
    try:
        if os.path.isfile(f"{directory}/annotation.csv"):
            os.remove(f"{directory}/annotation.csv")
    except OSError as err:
        print(f"Возникла ошибка!!{err}")


class Annotation:
    def __init__(self, directory: str, class_name: str) -> None:
        """
        :param directory: Название директории.
        :param class_name: Название класса.
        """
        self.directory = directory
        self.class_name = class_name
        self.row = 0

    def add(self, abs_path: str, name_image: str, N: int) -> None:
        """
        Добавление строки, в которой содержатся абсолютный и относительный пути к файлу и название класса.
        :param abs_path: Абсолютный путь к файлу.
        :param name_image: Название файла с изображением.
        :param N: Число вхождений. Нужен, чтобы постоянно не записывалась строчка: "Абсолютный путь, Относительный путь,
        Название класса".
        """
        with open(f"{self.directory}/annotation.csv", "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            if (self.row == 0) & (N == 0):
                writer.writerow(["Абсолютный путь", "Относительный путь", "Название класса"])
                self.row += 1
            writer.writerow([abs_path, os.path.join(self.directory, self.class_name, name_image), self.class_name])
            self.row += 1


if __name__ == "__main__":
    N = 0
    check_file("dataset")
    for class_name in CLASSES:
        obj = Annotation("dataset", class_name)
        for index in range(999):
            abs_path = os.path.abspath(f"{class_name}/{index:04d}.jpg")
            obj.add(abs_path, f"{index:04d}.jpg", N)
        N += 1
