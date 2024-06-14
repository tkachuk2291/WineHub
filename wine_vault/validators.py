import re

from rest_framework.exceptions import ValidationError


def validate_wine_name(value):
    if not any(char.isupper() for char in value):
        raise ValidationError(f"'{value}' must have uppercase Latin characters",
                              )
    if not any(char.islower() for char in value):
        raise ValidationError(f"'{value}' must have low case Latin characters")

    if value[0:1] == "." or value[0:1] == ".":
        raise ValidationError(f"'{value}' must not begin with dote",
                              )
    if value[0:1] == "." or value[-1:] == ".":
        raise ValidationError(f"'{value}' must not end with dote")
    if not re.findall(r'\d+', value):
        raise ValidationError(f"'{value}' must have digits )")
    if not any(char in ["'", "-"] for char in value):
        raise ValidationError(f"'{value}' must have special characters [',-]")
    if len(value) < 3:
        raise ValidationError(f"'{value}' must have at least 3 characters")
    if not re.match(r'^[a-zA-Z]', value):
        raise ValidationError('The value must start with a letter.')


def validate_wine_vintage(value):
    if not re.findall(r'\d+', value):
        raise ValidationError(f"'{value}' must have digits )")

    if len(value) < 4:
        raise ValidationError(f"'{value}' must have at least 4 characters")