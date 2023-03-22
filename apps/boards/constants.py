DEFAULT_BOARD_TITLES = ["Backlog", "To Do", "In Progress", "Done"]
DEFAULT_BOARD_COLUMNS = [
    {
        "name": name,
        "order": i,
        "description": name
    } for i, name in enumerate(DEFAULT_BOARD_TITLES)
]
