DEFAULT_BOARD_TITLES = ["Backlog", "To Do", "In Progress", "Done"]
COMPLETED_COLUMN_NAMES = ["Done", "Completed", "Closed"]
DEFAULT_BOARD_COLUMNS = [
    {
        "name": name,
        "order": i,
        "description": name,
        "is_completed_column": name in COMPLETED_COLUMN_NAMES,
    } for i, name in enumerate(DEFAULT_BOARD_TITLES)
]
