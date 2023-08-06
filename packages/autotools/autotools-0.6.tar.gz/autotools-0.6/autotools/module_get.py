from inspect import getmembers, isfunction
import requests as req
from importlib import import_module

def get_funcs_from_py_file(filename: str = '') -> list:
    mod = import_module(filename)
    members = getmembers(mod, isfunction)
    result = [s[1] for s in members]
    return result

def temp_func_from_web(url: str) -> None:
    """
    Извлекает файл Python из указанного URL и записывает его в локальный файл с именем 'tmp.py'.
    Затем извлекает все функции из файла 'tmp.py' с помощью функции 'get_funcs_from_py_file'.

    :param url: Строка, представляющая URL файла Python для извлечения.
    :type url: str

    :return: None
    :rtype: None
    """
    response = req.get(url)
    with open("tmp.py", "w") as f:
        f.write(response.text)
    try:
        tmp = import_module("tmp")
    except ImportError:
        raise Exception('Неверный URL. Попробуйте еще раз.')
    return tmp
