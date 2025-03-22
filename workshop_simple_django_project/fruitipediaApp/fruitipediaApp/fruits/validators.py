from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class AlphaValidator:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, value: str):
        for char in value:
            if not char.isalpha():
                raise ValidationError(self.message)