from http import HTTPStatus

from jwt import decode

from fast_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1',
        headers={
            'Authorization': 'Bearer token-invalido'
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'Could not validate credentials'
    }


# TODO: test get current user UNAUTHORIZED no email (a6e1)
# TODO: test get current user UNAUTHORIZED no user (a6e2)
