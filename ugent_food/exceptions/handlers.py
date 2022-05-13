import typing
from http import HTTPStatus

from .internal_server_error import InternalServerError
from .no_menu_found import NoMenuFoundException


@typing.no_type_check
def handle_request_error(status_code: int, **kwargs):
    """Raise the correct error when the GET-request fails
    As every exception type gets arbitrary arguments, Mypy doesn't enjoy
    so the typing is ignored for this
    """
    if status_code == HTTPStatus.NOT_FOUND:
        raise NoMenuFoundException(kwargs.get("day"))

    if status_code >= 500:
        raise InternalServerError(status_code)
