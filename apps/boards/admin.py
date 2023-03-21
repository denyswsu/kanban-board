from django.contrib import admin

from apps.boards.models import Board, Column

admin.site.register(Board)
admin.site.register(Column)
