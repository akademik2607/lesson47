import factory
import pytest
from django.contrib.auth.hashers import make_password

from tests.factories import UserFactory


@pytest.fixture
@pytest.mark.django_db
def user_token(client, user, django_user_model):
    data = {
        "username": user.username,
        "password": "test_password",
    }

    response = client.post(
        "/user/token/",
        data=data,
        format='json'
    )

    return response.data["access"]
