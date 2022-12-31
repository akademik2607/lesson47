import pytest


@pytest.mark.django_db
def test_ads_retrieve(client, advertisement, user_token):
    expected_result = {
        "id": advertisement.pk,
        "name": advertisement.name,
        "price": advertisement.price,
        "description": advertisement.description,
        "is_published": False,
        "image": None,
        "author": advertisement.author.pk,
        "category": advertisement.category.pk
    }

    result = client.get(
        f'/ads/{advertisement.pk}/',
        HTTP_AUTHORIZATION=f'Bearer {user_token}'
    )

    assert result.status_code == 200
    assert result.data == expected_result
