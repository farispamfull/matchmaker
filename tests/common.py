from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def create_users_api(user_client):
    data = {
        'first_name': 'TestUser1234',
        'last_name': 'Testlastname',
        'role': 'user',
        'email': 'testuser@matchmaker.fake'
    }
    user_client.post('/api/v1/users/', data=data)
    user = get_user_model().objects.get(username=data['username'])
    data = {
        'first_name': 'fsdfsdf',
        'last_name': 'dsgdsfg',
        'username': 'TestUser4321',
        'gender': 'male',
        'role': 'moderator',
        'email': 'testuser2342@matchmaker.fake'
    }
    user_client.post('/api/v1/users/', data=data)
    moderator = get_user_model().objects.get(username=data['username'])
    return user, moderator


def auth_client(user):
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client
