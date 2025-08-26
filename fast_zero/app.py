from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routers import auth, users
from fast_zero.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'Ola, Mundo!'}


# read html (a2e1)
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
