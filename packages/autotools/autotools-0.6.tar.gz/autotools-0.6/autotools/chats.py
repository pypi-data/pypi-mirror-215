from .audio import speech_to_text, string_to_speech
from .chatgpt import _get_response


def voice_chat(behaviour: str) -> None:
    """
    Runs a voice chat program with an AI assistant. Takes in a string 'behaviour'
    as input, which determines the type of chat behaviour the AI assistant will
    exhibit. Returns None.

    Parameters:
    behaviour (str): The type of chat behaviour to exhibit.

    Returns:
    None
    """
    message_log = [
        {"role": "system", "content": behaviour}
    ]

    while True:
        user_input = speech_to_text()
        if user_input.lower() == "выход":
            print("До свидания!")
            break
        message_log.append({"role": "user", "content": user_input})
        response = _get_response(message_log)
        message_log.append({"role": "assistant", "content": response})
        string_to_speech(response)
        print(f"ИИ: {response}")

        if 'exit' in response.lower():
            print('ChatGPT has exited the program')
            break


def chat(behaviour: str) -> None:
    """
    Creates a chat between the user and an AI assistant. The function takes in a string 'behaviour' as a parameter, 
    which is used to initialize the message log. The function then enters into a while loop and prompts the user for 
    input. If the user enters 'exit', the function returns None. Otherwise, the user's input is appended to the message 
    log, and the function calls a helper function '_get_response' to retrieve the AI's response. The AI's response is 
    then appended to the message log and printed to the console. 

    Args:
    - behaviour (str): A string used to initialize the message log.

    Returns:
    - None
    """
    message_log = [
        {"role": "system", "content": behaviour}
    ]

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            return

        message_log.append({"role": "user", "content": user_input})

        response = _get_response(message_log)

        message_log.append({"role": "assistant", "content": response})
        print(f"AI assistant: {response}")
