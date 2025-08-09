from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User

SECRET_KEY = 'your-secret-key'  # provisorio
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = PasswordHash.recommended()

oath2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict):  # define funcao
    to_encode = data.copy()  # cria um copia do dados para encodar
    # define o tempo de expiracao
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # adiciona o horario de expiracao no payload
    to_encode.update({'exp': expire})
    # cria o json web token
    encoded_jwt = encode(
        payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt  # retorno jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plaint_password: str, hashed_password: str):
    return pwd_context.verify(plaint_password, hashed_password)


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oath2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        subject_email = payload.get('sub')

        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == subject_email))

    if not user:
        raise credentials_exception

    return user
