from datetime import datetime
from http import HTTPStatus


from .no_menu_found import NoMenuFoundException


def handle_request_error(status_code: int, date: datetime):
    """Raise the correct error when the GET-request fails"""
    if status_code == HTTPStatus.NOT_FOUND:
        raise NoMenuFoundException(date)
