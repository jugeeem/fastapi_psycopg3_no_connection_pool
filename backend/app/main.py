from db.database import get_connection
from fastapi import FastAPI
from routers import todo
from db.query.ddl import ddl


app = FastAPI()

app.include_router(todo.router)


@app.get("/")
def root():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ddl.CREATE_TODO_SCHEMA)
        # テーブルが存在するか確認
        cursor.execute("SELECT to_regclass('todo.task')")
        if cursor.fetchone()[0] is None:
            # テーブルが存在しない場合のみ作成
            cursor.execute(ddl.CREATE_TASK_TABLE)
    return {"message": "created schema and table if not exists"}
