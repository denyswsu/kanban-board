from rest_framework import serializers

from apps.boards.models import Board
from apps.boards.serializers.column_serializers import ColumnSerializer


class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True)

    class Meta:
        model = Board
        fields = ("id", "name", "description", "owner", "columns")
