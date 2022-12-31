import pytest


@pytest.mark.django_db
def test_ads_create(client, user, category, user_token):
    expected_value = {
        "id": 1,
        "is_published": False,
        "name": "Сибирская котята, новые",
        "price": 2500,
        "description": "Продаю сибирских котят,новых.",
        "image": None,
        "author": user.pk,
        "category": 1
    }

    data = {
        "name": "Сибирская котята, новые",
        "author": user.pk,
        "price": 2500,
        "description": "Продаю сибирских котят,новых.",
        "is_published": False,
        "category": category.pk
    }

    response = client.post(
        "/ads/",
        data,
        format='json',
        HTTP_AUTHORIZATION=f'Bearer {user_token}'
    )

    assert response.status_code == 201
    assert expected_value == response.data

