from rest_framework import serializers

from apps.boards.models import Column


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ("id", "name", "board", "order")
