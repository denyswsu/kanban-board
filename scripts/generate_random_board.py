import random
from uuid import uuid4

from django.contrib.auth import get_user_model

from boards.models import Board, Column
from tasks.models import Task


User = get_user_model()


def generate_random_board():
    username = f"user_<{str(uuid4())[:30]}>"
    owner = User.objects.create_user(
        username=f"user_<{username}>", email=f"user_<{username}>@example.com"
    )
    board = Board(name=f"Random Board <{uuid4()}>", owner=owner)
    board.save()
    generate_random_columns(board)


def generate_random_columns(board):
    for i in range(random.randint(1, 5)):
        column = Column(name=f"Random Column <{str(uuid4())[:10]}>", board=board, order=i)
        column.save()
        generate_random_tasks(column, board.owner)


def generate_random_tasks(column, owner):
    for j in range(random.randint(1, 7)):
        task = Task(
            name=f"Random Task <{str(uuid4())[:20]}>",
            description=f"Random Description: \n{uuid4()}",
            column=column,
            board=column.board,
            order=j,
            owner=owner,
        )
        username = f"user_<{str(uuid4())[:30]}>"
        task.assigned_to = User.objects.create_user(
            username=f"user_<{username}>", email=f"user_<{username}>@example.com"
        ) if j % 2 == 0 else owner
        task.save()


def run():
    generate_random_board()
