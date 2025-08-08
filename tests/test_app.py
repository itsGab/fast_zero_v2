from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola, Mundo!'}


# ! aula 02 exerc 01 - inicio
def test_html(client):
    response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert 'Ola Mundo' in response.text


# ! aula 2 exerc 01 - fim


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
        }
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
        }
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


def test_update_user(client, user):
    response = client.put(
        '/users/1',
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
        'id': 1,
    }


def test_update_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'integrity',
            'email': 'integrity@mail.com',
            'password': 'integrity_pwd',
        }
    )
    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'integrity',
            'email': 'test_user@mail.com',
            'password': 'test_user_pwd',
        }
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}

# ! aula 05 exerc 03 - inicio 
# ! aula 03 exerc 01, 02 e 03 - inicio
# 1. test not found put
def test_update_user_not_found(client, user):
    response = client.put(
        '/users/2',
        json={
            'username': 'not_found_user',
            'email': 'not_found_user@mail.com',
            'password': 'not_found_user_pwd',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


# 2. test not found delete
def test_delete_user_not_found(client, user):
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


# 3. test user by id and user user not found by id
# 3.1.user by id
def test_read_user_by_id(client, user):
    response = client.get('/user/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'test_user',
        'email': 'test_user@mail.com',
        'id': 1,
    }


# 3.2. user not found by id
def test_read_user_by_id_not_found(client, user):
    response = client.get('/user/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


# ! aula 03 exerc 01, 02 e 03 - fim
# ! aula 05 exerc 03 - fim
