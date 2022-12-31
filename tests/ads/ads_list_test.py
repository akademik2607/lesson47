from collections import OrderedDict

import pytest

from ads.serializers import AdvertisementSerializer
from tests.factories import AdvertisementFactory


@pytest.mark.django_db
def test_ads_list(client, user_token):

    ads = AdvertisementFactory.create_batch(2)
    expected_result = OrderedDict([
        ("count", 2),
        ("next", None),
        ("previous", None),
        ("results", AdvertisementSerializer(ads, many=True).data)
    ])

    responce = client.get(
        '/ads/',
        format='json',
        HTTP_AUTHORIZATION=f'Bearer {user_token}'
    )

    assert responce.status_code == 200
    assert responce.data == expected_result
