from inspect import getmembers, isfunction
import requests as req
import sys


def get_funcs_from_py_file(filename: str = '') -> list:
    exec('import {} as tmp'.format(filename))
    return [s[1] for s in getmembers(tmp, isfunction)]

def temp_fucnc_from_web(url: str) -> None:
    """
    Retrieves a Python file from a given URL and writes it to a local file named 'tmp.py'.
    Then extracts all functions from the 'tmp.py' file using 'get_funcs_from_py_file'.
    
    :param url: A string representing the URL of the Python file to be retrieved.
    :type url: str
    
    :return: None
    :rtype: None
    """
    a = req.get(url)
    with open("tmp.py", "w") as f:
        f.write(a.text)
    try:
        get_funcs_from_py_file("tmp")
    except:
        raise Exception('Wrong URL. Try again.')