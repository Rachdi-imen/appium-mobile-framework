"""Typed, validated configuration loaded from environment variables / .env."""

from functools import lru_cache
from pathlib import Path
from typing import Self

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.enums import ExecutionMode, Platform

ROOT_DIR: Path = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Single source of truth for every runtime option."""

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Execution -------------------------------------------------------
    platform: Platform = Platform.ANDROID
    execution_mode: ExecutionMode = ExecutionMode.LOCAL
    appium_server_url: str = "http://127.0.0.1:4723"
    explicit_wait_timeout: int = 15
    new_command_timeout: int = 120

    # --- Android (local) -------------------------------------------------
    android_device_name: str = "Android Emulator"
    android_platform_version: str | None = None
    android_app_path: Path = Path("apps/android-mydemoapp.apk")
    android_app_package: str = "com.saucelabs.mydemoapp.android"

    # --- iOS (local) -----------------------------------------------------
    ios_device_name: str = "iPhone 15"
    ios_platform_version: str | None = None
    ios_app_path: Path = Path("apps/ios-mydemoapp.zip")
    ios_bundle_id: str = "com.saucelabs.mydemo.app.ios"

    # --- BrowserStack ----------------------------------------------------
    browserstack_username: str | None = None
    browserstack_access_key: SecretStr | None = None
    browserstack_app_url: str | None = None  # e.g. bs://<app-id>
    browserstack_device_name: str = "Google Pixel 8"
    browserstack_platform_version: str = "14.0"

    # --- Sauce Labs ------------------------------------------------------
    saucelabs_username: str | None = None
    saucelabs_access_key: SecretStr | None = None
    saucelabs_app: str | None = None  # e.g. storage:filename=app.apk
    saucelabs_region: str = "eu-central-1"
    saucelabs_device_name: str = "Google Pixel 8 GoogleAPI Emulator"
    saucelabs_platform_version: str = "14.0"

    # --- Observability ---------------------------------------------------
    record_video: bool = True
    video_time_limit_seconds: int = 180

    # --- Validation ------------------------------------------------------
    @model_validator(mode="after")
    def _validate_cloud_credentials(self) -> Self:
        required: dict[str, object] = {}
        if self.execution_mode is ExecutionMode.BROWSERSTACK:
            required = {
                "BROWSERSTACK_USERNAME": self.browserstack_username,
                "BROWSERSTACK_ACCESS_KEY": self.browserstack_access_key,
                "BROWSERSTACK_APP_URL": self.browserstack_app_url,
            }
        elif self.execution_mode is ExecutionMode.SAUCELABS:
            required = {
                "SAUCELABS_USERNAME": self.saucelabs_username,
                "SAUCELABS_ACCESS_KEY": self.saucelabs_access_key,
                "SAUCELABS_APP": self.saucelabs_app,
            }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ValueError(
                f"Missing variables for mode '{self.execution_mode}': "
                f"{', '.join(missing)}"
            )
        return self

    # --- Derived values --------------------------------------------------
    @property
    def is_cloud(self) -> bool:
        return self.execution_mode is not ExecutionMode.LOCAL

    @property
    def is_android(self) -> bool:
        return self.platform is Platform.ANDROID

    @property
    def remote_url(self) -> str:
        """Appium endpoint (credentials are passed via capabilities, not the URL)."""
        match self.execution_mode:
            case ExecutionMode.BROWSERSTACK:
                return "https://hub-cloud.browserstack.com/wd/hub"
            case ExecutionMode.SAUCELABS:
                return (
                    f"https://ondemand.{self.saucelabs_region}.saucelabs.com:443/wd/hub"
                )
            case _:
                return self.appium_server_url

    @property
    def local_app_path(self) -> Path:
        """Absolute path of the local app binary for the selected platform."""
        path = self.android_app_path if self.is_android else self.ios_app_path
        return path if path.is_absolute() else ROOT_DIR / path


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance (one per process / xdist worker)."""
    return Settings()
