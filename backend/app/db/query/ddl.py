class DDL:
    CREATE_TODO_SCHEMA = """
        CREATE SCHEMA IF NOT EXISTS todo
        AUTHORIZATION postgres;
    """

    CREATE_TASK_TABLE = """
        CREATE TABLE todo.task (
            id SERIAL PRIMARY KEY,
            title VARCHAR(64) NOT NULL,
            description VARCHAR(256) NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """


ddl = DDL()
