class DeleteQuery:
    DELETE_TODO_TASK_BY_ID = """
        DELETE FROM todo.task
        WHERE id = %s
    """


delete_query = DeleteQuery()
