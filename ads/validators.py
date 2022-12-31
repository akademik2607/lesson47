from django.utils.deconstruct import deconstructible
from rest_framework.exceptions import ValidationError


@deconstructible
class MinLengthValidator:
    def __init__(self, length):
        self.length = length

    def __call__(self, value):
        if len(value) < self.length:
            raise ValidationError('string is a too small')


def is_false_validator(value):
    if value is not False:
        raise ValidationError('value is not False')

