"""Login test data. The credentials are the demo ones shown by the app itself."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class LoginCase:
    id: str
    username: str = ""
    password: str = ""
    saved_user: str | None = None
    error_field: Literal["username", "password"] | None = None
    error_message: str = ""


VALID_CASES: list[LoginCase] = [
    LoginCase(id="typed-credentials", username="bod@example.com", password="10203040"),
    LoginCase(id="saved-user", saved_user="bod@example.com"),
]

INVALID_CASES: list[LoginCase] = [
    LoginCase(
        id="empty-form",
        error_field="username",
        error_message="Username is required",
    ),
    LoginCase(
        id="locked-out-user",
        saved_user="alice@example.com (locked out)",
        error_field="password",
        error_message="Sorry this user has been locked out.",
    ),
]
