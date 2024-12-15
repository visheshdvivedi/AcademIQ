import re
from typing import List
from models import User

NAME_MIN_LENGTH = 3
NAME_MAX_LENGTH = 255
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 255

def validate_name(attribute: str, value: str) -> List[str]:
    errors = []

    # validate name length
    if len(value) < NAME_MIN_LENGTH:
        errors.append(f"'{attribute}' must be at least {NAME_MIN_LENGTH} characters long")
    elif len(value) > NAME_MAX_LENGTH:
        errors.append(f"'{attribute}' length cannot be more than {NAME_MAX_LENGTH} characters.")

    return errors

def validate_email_address(value: str) -> List[str]:
    errors = []

    # validate email length
    if len(value) < NAME_MIN_LENGTH:
        errors.append(f"'email' must be at least {NAME_MIN_LENGTH} characters long")
    elif len(value) > NAME_MAX_LENGTH:
        errors.append(f"'email' length cannot be more than {NAME_MAX_LENGTH} characters.")

    # validate email format
    if not re.match(EMAIL_REGEX, value):
        errors.append(f"Invalid email address format")

    return errors

def validate_password(value: str) -> List[str]:
    errors = []

    # validate password length
    if len(value) < PASSWORD_MIN_LENGTH:
        errors.append(f"'password' must be at least {PASSWORD_MIN_LENGTH} characters long")
    elif len(value) > PASSWORD_MAX_LENGTH:
        errors.append(f"'password' length cannot be more than {PASSWORD_MAX_LENGTH} characters.")

    # validate password strength
    has_upper = False
    has_lower = False
    has_num = False
    has_special = False

    for char in value:
        if char.isdigit():
            has_num = True
        elif char.isalpha():
            if char.islower(): has_lower = True
            elif char.isupper(): has_upper = True
        else:
            has_special = True

    if not has_lower:
        errors.append("Password must have at least on lowercase character.")
    if not has_upper:
        errors.append("Password must have at least one uppercase character.")
    if not has_num:
        errors.append("Password must have at least on number.")
    if not has_special:
        errors.append("Password must have at least one special character.")

    return errors