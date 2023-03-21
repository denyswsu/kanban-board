import random
from uuid import uuid4

from django.contrib.auth import get_user_model

from boards.models import Board, Column
from tasks.models import Task


User = get_user_model()


def generate_random_board():
    owner = User.objects.create_user(
        username=f"user_<{uuid4()}>",
        email=f"user_<{uuid4()}>@example.com",
    )

    board = Board(
        name=f"Random Board <{uuid4()}>",
        owner=owner,
    )
    board.save()

    for i in range(random.randint(1, 5)):
        
        column = Column(
            name=str(uuid4())[:7],
            board=board,
            order=i,
        )
        column.save()
        for j in range(random.randint(1, 5)):
            task = Task(
                name=f"Random Task <{uuid4()}>",
                description=f"Random Description <{uuid4()}>",
                column=column,
                board=board,
                order=j,
                owner=owner,
            )
            if j % 2 == 0:
                assigned = owner
            else:
                assigned = User.objects.create_user(
                    username=f"user_<{uuid4()}>",
                    email=f"user_<{uuid4()}>@example.com",
                )


            task.assigned_to = assigned
            task.save()


def run():
    generate_random_board()
