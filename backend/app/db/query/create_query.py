class CreateQuery:
    CREATE_TODO_TASK = """
        INSERT INTO todo.task (
            title
            ,description
        ) VALUES
        (
            %s
            ,%s
        )
    """


create_query = CreateQuery()
