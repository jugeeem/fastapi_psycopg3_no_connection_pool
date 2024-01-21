class ReadQuery:
    READ_ALL_TODO_TASK = """
        SELECT
            id
            ,title
            ,description
        FROM todo.task
    """

    READ_TODO_TASK_BY_ID = """
        SELECT
            id
            ,title
            ,description
        FROM todo.task
        WHERE id = %s
    """


read_query = ReadQuery()
