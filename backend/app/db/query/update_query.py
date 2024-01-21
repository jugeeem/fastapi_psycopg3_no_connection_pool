class UpdateQuery:
    UPDATE_TODO_TASK_BY_ID = """
        UPDATE todo.task
        SET
            title = %s
            ,description = %s
        WHERE id = %s
    """


update_query = UpdateQuery()
