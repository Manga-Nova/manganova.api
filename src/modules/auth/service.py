from typing import TYPE_CHECKING

from src.core.validators import RegexValidator
from src.exceptions.bad_request import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidUsernameError,
    PasswordsDoNotMatchError,
)
from src.exceptions.conflict import PasswordAlreadyUsedError, UsernameAlreadyExistsError
from src.exceptions.unauthorized import EmailOrPasswordError
from src.modules.auth.dtos import (
    ChangePasswordParams,
    LoginParams,
    LoginResponse,
    Payload,
    RegisterParams,
)
from src.modules.user.dtos import User
from src.settings import Settings

if TYPE_CHECKING:
    from src.core.crypt import CryptHelper
    from src.modules.auth.repository import AuthRepository


class AuthService:
    def __init__(
        self,
        auth_repository: "AuthRepository",
        crypt_helper: "CryptHelper",
    ) -> None:
        self.repository = auth_repository
        self.crypt_helper = crypt_helper

    async def login(self, params: LoginParams) -> LoginResponse:
        """Login with email and password."""
        user = await self.repository.get_user(email=params.email)
        if not user:
            raise EmailOrPasswordError

        if not self.crypt_helper.check_password(params.password, user.password):
            raise EmailOrPasswordError

        token = self.crypt_helper.encode(
            Payload(
                stay_logged_in=params.stay_logged_in,
                **user.model_dump(),
            ).model_dump(),
            stay_logged_in=params.stay_logged_in,
        )

        return LoginResponse(user=User(**user.model_dump()), access_token=token)

    async def register(self, params: RegisterParams) -> LoginResponse:
        """Register a new user."""

        if _user := await self.repository.get_user_by_email_or_username(
            params.email,
            params.username,
        ):
            if _user.email == params.email:
                raise EmailOrPasswordError

            if _user.username == params.username:
                raise UsernameAlreadyExistsError

        RegexValidator(
            string=params.username,
            regex=Settings.USERNAME_REGEX,
            exception=InvalidUsernameError,
        )

        RegexValidator(
            string=params.email,
            regex=Settings.EMAIL_REGEX,
            exception=InvalidEmailError,
        )

        RegexValidator(
            string=params.password,
            regex=Settings.PASSWORD_REGEX,
            exception=InvalidPasswordError,
        )

        params.password = self.crypt_helper.hash_password(params.password)

        user = await self.repository.create_user(params)

        token = self.crypt_helper.encode(
            Payload(**user.model_dump(), stay_logged_in=False).model_dump(),
        )

        return LoginResponse(user=User(**user.model_dump()), access_token=token)

    async def change_password(self, user_id: int, params: ChangePasswordParams) -> User:
        """Change the password of the current user."""
        user = await self.repository.get_user(id=user_id)
        if not user:
            raise EmailOrPasswordError

        if self.crypt_helper.check_password(params.new_password, user.password):
            raise PasswordsDoNotMatchError

        old_hashes = await self.repository.get_old_passwords(user_id=user.id)

        for old_hash in old_hashes:
            if self.crypt_helper.check_password(params.new_password, old_hash.password):
                raise PasswordAlreadyUsedError

        RegexValidator(
            string=params.new_password,
            regex=Settings.PASSWORD_REGEX,
            exception=InvalidPasswordError,
        )

        new_password = self.crypt_helper.hash_password(params.new_password)

        user = await self.repository.update_user_password(user, new_password)
        return User(**user.__dict__)
