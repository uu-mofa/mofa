# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""This file contains the logger."""
import logging


def log_response(url, status_code, params=None, headers=None, data=None, json=None, text=None):
    """
    Log a response.

    :param url: The URL the request was sent to.
    :param params: The parameters used for the request.
    :param headers: The headers used for the request.
    :param json: The json used for the request.
    :param text: The response text to log.
    """
    ret = [f'API error! Status code = {status_code}. Data = {url}']

    if params is not None:
        ret.append(f'{params}')
    if headers is not None:
        ret.append(f'{headers}')
    if data is not None:
        ret.append(f'{data}')
    if json is not None:
        ret.append(f'{json}')
    if text is not None:
        ret.append(text.replace('\n', ''))

    logging.warning(' '.join(ret))


def log_text(text):
    """Put text in logger."""
    logging.warning(text)


def log_assistants(message, assistant_name):
    """
    Log an assistant information message.

    :param message: the message to be logged
    :param assistant_name: the name of the assistant
    """
    logging.warning(f'{assistant_name}: {message}')
