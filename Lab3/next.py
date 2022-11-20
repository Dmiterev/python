import os
import re


def next_element(element_path: str) -> str:
    """
    Принимает на вход путь к файлу и возвращает путь к следующему после него файлу. Если файла не существует,
    возвращается "Такого файла не существует". Если это последний файл, возвращается None.
    :param element_path: Путь к файлу.
    """
    if os.path.isfile(element_path):
        class_path, element = os.path.split(element_path)
        index = re.search(r'\d{4}', element)
        clear_index = int(index.group(0))
        clear_index += 1
        if clear_index < 1000:
            next_element = os.path.join(class_path, re.sub(r'\d{4}', f'{clear_index:04d}', element))
            return next_element
        else:
            return None
    else:
        return "Такого файла не существует"

if __name__ == "__main__":
    print(next_element("dataset\\tiger\\0000.jpg"))
