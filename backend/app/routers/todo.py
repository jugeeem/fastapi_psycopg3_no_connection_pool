from fastapi import APIRouter, HTTPException
from psycopg.rows import class_row

from core.config import config
from db.database import get_connection
from db.query.create_query import create_query
from db.query.delete_query import delete_query
from db.query.read_query import read_query
from db.query.update_query import update_query
from schemas.todo import TodoCreate, TodoRead, TodoUpdate

# routerのprefixを設定
router = APIRouter(prefix=config.TODO_PREFIX)


@router.post("/")
def create_todo(todo: TodoCreate):
    with get_connection() as conn:
        conn.execute(
            create_query.CREATE_TODO_TASK,
            (todo.title, todo.description),
        )
    return {"message": "Todo created successfully."}


@router.get("/")
def read_todos():
    with get_connection() as conn, conn.cursor(row_factory=class_row(TodoRead)) as cur:
        records = cur.execute(read_query.READ_ALL_TODO_TASK).fetchall()
        return records


@router.get("/{id}")
def read_todo_by_id(id: int):
    with get_connection() as conn, conn.cursor(row_factory=class_row(TodoRead)) as cur:
        record = cur.execute(read_query.READ_TODO_TASK_BY_ID, (id,)).fetchone()
        if record is None:
            raise HTTPException(status_code=404, detail="Todo not found.")
        return record


@router.put("/")
def update_todo_by_id(todo: TodoUpdate):
    with get_connection() as conn:
        conn.execute(
            update_query.UPDATE_TODO_TASK_BY_ID,
            (todo.title, todo.description, todo.id),
        )
    return {"message": "Todo updated successfully."}


@router.delete("/{id}")
def delete_todo_by_id(id: int):
    with get_connection() as conn:
        conn.execute(
            delete_query.DELETE_TODO_TASK_BY_ID,
            (id,),
        )
    return {"message": "Todo deleted successfully."}
