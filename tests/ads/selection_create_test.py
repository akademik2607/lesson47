import pytest


@pytest.mark.django_db
def test_selection_create(client, advertisement, user, user_token):
    expected_result = {
        'id': 1,
        'items': [advertisement.pk],
        'name': 'test_selection'
    }

    data = {
        'items': [advertisement.pk],
        'owner': user,
        'name': 'test_selection'
    }

    response = client.post(
        '/selection/',
        data,
        format='json',
        HTTP_AUTHORIZATION=f'Bearer {user_token}'
    )

    assert response.status_code == 201
    assert response.data == expected_result