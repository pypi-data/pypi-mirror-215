import requests as req
import os
import atexit
import shutil

def download_file(filename: str, url: str, method="wb") -> None:
    a = req.get(url)
    os.makedirs("tempy", exist_ok=True)
    with open("tempy/" + filename, method) as f:
        f.write(a.content)
    def cleanup():
        try:
            shutil.rmtree("tempy")
        except:
            pass
    atexit.register(cleanup)
