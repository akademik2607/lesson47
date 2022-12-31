from datetime import datetime

from django.utils.deconstruct import deconstructible
from rest_framework.exceptions import ValidationError


@deconstructible
class UserAgeValidator:
    def __init__(self, min_age):
        self.min_age = min_age

    def __call__(self, value):
        birth_year = datetime.strptime(value, '%Y-%m-%d').year
        age = datetime.now().year
        if age - birth_year < age:
            raise ValidationError('the age is too small')


@deconstructible
class IsBlockedDomain:
    def __init__(self, *blocked_domains):
        self.blocked_domains = blocked_domains

    def __call__(self, value):
        for domain in self.blocked_domains:
            if value.endswith(domain):
                raise ValidationError('this domain is banned')
