from http import HTTPStatus


def test_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola, Mundo!'}


# ! aula 02 exerc 01
def test_html(client):
    response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert 'Ola Mundo' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'james',
            'email': 'james@mail.com',
            'password': '12345',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'james',
        'email': 'james@mail.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'username': 'james', 'email': 'james@mail.com', 'id': 1}]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'thiago',
            'email': 'thiago@mail.com',
            'password': '12345',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'thiago',
        'email': 'thiago@mail.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
