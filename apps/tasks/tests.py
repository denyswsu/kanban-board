from django.test import TestCase
from model_bakery import baker

from boards.constants import DEFAULT_BOARD_COLUMNS
from tasks.services import TaskService


class TaskServiceTestCase(TestCase):

    def setUp(self) -> None:
        self.board = baker.make('boards.Board')
        for column_data in DEFAULT_BOARD_COLUMNS:
            self.board.columns.create(**column_data)

        self.first_column = self.board.columns.all()[0]
        self.first_column_task_count = 5
        for i in range(self.first_column_task_count):
            self.first_column.tasks.create(name=f"Task {i}", board=self.board, order=i)
        self.first_col_movable_task = self.first_column.tasks.all()[0]

        self.second_column = self.board.columns.all()[1]
        self.second_col_movable_task = self.second_column.tasks.create(name=f"Move Me", board=self.board)

    def test_get_new_column_order(self):
        expected_columns_count = len(DEFAULT_BOARD_COLUMNS)
        self.assertEqual(self.board.get_new_column_order(), expected_columns_count)

    def test_get_last_column_order(self):
        expected_last_column_order = len(DEFAULT_BOARD_COLUMNS) - 1
        self.assertEqual(self.board.get_last_column_order(), expected_last_column_order)

    def test_move_task_to_another_column_scenario1(self):
        task_service = TaskService(self.second_col_movable_task)
        task_service.move_task(new_order=0, column=self.first_column, save=True)

        self.assertEqual(self.second_col_movable_task.column, self.first_column)
        self.assertEqual(self.second_col_movable_task.order, 0)

        self.assertEqual(self.first_column.tasks.count(), self.first_column_task_count + 1)
        self.assertEqual(self.second_column.tasks.count(), 0)

    def test_move_task_to_another_column_scenario2(self):
        task_service = TaskService(self.second_col_movable_task)
        task_service.move_task(new_order=3, column=self.first_column, save=True)

        self.assertEqual(self.second_col_movable_task.column, self.first_column)
        self.assertEqual(self.second_col_movable_task.order, 3)

        self.assertEqual(self.first_column.tasks.count(), self.first_column_task_count + 1)
        self.assertEqual(self.second_column.tasks.count(), 0)

    def test_move_task_within_column_scenario1(self):
        task_service = TaskService(self.first_col_movable_task)
        task_service.move_task(new_order=3, column=self.first_column, save=True)

        self.assertEqual(self.first_col_movable_task.column, self.first_column)
        self.assertEqual(self.first_col_movable_task.order, 3)

        self.assertEqual(self.first_column.tasks.count(), self.first_column_task_count)
        self.assertEqual(self.second_column.tasks.count(), 1)

