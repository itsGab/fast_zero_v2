from http import HTTPStatus


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
