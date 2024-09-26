import re


class EmailValidator:
    def __init__(self, email: str) -> None:
        self._email = email
        self._pattern = re.compile(
            r"^(?=.{4,256}$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        )

    def validate(self) -> None:
        """Validate email."""
        if not self._email:
            raise ValueError("Email is required")

        if not re.match(self._pattern, self._email):
            raise ValueError("Invalid email")
