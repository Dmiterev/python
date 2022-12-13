import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2

CLASSES = ["tiger", "leopard"]


def dataframe_create(filename: str) -> pd.DataFrame:
    """
    Создает датафрейм по аннотации.
    :param filename: Название файла аннотации.
    """
    df = pd.read_csv(filename)
    df.drop(["Относительный путь"], axis=1, inplace=True)
    df = df.rename(columns={"Абсолютный путь": "absolute_path", "Название класса": "class_name"})
    add_columns(df)
    return df


def add_columns(df: pd.DataFrame) -> None:
    """
    Добавляет столбцы с меткой класса, высотой, шириной и глубиной изображения.
    :param df: Датафрейм.
    """
    width = []
    height = []
    depth = []
    label = (df.class_name != CLASSES[0])
    df["class_label"] = label.astype(int)
    for path in df.absolute_path:
        image = cv2.imread(path)
        image_height, image_width, image_depth = image.shape
        height.append(image_height)
        width.append(image_width)
        depth.append(image_depth)
    df["height"] = height
    df["width"] = width
    df["depth"] = depth


def label_filter(df: pd.DataFrame, label: str) -> pd.DataFrame:
    """
    Фильтрация датафрейма по метке класса.
    :param df: Датафрейм.
    :param label: Метка класса.
    """
    return df[df.class_label == label]


def max_filter(df: pd.DataFrame, label: str, max_height: int, max_width: int) -> pd.DataFrame:
    """
        Фильтрация датафрейма по метке класса, максимальной высоте и ширине.
        :param df: Датафрейм.
        :param label: Метка класса.
        :param max_height: Максимально значение высоты.
        :param max_width: Максимальное значение ширины.
        """
    return df[((df.class_label == label) & (df.height <= max_height) & (df.width <= max_width))]


def grouping(df: pd.DataFrame) -> tuple:
    """
    Группировка датафрейма по метке класса и вычисление максимального, минимального и среднего значения по количеству
    пикселей.
    :param df: Датафрейм.
    """
    df["pixels"] = df["width"] * df["height"] * df["depth"]
    return df.groupby("class_label").max(), df.groupby("class_label").min(), df.groupby("class_label").mean()


def histogram_construction(df: pd.DataFrame, label: str) -> list:
    """
    Построение гистограммы.
    :param df: Датафрейм.
    :param label: Метка класса.
    """
    df = label_filter(df, label)
    path = np.random.choice(df.absolute_path.to_numpy())
    image = cv2.imread(path)
    height, width, depth = image.shape
    return [cv2.calcHist([image], [0], None, [255], [0, 255]) / (height * width),
            cv2.calcHist([image], [1], None, [255], [0, 255]) / (height * width),
            cv2.calcHist([image], [2], None, [255], [0, 255]) / (height * width)]


def histogram_drawing(df: pd.DataFrame, label: str) -> None:
    """
    Отрисовка гистограмм, которые возвращаются из histogram_construction .
    :param df: Датафрейм.
    :param class_label: Метка класса.
    """
    histograms = histogram_construction(df, label)
    plt.title("Гистограмма")
    plt.ylabel("Плотность")
    plt.xlabel("Интенсивность")
    plt.xlim([0, 255])
    plt.plot(histograms[0], "b")
    plt.plot(histograms[1], "g")
    plt.plot(histograms[2], "r")
    plt.show()


if __name__ == "__main__":
    ann_df = dataframe_create("annotation.csv")
    ann_df.to_csv("DataFrame")
    label_filter(ann_df, 1).to_csv("DataFrame1")
    max_filter(ann_df, 1, 310, 500).to_csv("DataFrame2")
    histogram_drawing(ann_df, 0)
