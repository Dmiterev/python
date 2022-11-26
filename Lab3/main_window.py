import os
import sys
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import QSize
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
        self.setMinimumSize(1000, 500)
        self.setStyleSheet("background-color : #98F5FF")
        self.dataset_path = ""
        self.tiger_index = 0
        self.leopard_index = 0
        self.tiger_path = os.path.join("dataset", "tiger", "0000.jpg")
        self.leopard_path = os.path.join("dataset", "leopard", "0000.jpg")
        self.size = 0

        self.image_tiger = QtWidgets.QLabel(self)
        self.image_tiger.setPixmap(QtGui.QPixmap(self.tiger_path))
        self.image_tiger.setFixedSize(QSize(500, 200))
        self.image_tiger.move(300, 50)

        self.image_leopard = QtWidgets.QLabel(self)
        self.image_leopard.setPixmap(QtGui.QPixmap(self.leopard_path))
        self.image_leopard.setFixedSize(QSize(500, 200))
        self.image_leopard.move(300, 300)

        button_get_directory = self.add_button("Выбрать директорию для работы", 250, 50, 5, 50)
        button_get_directory.setStyleSheet("background-color : #800080")
        button_get_directory.clicked.connect(self.get_directory)

        button_create_annotation = self.add_button("Создать аннотацию к датасету", 250, 50, 5, 100)
        button_create_annotation.setStyleSheet("background-color :  #ADD8E6")
        button_create_annotation.clicked.connect(self.create_annotation)

        button_copy_dataset = self.add_button("Скопировать датасет", 250, 50, 5, 150)
        button_copy_dataset.setStyleSheet("background-color : #ADD8E6")
        button_copy_dataset.clicked.connect(self.copy_dataset)

        button_copy_random_dataset = self.add_button("Скопировать датасет в случайном порядке", 250, 50, 5, 200)
        button_copy_random_dataset.setStyleSheet("background-color : #ADD8E6")
        button_copy_random_dataset.clicked.connect(self.random_copy)

        next_tiger_button = self.add_button("Показать следующего тигра", 250, 50, 5, 250)
        next_tiger_button.setStyleSheet("background-color : #ADD8E6")
        next_tiger_button.clicked.connect(lambda tiger=self.tiger_path: self.next_image("tiger"))

        next_leopard_button = self.add_button("Показать следующего леопарда", 250, 50, 5, 300)
        next_leopard_button.setStyleSheet("background-color : #ADD8E6")
        next_leopard_button.clicked.connect(lambda leopard=self.leopard_path: self.next_image("leopard"))

        exit_button = self.add_button("Выйти из программы", 250, 50, 5, 350)
        exit_button.setStyleSheet("background-color : #53868B")
        exit_button.clicked.connect(self.exit)

        self.text_directory = QLabel(f"Текущая папка: {self.dataset_path}", self)
        self.text_directory.setFixedSize(QSize(500, 50))
        self.text_directory.move(5, 0)

        self.text = QLabel("", self)
        self.text.setFixedSize(QSize(285, 50))
        self.text.move(5, 400)

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
        self.size = 0
        self.dataset_path = QFileDialog.getExistingDirectory(self)
        self.text_directory.setText(f"Текущая папка: {self.dataset_path}")
        self.counting_images()
        if self.size == 0:
            self.text.setText("Программа не работает с такими папками!")
        else:
            self.text.setText("Папка выбрана!")

    def counting_images(self) -> None:
        for index in range(999):
            if os.path.isfile(os.path.join(self.dataset_path, "tiger", f"{index:04d}.jpg")):
                self.size += 1
            else:
                break

    def create_annotation(self) -> None:
        """
        Создает аннотацию к датасету.
        """
        if self.dataset_path != "":
            if self.size != 0:
                remove_annotation(self.dataset_path)
                n = 0
                for class_name in CLASSES:
                    obj = Annotation(self.dataset_path, class_name)
                    for index in range(self.size):
                        obj.add(os.path.abspath(os.path.join(class_name, f"{index:04d}.jpg")), f"{index:04d}.jpg", n)
                        n = 1
                self.text.setText("Аннотация создана!")
            else:
                self.text.setText("В папке нет изображений")
        else:
            self.text.setText("Папка еще не выбрана!")

    def copy_dataset(self) -> None:
        """
        Копирует датасет в другую директорию.
        """
        if self.dataset_path != "":
            if self.size != 0:
                self.text.setText("Выберите папку!")
                dataset1_path = QFileDialog.getExistingDirectory(self)
                if dataset1_path != "":
                    n = 0
                    create_dataset(dataset1_path)
                    remove_annotation(dataset1_path)
                    for class_name in CLASSES:
                        for index in range(self.size):
                            copy_element(Annotation(dataset1_path, class_name), n, index, self.dataset_path)
                            n = 1
                    self.text.setText("Папка скопирована")
            else:
                self.text.setText("В папке нет изображений")
        else:
            self.text.setText("Папка еще не выбрана!")

    def random_copy(self) -> None:
        """
        Копирует датасет в другую директорию случайным образом.
        """
        if self.dataset_path != "":
            if self.size != 0:
                self.text.setText("Выберите папку!")
                n = 0
                dataset2_path = QFileDialog.getExistingDirectory(self)
                if dataset2_path != "":
                    create_dataset(dataset2_path)
                    remove_annotation(dataset2_path)
                    for class_name in CLASSES:
                        for index in range(self.size):
                            random_copy_element(Annotation(dataset2_path, class_name), n, index, self.dataset_path)
                            n = 1
                    self.text.setText("Папка скопирована случайным образом!")
            else:
                self.text.setText("В папке нет изображений")
        else:
            self.text.setText("Папка еще не выбрана!")


    def next_image(self, class_name: str) -> None:
        """
        Выводит следующее изображение класса. Если они кончились, то выводится соответствующая надпись.
        :param class_name: Название класса.
        """
        if self.dataset_path != "":
            if self.size != 0:
                if class_name == "tiger":
                    if self.tiger_index < self.size - 2:
                        self.tiger_index += 1
                        obj = ElementIterator(self.tiger_path)
                        self.tiger_path = obj.__next__()
                        self.image_tiger.setPixmap(QtGui.QPixmap(self.tiger_path))
                    else:
                        self.text.setText("Изображения кончились!")
                else:
                    if self.leopard_index < self.size - 2:
                        self.leopard_index += 1
                        obj = ElementIterator(self.leopard_path)
                        self.leopard_path = obj.__next__()
                        self.image_leopard.setPixmap(QtGui.QPixmap(self.leopard_path))
                    else:
                        self.text.setText("Изображения кончились!")
            else:
                self.text.setText("В папке нет изображений")
        else:
            self.text.setText("Папка еще не выбрана!")

    def exit(self) -> None:
        """
        Выход из программы.
        """
        self.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
