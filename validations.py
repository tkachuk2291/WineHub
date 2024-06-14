import re

from django.core.exceptions import ValidationError


def validate_first_last_name(value, field_name, error, validation_type="model"):
    if not any(char.isupper() for char in value):
        raise error(f"{field_name} '{value}' must have uppercase Latin characters",
                    )
    if not any(char.islower() for char in value):
        raise error(f"{field_name} '{value}' must have low case Latin characters",
                    )
    if value[0:1] == "." or value[0:1] == ".":
        raise error(f"{field_name} '{value}' must not begin with dote",
                    )
    if value[0:1] == "." or value[-1:] == ".":
        raise error(f"{field_name} '{value}' must not end with dote",
                    )
    if not any(char in ["'", "-"] for char in value):
        raise error(f"{field_name} '{value}' must have special characters(', space hyphen)",

                    )
    if not re.findall(r'\d+', value):
        raise error(f"{field_name} '{value}' must have digits) , in {validation_type}",
                    )
    if len(value) < 1:
        raise error(f"{field_name} '{value}' must have one and more chars")

    if value[0] in ["'", "-"]:
        raise ValidationError(f"{field_name} '{value}'  must not be a special character")


def validate_first_name(value):
    validate_first_last_name(value, field_name="first_name", error=ValidationError)


def validate_last_name(value):
    validate_first_last_name(value, field_name="last_name", error=ValidationError)


def validate_age(value):
    if value < 21:
        raise ValidationError(f'{value} should be 21 and more')


def validate_password(value):
    if not any(char.isupper() for char in value):
        raise ValidationError(f"'{value}' must have uppercase Latin characters",
                              params={"value": value},
                              )
    if not any(char.islower() for char in value):
        raise ValidationError(f"'{value}' must have low case Latin characters",
                              params={"value": value})
    if not any(char in ["'", "-", "!", "?", "*", ".", "@"] for char in value):
        raise ValidationError(f"'{value}' must have special characters [',!,?,*,hyphen,dot,@)",
                              params={"value": value})
    if not re.findall(r'\d+', value):
        raise ValidationError(f"'{value}' must have digits )",
                              params={"value": value})
    if len(value) < 6:
        raise ValidationError(f"'{value}' must have six and more chars")
