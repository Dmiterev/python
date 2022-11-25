import os
import sys
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow, QFileDialog, QLabel
import copy_dataset
import main
import random_copy
from Iterator import ElementIterator
from main import Annotation


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle("Main Window")
        self.setMinimumSize(1000, 500)
        self.setStyleSheet("background-color : #98F5FF")
        self.dataset_path = QFileDialog.getExistingDirectory(self)
        if self.dataset_path.replace("/", "\\") != os.path.abspath(os.path.join("dataset")):
            print("Неправильная папка!")
            self.exit
        else:
            self.tiger_index = 0
            self.leopard_index = 0
            self.tiger_path = os.path.join("dataset", "tiger", "0000.jpg")
            self.leopard_path = os.path.join("dataset", "leopard", "0000.jpg")

            self.image_tiger = QtWidgets.QLabel(self)
            self.image_tiger.setPixmap(QtGui.QPixmap(self.tiger_path))
            self.image_tiger.setFixedSize(QSize(500, 200))
            self.image_tiger.move(300, 50)

            self.image_leopard = QtWidgets.QLabel(self)
            self.image_leopard.setPixmap(QtGui.QPixmap(self.leopard_path))
            self.image_leopard.setFixedSize(QSize(500, 200))
            self.image_leopard.move(300, 300)

            button_create_annotation = self.add_button("Создать аннотацию к датасету", 250, 50, 5, 50)
            button_create_annotation.setStyleSheet("background-color : #FF6103")
            button_create_annotation.clicked.connect(self.create_annotation)

            button_copy_dataset = self.add_button("Скопировать датасет", 250, 50, 5, 100)
            button_copy_dataset.setStyleSheet("background-color : #FF6103")
            button_copy_dataset.clicked.connect(self.copy_dataset)

            button_copy_random_dataset = self.add_button("Скопировать датасет в случайном порядке", 250, 50, 5, 150)
            button_copy_random_dataset.setStyleSheet("background-color : #FF6103")
            button_copy_random_dataset.clicked.connect(self.random_copy)

            next_tiger_button = self.add_button("Показать следующего тигра", 250, 50, 5, 200)
            next_tiger_button.setStyleSheet("background-color : #FF6103")
            next_tiger_button.clicked.connect(lambda tiger=self.tiger_path: self.next_tiger())

            next_leopard_button = self.add_button("Показать следующего леопарда", 250, 50, 5, 250)
            next_leopard_button.setStyleSheet("background-color : #FF6103")
            next_leopard_button.clicked.connect(lambda leopard=self.leopard_path: self.next_leopard())

            exit_button = self.add_button("Выйти из программы", 250, 50, 5, 300)
            exit_button.setStyleSheet("background-color : #53868B")
            exit_button.clicked.connect(self.exit)

            self.text = QLabel("", self)
            self.text.setFixedSize(QSize(250, 50))
            self.text.move(5, 350)

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

    def create_annotation(self) -> None:
        """
        Создает аннотацию к датасету.
        """
        main.check_file("dataset")
        n = 0
        for class_name in main.CLASSES:
            obj = Annotation("dataset", class_name)
            for index in range(999):
                obj.add(os.path.abspath(os.path.join(class_name, f"{index:04d}.jpg")), f"{index:04d}.jpg", n)
                n = 1
        self.text.setText("Аннотация создана!")

    def copy_dataset(self) -> None:
        """
        Копирует датасет в другую директорию.
        """
        n = 0
        copy_dataset.create_dataset("dataset1")
        main.check_file("dataset1")
        for class_name in main.CLASSES:
            for index in range(999):
                copy_dataset.copy_element(Annotation("dataset1", class_name), n, index)
                n = 1
        self.text.setText("dataset скопирован в dataset1!")

    def random_copy(self) -> None:
        """
        Копирует датасет в другую директорию случайным образом.
        """
        n = 0
        copy_dataset.create_dataset("dataset2")
        main.check_file("dataset2")
        for class_name in main.CLASSES:
            for index in range(999):
                random_copy.random_copy_element(Annotation("dataset2", class_name), n, index)
                n = 1
        self.text.setText("dataset скопирован в dataset2 "
                          "случайным образом!")

    def next_tiger(self) -> None:
        """
        Выводит следующее изображение с тигром. Если они кончились, то выводится соответствующая надпись.
        """
        if self.tiger_index < 999:
            self.tiger_index += 1
            obj = ElementIterator(self.tiger_path)
            self.tiger_path = obj.__next__()
            self.image_tiger.setPixmap(QtGui.QPixmap(self.tiger_path))
        else:
            self.text.setText("Изображения кончились!")

    def next_leopard(self) -> None:
        """
        Выводит следующее изображение с леопардом. Если они кончились, то выводится соответствующая надпись.
        """
        if self.leopard_index < 999:
            self.leopard_index += 1
            obj = ElementIterator(self.leopard_path)
            self.leopard_path = obj.__next__()
            self.image_leopard.setPixmap(QtGui.QPixmap(self.leopard_path))
        else:
            self.text.setText("Изображения кончились!")

    def exit(self) -> None:
        """
        Выход из программы.
        """
        self.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()