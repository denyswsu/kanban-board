from django.contrib import admin

from boards.models import Board, Column


class ColumnInline(admin.TabularInline):
    model = Column


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "owner")
    inlines = [ColumnInline]


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "board", "order")
    list_filter = ("board",)
