from http import HTTPStatus

from fast_zero.schemas import UserPublic


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


def test_update_integrity_error(client, user, other_user, token):
    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': other_user.username,  # username duplicado
            'email': user.email,
            'password': user.clean_password,
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
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }
    assert response.status_code == HTTPStatus.OK


def test_read_user_by_id_not_found(client, user):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


# test update user NOT ENOUGH PERMISSIONS
def test_update_user_forbidden(client, user, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': user.username,
            'email': 'updated_email@mail.com',
            'password': user.clean_password,
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


# test delete user NOT ENOUGH PERMISSIONS
def test_delete_user_forbidden(client, user, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
