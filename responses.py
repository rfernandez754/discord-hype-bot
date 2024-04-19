""" Module providing functionality for getting the response from the bot. """

def get_response(user_input: str) -> str:
    """ Decides a response to a given user input """
    lowered = user_input.lower()

    if lowered == '':
        return "Did not receive a message!"
    if 'hey' in lowered:
        return 'Hey !'
    if 'hi' in lowered:
        return 'hiiiiii'
    if 'hello' in lowered:
        return 'Hello!!!!'
    if 'bye' in lowered:
        return 'see ya'

    return 'I did not understand your message, sorry...'
