import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from profiles.models import Profile


@pytest.fixture
def profile(db):
    user = User.objects.create_user(
        username='PatrickEwing',
        password='testpass123',
        first_name='Patrick',
        last_name='Ewing',
        email='patrick.ewing@example.com',
    )
    return Profile.objects.create(user=user, favorite_city='New York')


def test_profiles_index(client, profile):
    url = reverse('profiles:index')
    response = client.get(url)

    content = response.content.decode()
    assert response.status_code == 200
    assert '<title>Profiles</title>' in content
    assert 'PatrickEwing' in content


def test_profile_detail(client, profile):
    url = reverse('profiles:profile', kwargs={'username': 'PatrickEwing'})
    response = client.get(url)

    content = response.content.decode()
    assert response.status_code == 200
    assert '<title>PatrickEwing</title>' in content
    assert 'Patrick' in content
    assert 'Ewing' in content
    assert 'New York' in content
