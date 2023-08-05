import openai

temperature: float = 0.1
max_tokens: int = 360


def set_api_key(api: str) -> None:
    openai.api_key = api


def set_temperature(new_temperature: float) -> None:
    """
    Sets the temperature to a new value.

    Args:
        new_temperature (float): The new temperature value to be set.
    
    Returns:
        None.
    
    Raises:
        ValueError: If the new_temperature value is not between 0 and 1.
    """
    if 0 > new_temperature > 1:
        raise ValueError('new_temperature must be between 0 and 1')

    global temperature
    temperature = new_temperature


def set_max_tokens(new_max_tokens: int) -> None:
    """
    Sets the value of the global variable max_tokens to the given integer. 
    
    Args:
        new_max_tokens (int): The new value to assign to max_tokens.
    
    Returns:
        None
    """
    global max_tokens
    max_tokens = new_max_tokens


def _get_response(message_log: list[dict]) -> str:
    """
    This function takes in a list of dictionaries `message_log` and returns a string `response`.
    It calls the `openai.ChatCompletion.create()` method with the specified arguments to generate a chatbot response.
    The generated response is then checked for the presence of "text" and returned if found.
    If the "text" is not present in any of the response choices, the first response is returned.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=message_log,
        max_tokens=max_tokens,
        stop=None,
        temperature=temperature,
    )

    for choice in response.choices:
        if "text" in choice:
            return choice.text

    return response.choices[0].message.content


def get_response(message: str, behaviour: str) -> str:
    """
    Takes in a message and a behaviour, logs the message and behaviour, gets a response using the logged data, 
    prints the response as an AI assistant message, and returns the response.
    
    Args:
    - message (str): The message to be logged.
    - behaviour (str): The behaviour to be logged.
    
    Returns:
    - response (str): The response received using the logged data.
    """
    message_log = [{"role": "system", "content": behaviour}, {"role": "user", "content": message}]
    response = _get_response(message_log)
    print("\n" + f"AI assistant: {response}" + "\n")
    return response
