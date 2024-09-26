import re

from src.exceptions.bad_request import BadRequestError


class RegexValidator:
    def __init__(
        self,
        *,
        string: str,
        regex: str,
        exception: type[BadRequestError],
    ) -> None:
        self._string = string
        self._pattern = re.compile(regex)
        self._exception = exception

        self._validate()

    def _validate(self) -> None:
        if not re.match(self._pattern, self._string):
            raise self._exception
