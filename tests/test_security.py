from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token, settings


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(
        jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


# test get current user UNAUTHORIZED no email (a6e1)
def test_get_current_user_no_email(client, user):
    data = {'no-email': 'test@mail.com'}
    token = create_access_token(data)
    response = client.delete(
        f'/users/{user.id}',  # para usar um id que exista
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


# test get current user UNAUTHORIZED no user (a6e2)
def test_get_current_user_no_user(client, user):
    data = {'sub': 'test@mail.com'}
    token = create_access_token(data)

    response = client.delete(
        f'/users/{user.id}',  # para usar um id que exista
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
