from typing import List

def validate_password_strength(password: str) -> List[str]:
    errors = []
    has_lower = has_upper = has_digit = has_special_char = False

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        else:
            has_special_char = True

    if not has_lower:
        errors.append("Password must have at least one lowercase character")
    if not has_upper:
        errors.append("Password must have at least one uppercase character")
    if not has_digit:
        errors.append("Password must have at least one digit")
    if not has_special_char:
        errors.append("Password must have at least one special character")

    return errors