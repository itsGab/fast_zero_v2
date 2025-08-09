from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola, Mundo!'}


# read html (a2e1)
def test_html(client):
    response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert 'Ola Mundo' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'user_created',
            'email': 'user_created@mail.com',
            'password': 'user_created_pwd',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'user_created',
        'email': 'user_created@mail.com',
        'id': 1,
    }


def test_create_user_username_conflict(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,  # duplicated
            'email': 'user_created@mail.com',
            'password': 'user_created_pwd',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_conflict(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'user_created',
            'email': user.email,  # duplicated
            'password': 'user_created_pwd',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users_no_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'user_updated',
            'email': 'user_updated@mail.com',
            'password': 'user_updated_pwd',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'user_updated',
        'email': 'user_updated@mail.com',
        'id': user.id,
    }


def test_update_integrity_error(client, user, token):
    client.post(
        '/users',
        json={
            'username': 'integrity',
            'email': 'integrity@mail.com',
            'password': 'integrity_pwd',
        },
    )
    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'integrity',
            'email': 'test_user@mail.com',
            'password': 'test_user_pwd',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


# exercicio: user by id (a3e3)
def test_read_user_by_id(client, user, token):
    response = client.get(
        f'/user/{user.id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'test_user',
        'email': 'test_user@mail.com',
        'id': user.id,
    }


def test_read_user_by_id_not_found(client, user):
    response = client.get('/user/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


# TODO: test update user NOT ENOUGH PERMISSIONS
# TODO: test delete user NOT ENOUGH PERMISSIONS
# TODO: test login for access token UNAUTHORIZED incorrect email
# TODO: test login for access token UNAUTHORIZED incorrect password
