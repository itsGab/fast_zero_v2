from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Ola, Mundo!'}


# ! aula 02 exerc 01
@app.get('/html', response_class=HTMLResponse, deprecated=True)
def read_html():
    return """
    <html>
      <head>
        <title> Nosso ola mundo!</title>
      </head>
      <body>
        <h1> Ola Mundo </h1>
      </body>
    </html>"""
