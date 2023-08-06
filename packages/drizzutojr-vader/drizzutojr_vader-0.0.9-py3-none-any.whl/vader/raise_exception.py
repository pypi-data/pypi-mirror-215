import re
import semver

from .external import *
from .general import *
from .exceptions import *

MIN_DESCRIPTION_LENGTH = 20
MAX_DESCRIPTION_LENGTH = 100


def raise_exception_invalid_email(email: str):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if not re.fullmatch(regex, email):
        raise VaderConfigError(f"Email is not a valid email: {email}")


def raise_exception_invalid_description(
    description: str,
    min_length: int = MIN_DESCRIPTION_LENGTH,
    max_length: int = MAX_DESCRIPTION_LENGTH,
):
    if len(description) < min_length:
        raise VaderConfigError(f"Description may not be under {min_length} characters")

    if len(description) > max_length:
        raise VaderConfigError(f"Description may not be over {max_length} characters")


def raise_exception_invalid_version(version):
    if not semver.VersionInfo.is_valid(version):
        raise VaderConfigError(f"Version number is not a valid version: {version}")


def raise_exception_username_does_not_exist(username):
    if not validate_username_exists(username):
        raise VaderConfigError(f"Username {username} not found")


def raise_exception_email_does_not_exist(email):
    if not validate_email_exists(username):
        raise VaderConfigError(f"Email {email} not found")


def raise_exception_app_id_does_not_exist(app_id):
    if not validate_app_id_exists(app_id):
        raise VaderConfigError(f"App ID {app_id} not found")


def raise_exception_group_does_not_exist(group_name):
    if not validate_group_exists(group_name):
        raise VaderConfigError(f"Group {group_name} not found")


def raise_exception_invalid_min(value_name: str, value: int, min_value: int):
    if min_value and value < min_value:
        raise VaderConfigError(
            f"Value {value} for {value_name} may not be less than {min_value}"
        )


def raise_exception_invalid_max(value_name: str, value: int, max_value: int):
    if max_value and value > max_value:
        raise VaderConfigError(
            f"Value {value} for {value_name} may not be more than {max_value}"
        )


def raise_exception_invalid_option(
    value_name: str, chosen_option: str, available_options: list
):
    if chosen_option not in available_options:
        raise VaderConfigError(
            f"Option {chosen_option} for {value_name} must be one of {', '.join(available_options)}"
        )
