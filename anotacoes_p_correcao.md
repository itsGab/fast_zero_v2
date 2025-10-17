# notas de possiveis correcoes nas aulas

## aula 3 

3.1. na implementando a rota get, segunda imagem de codigo, o highlight esta errado. esta em userdb e deveria estar em userlist

## aula 4 

4.1. erro em "Session(engine): cria uma sessão Session para que os testes possam se comunicar com o banco de dadosvia engine."

4.2. ...á executado durante o teste que faça ***que com*** os registros inseridos...
Substituir por: ***com que*** ???

## aula 7

7.1.annotated antes da hora?

o annotated apareceu no código sem uma apresentação? é proposital? especificamente na parte da aplicacao do router de auth.

> fast_zero/routers/auth.py

```from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Token
from fast_zero.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])

# ! ----------------------- aqui --------------------------- #
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token)
def login_for_access...[continua]
```

7.2. Antecipar plug das rotas no app

A parte "plugando as rotas em app" não ficaria melhor no começo da aula? No meu caso gosto de ir rodando o código, conforme a aula vai progredindo, e quando estava definindo as rotas, não aparecia no Swagger e até cogitei estar fazendo algo errado. Apenas uma reflexão minha e sugestão, caso faça sentido.

7.3. Imagens 'swagger tags', para ficar igual a imagem, a tag do auth deve ser 'token'. Da seguinte forma:

`router = APIRouter(prefix='/auth', tags=['token'])`


7.4. Subindo fixture de token

Subir a fixture de token, para antes da sugestão de rodar os testes.

texto: "Importante, porém, notar que alguns destes testes usam a fixture token para checar a autorização, como o endpoint do token foi alterado, devemos alterar a fixture de token para que esses testes continuem passando."

## Aula 8

8.1. no seguinte bloco de texto, o termo O/O está certo, ou o correto seria I/O?

> O await é usado para chamar operações que podem levar algum tempo, pelo bloqueio de I/O. Isso permite que o Python "libere" o controle de volta para o loop de eventos, que pode executar outras tarefas enquanto aguarda a operação "espera" a **resposta de O/O** ser concluída:


8.2. possivel erro no codigo, faltou um `{}`

Não sei se o código está realmente errado, mas o pylance estava dando erro antes de colocar o `{}`. No material escrito está sem e no aula em vídeo está com.
```
async def run_async_migrations(): 
    connectable = async_engine_from_config(
        # config.get_section(config.config_ini_section), <- aqui
        config.get_section(config.config_ini_section, {}),  # <- correcao
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
```


## Aula 10

10.1. importado o `TodoUpdate` no codigo de exemplo, mas ainda nao foi declarado no codigo. nessa parte o `Message` importado, tambem nao foi usado no todos.

10.... nos exercicios o ex 7 e 8 deveriam ser extensoes do 6.


## Aula 11

11.1. vale a pena comentar que o `-d` do docker é para _"detached"_???


11.2. sugestao: colocar informacao sobre **chmod** do `entrypoint.sh`


## Aula 13

13.1. nao sei "Ruby on rails" ao inves de "Ruby e rails"???