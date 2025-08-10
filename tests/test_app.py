from http import HTTPStatus


def test_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Ola, Mundo!'}


# read html (a2e1)
def test_html(client):
    response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert 'Ola Mundo' in response.text
