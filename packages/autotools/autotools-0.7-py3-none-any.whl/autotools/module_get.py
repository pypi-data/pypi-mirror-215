from inspect import getmembers, isfunction
import requests as req
from importlib import import_module

def get_funcs_from_py_file(filename: str = '') -> list:
    """
    Gets all the functions from a Python file specified by `filename`.

    :param filename: A string representing the name of the Python file.
    :type filename: str
    :return: A list of functions present in the specified Python file.
    :rtype: list
    """
    mod = import_module(filename)
    members = getmembers(mod, isfunction)
    result = [s[1] for s in members]
    return result

def temp_func_from_url(filename:str, url: str) -> None:
    """
    Retrieves the Python file from the specified URL and writes it to a local file named 'tmp.py'.
    It then retrieves all the functions from the 'tmp.py' file using the 'get_funcs_from_py_file' function.

    :param url: A string representing the URL of the Python file to retrieve.
    :type url: str

    :return: None
    :rtype: None
    """
    import atexit
    import os
    import shutil
    response = req.get(url)
    os.makedirs("tempy", exist_ok=True)
    with open("tempy/" + filename, "w") as f:
        f.write(response.text)
    def cleanup():
        try:
            shutil.rmtree("tempy")
        except:
            pass
    atexit.register(cleanup)
    try:
        tmp = import_module("tmp")
    except:
        raise Exception('Error while importing module. Try again')
    return tmp
