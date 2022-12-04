import os
import sys
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow, QFileDialog, QLabel
from copy_dataset import create_dataset, copy_element
from main import remove_annotation, CLASSES, Annotation
from random_copy import random_copy_element
from Iterator import ElementIterator


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle("Work with images")
        self.setFixedSize(1200, 750)
        self.setStyleSheet("background-color : #98F5FF")
        self.dataset_path = ""
        self.tiger_index = 0
        self.leopard_index = 0
        self.tiger_path = ""
        self.leopard_path = ""
        self.dirname = ""

        self.image_tiger = QtWidgets.QLabel(self)
        self.image_tiger.resize(1000, 400)
        self.image_tiger.move(600, 50)

        self.image_leopard = QtWidgets.QLabel(self)
        self.image_leopard.resize(1000, 400)
        self.image_leopard.move(600, 350)

        button_get_directory = self.add_button("Выбрать директорию для работы", 350, 75, 5, 50)
        button_get_directory.setStyleSheet("background-color : #800080")
        button_get_directory.clicked.connect(self.get_directory)

        button_create_annotation = self.add_button("Создать аннотацию к датасету", 350, 75, 5, 125)
        button_create_annotation.setStyleSheet("background-color :  #ADD8E6")
        button_create_annotation.clicked.connect(self.create_annotation)

        button_copy_dataset = self.add_button("Скопировать датасет", 350, 75, 5, 200)
        button_copy_dataset.setStyleSheet("background-color : #ADD8E6")
        button_copy_dataset.clicked.connect(self.copy_dataset)

        button_copy_random_dataset = self.add_button("Скопировать датасет в случайном порядке", 350, 75, 5, 275)
        button_copy_random_dataset.setStyleSheet("background-color : #ADD8E6")
        button_copy_random_dataset.clicked.connect(self.random_copy)

        next_tiger_button = self.add_button("Показать следующего тигра", 350, 75, 5, 350)
        next_tiger_button.setStyleSheet("background-color : #ADD8E6")
        next_tiger_button.clicked.connect(lambda class_name="tiger": self.next_image("tiger"))

        next_leopard_button = self.add_button("Показать следующего леопарда", 350, 75, 5, 425)
        next_leopard_button.setStyleSheet("background-color : #ADD8E6")
        next_leopard_button.clicked.connect(lambda class_name="leopard": self.next_image("leopard"))

        exit_button = self.add_button("Выйти из программы", 350, 75, 5, 500)
        exit_button.setStyleSheet("background-color : #53868B")
        exit_button.clicked.connect(self.exit)

        self.text_directory = QLabel(f"Текущая папка: {self.dataset_path}", self)
        self.text_directory.setFixedSize(QSize(500, 50))
        self.text_directory.move(5, 0)

        self.text = QLabel("", self)
        self.text.setFixedSize(QSize(350, 75))
        self.text.move(5, 575)

        self.show()

    def add_button(self, button_name: str, width: int, height: int, x: int, y: int):
        """
        Добавление кнопки.
        :param button_name: Название кнопки.
        :param width: Ширина.
        :param height: Высота.
        :param x: Положение по X.
        :param y: Положение по Y.
        """
        button = QPushButton(button_name, self)
        button.setFixedSize(QSize(width, height))
        button.move(x, y)
        return button

    def get_directory(self) -> None:
        """
        Выбор директории для работы.
        """
        self.tiger_index = 0
        self.leopard_index = 0
        self.dataset_path = QFileDialog.getExistingDirectory(self)
        self.text_directory.setText(f"Текущая папка: {self.dataset_path}")
        self.dirname = os.path.dirname(self.dataset_path)
        if os.path.isdir(os.path.join(self.dataset_path, "tiger")) & os.path.isdir(os.path.join(self.dataset_path,
                                                                                                "leopard")):
            tigerfiles = []
            for (dirpath, dirnames, filenames) in os.walk(os.path.join(self.dataset_path, CLASSES[0])):
                tigerfiles.extend(filenames)
                self.tiger_path = os.path.join(self.dataset_path, CLASSES[0], tigerfiles[0])
                self.image_tiger.setPixmap(QtGui.QPixmap(self.tiger_path).scaled(self.image_tiger.height(),
                                          self.image_tiger.width(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
            leopardfiles = []
            for (dirpath, dirnames, filenames) in os.walk(os.path.join(self.dataset_path, CLASSES[1])):
                leopardfiles.extend(filenames)
                self.leopard_path = os.path.join(self.dataset_path, CLASSES[1], leopardfiles[0])
                self.image_leopard.setPixmap(QtGui.QPixmap(self.leopard_path).scaled(self.image_leopard.height(),
                                        self.image_leopard.width(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
                self.text.setText("Папка выбрана!")
        else:
            self.text.setText("В этой директории нет папок tiger и leopard!")

    def create_annotation(self) -> None:
        """
        Создает аннотацию к датасету.
        """
        if self.dataset_path != "":
            remove_annotation(self.dataset_path)
            n = 0
            for class_name in CLASSES:
                obj = Annotation(self.dataset_path, class_name)
                for index in range(len(os.listdir(os.path.join(self.dataset_path, class_name)))):
                    obj.add(os.path.abspath(os.path.join(class_name, f"{index:04d}.jpg")), f"{index:04d}.jpg", n)
                    n = 1
            self.text.setText("Аннотация создана!")
        else:
            self.text.setText("Папка еще не выбрана!")

    def copy_dataset(self) -> None:
        """
        Копирует датасет в другую директорию.
        """
        if self.dataset_path != "":
            self.text.setText("Выберите папку!")
            dataset1_path = QFileDialog.getExistingDirectory(self)
            if dataset1_path == self.dataset_path:
                self.text.setText("В эту папку нельзя копировать, с ней идет работа!")
            else:
                if dataset1_path != "":
                    n = 0
                    create_dataset(dataset1_path)
                    remove_annotation(dataset1_path)
                    for class_name in CLASSES:
                        for index in range(len(os.listdir(os.path.join(self.dataset_path, class_name)))):
                            copy_element(Annotation(dataset1_path, class_name), n, index, self.dataset_path)
                            n = 1
                    self.text.setText("Папка скопирована")
        else:
            self.text.setText("Папка не выбрана")

    def random_copy(self) -> None:
        """
        Копирует датасет в другую директорию случайным образом.
        """
        if self.dataset_path != "":
            self.text.setText("Выберите папку!")
            n = 0
            dataset2_path = QFileDialog.getExistingDirectory(self)
            if dataset2_path == self.dataset_path:
                self.text.setText("В эту папку нельзя копировать, с ней идет работа!")
            else:
                if dataset2_path != "":
                    create_dataset(dataset2_path)
                    remove_annotation(dataset2_path)
                    for class_name in CLASSES:
                        for index in range(len(os.listdir(os.path.join(self.dataset_path, class_name)))):
                            random_copy_element(Annotation(dataset2_path, class_name), n, index, self.dataset_path)
                            n = 1
                    self.text.setText("Папка скопирована случайным образом!")
        else:
            self.text.setText("Папка не выбрана")

    def next_image(self, class_name: str) -> None:
        """
        Выводит следующее изображение класса. Если они кончились, то выводится соответствующая надпись.
        :param class_name: Название класса.
        """
        if self.dataset_path != "":
            if class_name == "tiger":
                if self.tiger_index < len(os.listdir(os.path.join(self.dataset_path, class_name))) - 1:
                    self.tiger_index += 1
                    obj = ElementIterator(self.tiger_path)
                    self.tiger_path = obj.__next__()
                    self.image_tiger.setPixmap(QtGui.QPixmap(self.tiger_path).scaled(self.image_tiger.height(),
                                          self.image_tiger.width(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    self.text.setText("Изображения с тигром кончились!")
            else:
                if self.leopard_index < len(os.listdir(os.path.join(self.dataset_path, class_name))) - 1:
                    self.leopard_index += 1
                    obj = ElementIterator(self.leopard_path)
                    self.leopard_path = obj.__next__()
                    self.image_leopard.setPixmap(QtGui.QPixmap(self.leopard_path).scaled(self.image_leopard.height(),
                                        self.image_leopard.width(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    self.text.setText("Изображения с леопардом кончились!")
        else:
            self.text.setText("Папка не выбрана!")

    def exit(self) -> None:
        """
        Выход из программы.
        """
        self.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
