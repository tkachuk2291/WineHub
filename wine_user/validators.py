import re

from django.core.exceptions import ValidationError


def validate_first_last_name(value, field_name, error):
    allowed_pattern = re.compile(r"^[a-zA-Z0-9 '-]*$")
    if value[0:1] == "." or value[0:1] == ".":
        raise error(f"{field_name} '{value}' must not begin with dote",
                    )
    if value[0:1] == "." or value[-1:] == ".":
        raise error(f"{field_name} '{value}' must not end with dote",
                    )
    if not allowed_pattern.match(value):
        raise error(f"{field_name} '{value}' must have only special characters(',space hyphen," ")")

    if len(value) < 1:
        raise error(f"{field_name} '{value}' must have one and more chars")


def validate_first_name(value):
    validate_first_last_name(value, field_name="first_name", error=ValidationError, validation_type="model")


def validate_last_name(value):
    validate_first_last_name(value, field_name="last_name", error=ValidationError)


def validate_age(value):
    if value < 21:
        raise ValidationError(f'{value} should be 21 and more')


def password_validate(password):
    if not any(char.isupper() for char in password):
        raise ValidationError(f"'{password}' must have uppercase Latin characters",
                              params={"value": password},
                              )
    if not any(char.islower() for char in password):
        raise ValidationError(f"'{password}' must have low case Latin characters",
                              params={"value": password})
    if not any(char in ["'", "-", "!", "?", "*", ".", "@"] for char in password):
        raise ValidationError(f"'{password}' must have special characters [',!,?,*,hyphen,dot,@)",
                              params={"value": password})
    if not re.findall(r'\d+', password):
        raise ValidationError(f"'{password}' must have digits )",
                              params={"value": password})
    if len(password) < 6:
        raise ValidationError(f"'{password}' must have six and more chars")


def email_validate(value):
    allowed_pattern = re.compile(r"^[a-zA-Z0-9'!?*()-@.]*$")

    if not allowed_pattern.match(value):
        raise ValidationError(f"'{value}' must have only special characters[' ! ? * () hyphen]")

    if value[0:1] == "." or value[0:1] == ".":
        raise ValidationError(f"'{value}' must not begin with dote",
                              )
    if value[0:1] == "." or value[-1:] == ".":
        raise ValidationError(f"'{value}' must not end with dote")
    email_local_part = value.split('@')[0]
    email_domain_part = value.split('@')[1]
    if len(email_local_part) < 3:
        raise ValidationError(f"'local part {email_local_part}' must be 3 and more chars")
    if len(value.split('@')[0]) > 15:
        raise ValidationError(
            f"'local part {email_local_part}' must be 15 characters or less ,current length: {len(email_local_part)}")
    if len(email_domain_part) < 3:
        raise ValidationError(f"'domain part {email_local_part}' must be 3 and more chars")
    if len(email_domain_part) > 10:
        raise ValidationError(
            f"'domain part {value.split('@')[0]}' must be 10 characters or less ,current length: {len(email_local_part)}")
