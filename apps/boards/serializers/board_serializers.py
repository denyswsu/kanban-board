from rest_framework import serializers

from boards.models import Board
from boards.serializers.column_serializers import ColumnSerializer
from users.serializers import UserSerializer


class BoardSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True)
    owner = UserSerializer()

    class Meta:
        model = Board
        fields = ("id", "name", "description", "owner", "columns")
