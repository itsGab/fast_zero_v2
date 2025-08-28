from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


# test login for access token UNAUTHORIZED incorrect email
def test_login_token_unauthorized_incorrect_email(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': 'incorrect@mail.com',
            'password': user.clean_password,
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


# test login for access token UNAUTHORIZED incorrect password
def test_login_token_unauthorized_incorrect_password(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': 'incorrect_pwd',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_expired_after_time(client, user):
    with freeze_time('2025-01-01 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2025-01-01 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'}
        )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_inexistent_user(client):
    response = client.post(
        '/auth/token',
        data={'username': 'no_user@email.com', 'password': 'pwd_test'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_wrong_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'pwd_wrong'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client, user, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2025-01-01 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password}
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2025-01-01 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


# * bonus: teste para ver se o token atualizado esta funcionando!
def test_refreshed_token_works(client, user, token):
    with freeze_time('2025-01-01 12:00:00'):
        response = client.post(
            '/auth/token',
            data={
                'username': user.email,
                'password': user.clean_password},
        )
        assert 'access_token' in response.json()
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2025-01-01 12:25:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert 'access_token' in response.json()
        assert response.status_code == HTTPStatus.OK
        token_refreshed = response.json()['access_token']

    with freeze_time('2025-01-01 12:35:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token_refreshed}'},
            json={
                'username': user.username,
                'email': 'update@mail.com',
                'password': user.clean_password,
            }
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            'username': user.username,
            'email': 'update@mail.com',
            'id': user.id
        }
