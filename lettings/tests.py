import pytest
from django.urls import reverse

from lettings.models import Address, Letting


@pytest.fixture
def letting(db):
    address = Address.objects.create(
        number=42,
        street='Main Street',
        city='Springfield',
        state='CA',
        zip_code=90210,
        country_iso_code='USA',
    )
    return Letting.objects.create(title='Sunny Loft', address=address)


def test_lettings_index(client, letting):
    url = reverse('lettings:index')
    response = client.get(url)

    content = response.content.decode()
    assert response.status_code == 200
    assert '<title>Lettings</title>' in content
    assert 'Sunny Loft' in content


def test_letting_detail(client, letting):
    url = reverse('lettings:letting', kwargs={'letting_id': letting.id})
    response = client.get(url)

    content = response.content.decode()
    assert response.status_code == 200
    assert '<title>Sunny Loft</title>' in content
    assert 'Main Street' in content
