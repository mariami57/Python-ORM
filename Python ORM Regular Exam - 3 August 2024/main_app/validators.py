from django.utils.deconstruct import deconstructible


@deconstructible
class DigitsOnlyValidator:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, value):
        for char in value:
            if not char.isdigit():
                raise ValueError(self.message)