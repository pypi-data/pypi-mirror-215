import re
import semver

from .consts import *
from .external import *
from .general import *
from .exceptions import *


def raise_exception_invalid_email(email: str):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if not re.fullmatch(regex, email):
        raise VaderConfigError(f"Email is not a valid email: {email}")


def raise_exception_invalid_description(
    description: str,
    min_length: int = MIN_STRING_LENGTH,
    max_length: int = MAX_STRING_LENGTH,
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


def raise_exception_invalid_cidr_blocks(
    app_id: str,
    boundary_id: str,
    value_name: str,
    cidr_blocks: list,
    blacklist: list = [],
):
    errors = []
    cidr_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}$"

    if len(blacklist) == 0:
        blacklist = DEFAULT_INVALID_TOKEN_BOUND_CIDRS

    if len(cidr_blocks) < DEFAULT_MIN_TOKEN_BOUND_CIDRS:
        errors.append(
            f"CIDR Block list length is less than {DEFAULT_MIN_TOKEN_BOUND_CIDRS}"
        )
    elif len(cidr_blocks) > DEFAULT_MAX_TOKEN_BOUND_CIDRS:
        errors.append(
            f"CIDR Block list length is greater than {DEFAULT_MAX_TOKEN_BOUND_CIDRS}"
        )
    else:
        for cidr in cidr_blocks:
            if not re.match(cidr_pattern, cidr):
                errors.append(f"CIDR {cidr} is not valid CIDR notation")
            for bad_cidr in blacklist:
                if cidr.startswith(bad_cidr):
                    errors.append(
                        f"CIDR {cidr} is not allowed per the black list: {', '.join(blacklist)}"
                    )
            if not validate_cidr_block_owner(app_id, boundary_id, cidr):
                errors.append(
                    f"CIDR {cidr} is not authroized for {generate_project_name(app_id, boundary_id)}"
                )

    if len(errors) > 0:
        raise VaderConfigError(
            f"Invalid CIDR configuration in {value_name}", details=errors
        )
