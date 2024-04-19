

def get_response(user_input: str) -> str:
    """ Decides a response to a given user input """
    lowered = user_input.lower()

    if lowered == '':
        return "Did not receive a message!"
    elif 'hey' in lowered:
        return 'Hey !'
    elif 'hi' in lowered:
        return 'hiiiiii'
    elif 'hello' in lowered:
        return 'Hello!!!!'
    elif 'bye' in lowered:
        return 'see ya'
    else:
        return 'I did not understand your message, sorry...'