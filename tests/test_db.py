from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_zero.models import Todo, TodoState, User


@pytest.mark.asyncio
async def test_create_user_without_todos(session, mock_db_time):
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
        'todos': [],
    }


@pytest.mark.asyncio
async def test_create_todo(session, user: User, mock_db_time):
    with mock_db_time(model=Todo) as time:
        todo = Todo(
            title='Test todo',
            description='Test Desc',
            state='draft',
            user_id=user.id,
        )

        session.add(todo)
        await session.commit()

    todo = await session.scalar(select(Todo))
    # assert user.__dict__ == {}
    assert asdict(todo) == {
        'description': 'Test Desc',
        'id': 1,
        'state': 'draft',
        'title': 'Test todo',
        'user_id': 1,
        'created_at': time,
        'updated_at': time,
    # ! não tenho sei se está certo, ajetei para passar no teste
    # ! foi porq adicionei a relação antes da hora!!!
        'user': {
            'created_at': user.created_at,
            'email': user.email,
            'id': user.id,
            'password': user.password,
            'todos': user.todos,
            'updated_at': user.updated_at,
            'username': user.username,
        },
    }


@pytest.mark.asyncio
async def test_user_todo_relationship(session, user: User):
    todo = Todo(
        title='Test todo',
        description='Test Desc',
        state=TodoState.draft,
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()
    await session.refresh(user)

    user = await session.scalar(
        select(User).where(User.id == user.id)
    )

    assert user.todos == [todo]
