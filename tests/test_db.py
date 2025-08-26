from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='walter', password='12345', email='walt@mail.com'
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'walter'))

    assert asdict(user) == {
        'id': 1,
        'username': 'walter',
        'password': '12345',
        'email': 'walt@mail.com',
        'created_at': time,
        # aula 4 exerc 2
        'updated_at': time,
    }
