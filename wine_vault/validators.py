import re

from rest_framework.exceptions import ValidationError


def validate_wine_name(value):
    allowed_pattern = re.compile(r"^[a-zA-Z0-9 '-]*$")
    if not allowed_pattern.match(value):
        raise ValidationError(f"'{value}' must have only special characters(',space hyphen)")

    if value[0:1] == "." or value[0:1] == ".":
        raise ValidationError(f"'{value}' must not begin with dote", )
    if value[0:1] == "." or value[-1:] == ".":
        raise ValidationError(f"'{value}' must not end with dote")
    if len(value) < 3:
        raise ValidationError(f"'{value}' must have at least 3 characters")
    if not re.match(r'^[a-zA-Z]', value):
        raise ValidationError('The value must start with a letter.')

def validate_wine_vintage(value):
    if not re.findall(r'\d+', value):
        raise ValidationError(f"'{value}' must have digits )")

    if len(value) < 4:
        raise ValidationError(f"'{value}' must have at least 4 characters")
