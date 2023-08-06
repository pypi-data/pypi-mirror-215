import requests
import urllib.parse
from PIL.Image import open as open_image
def generate_image(prompt: str, open_img: bool = True) -> None:
    """
    Downloads an image based on a given prompt and saves it as 'img.jpg'. 
    If the 'open_img' flag is True, opens the saved image. 

    Args:
        prompt (str): The prompt used to generate the image.
        open_img (bool, optional): Determines whether or not to open the saved image. Defaults to True.

    Returns:
        None
    """
    formatted_prompt = urllib.parse.quote_plus(prompt)
    resp = requests.get('https://image.pollinations.ai/prompt/{}'.format(formatted_prompt))
    if resp.status_code != 200:
        raise Exception('request error. try again later')
    with open('img.png', 'wb') as f:
        for chunk in resp:
            f.write(chunk)
    if open_img:
        open_image('img.png').show()