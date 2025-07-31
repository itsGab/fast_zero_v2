from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola, Mundo!'}


# ! aula 02 exerc 01
def test_html():
    client = TestClient(app)
    response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert 'Ola Mundo' in response.text
