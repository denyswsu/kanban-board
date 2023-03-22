from django.db import transaction
from rest_framework import serializers

from boards.constants import DEFAULT_BOARD_COLUMNS
from boards.models import Board
from boards.serializers.column_serializers import ColumnSerializer
from users.serializers import UserSerializer


class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, required=False)
    owner = UserSerializer()

    class Meta:
        model = Board
        fields = ("id", "name", "description", "owner", "columns")


class CreateBoardSerializer(BoardSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    with_default_columns = serializers.BooleanField(default=True, write_only=True)

    class Meta:
        model = Board
        fields = ("id", "name", "description", "owner", "columns", "with_default_columns")
        read_only_fields = ("id", "columns", "owner")

    @transaction.atomic
    def create(self, validated_data):
        with_default_columns = validated_data.pop("with_default_columns")
        board = Board.objects.create(**validated_data)
        if with_default_columns:
            self._create_default_columns(board)
        return board

    @staticmethod
    def _create_default_columns(board):
        for column_data in DEFAULT_BOARD_COLUMNS:
            board.columns.create(**column_data)
