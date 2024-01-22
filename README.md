# Implement CRUD processing using FastAPI and psycopg3

## Introduction.
There are few articles related to psycopg3, so I wrote this article as a reminder for myself.  
In this article, I will show you how to make a DB connection without using psycopg's connection pool.  
I may write a future article on how to use psycopg's connection pool.
- [Official documentation for connection pools can be found here](https://www.psycopg.org/psycopg3/docs/advanced/pool.html#connection-pools)

Also, since this article focuses on psycopg3, we will include it in [Disclaimer](#Disclaimer), but for other content, please refer to other articles.

## Disclaimer
As described in [Introduction](#Introduction), this article focuses on psycopg3 operations.  
For this reason, the content not dealt with in this article is summarized below.
- Basic Python Usage
- Basic usage of FastAPI
- Basic usage of PostgreSQL
- Basic SQL usage
- Basic usage of Docker
- How to use Docker Compose
- About Open API

## Environment building
To eliminate environmental differences, we will use Docker to build the environment.  
In any directory, execute the following commands.
``` 
$ git clone https://github.com/jugeeem/fastapi_psycopg3_no_connection_pool.git
```
Then execute the following command
```
docker-compose up -d
```
When the container has been built, access the following URL
```
http://127.0.0.1:8000/
```
After that, access the following URL to display the Swagger UI.
```
http://127.0.0.1:8000/docs
```

## Body
First, set the necessary information for DB connection to the environment variables.
The `get_connection()` function is used to make the DB connection.  
It is possible to wrap this function with a with statement to make a DB connection; however, it is necessary to write `commit()`, `close()`, etc. every time, and this is a best practice in the official sense to prevent omissions. However, it is necessary to write `commit()`, `close()`, etc. every time.
```
# backend/app/db/database.py

import psycopg
from core.config import config

conninfo = f"user={config.DATABASE_USER} password={config.DATABASE_PASSWORD} host={config.DATABASE_HOST} port={config.DATABASE_PORT} dbname={config.DATABASE_DBNAME}"


def get_connection():
    return psycopg.connect(conninfo)
```
Next, within each routing, the part that performs DB operations is described.
First, data creation is described as follows
```
# backend/app/routers/todo.py

from core.config import config
from db.database import get_connection
from schemas.todo import TodoCreate
from db.query.create_query import create_query

router = APIRouter(prefix=config.TODO_PREFIX)

@router.post("/")
def create_todo(todo: TodoCreate):
    with get_connection() as conn:
        conn.execute(
            create_query.CREATE_TODO_TASK,
            (todo.title, todo.description),
        )
    return {"message": "Todo created successfully."}
```
When you send a POST request to `http://127.0.0.1:8000/todo/`, the `create_todo()` function is executed.  
In that case, a DB connection is made because `get_connection()` is wrapped in a with statement.  
When executing the query, `conn.execute()` is used.
The first argument of `conn.execute()` specifies the query to be executed.
The second argument specifies the value to be placed in a placeholder in the query specified by the first argument.  
Now, let's check the file that actually defines the query.  
```
# backend/app/db/query/create_query.py

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
```
The `%s` is a placeholder.  
If the number of `%s` does not match the number of elements in the second argument tuple, an error will result.
In addition, there are multiple types of placeholders, which must be used accordingly.   

Next, the data acquisition is described as follows.
First, the acquisition of all data.
```
# backend/app/routers/todo.py

from core.config import config
from db.database import get_connection
from schemas.todo import TodoRead
from db.query.read_query import read_query

router = APIRouter(prefix=config.TODO_PREFIX)

@router.get("/")
def read_todos():
    with get_connection() as conn, conn.cursor(row_factory=class_row(TodoRead)) as cur:
        records = cur.execute(read_query.READ_ALL_TODO_TASK).fetchall()
        return records
```
You can see the change in the with statement compared to when executing INSERT.  
When retrieving data, specify a parameter to the `row_factory` argument of `conn.cursor()`.
In FastAPI, by specifying the `class_row()` function in the `row_factory` argument, you can convert the acquired data into an instance of the specified class.  
After executing `cru.execute()`, you can retrieve the retrieved data in a list by executing `fetchall()`.  
The query to be issued is the same as for INSERT and requires a placeholder value.

The next step is to retrieve specific data.
```
# backend/app/routers/todo.py

from core.config import config
from db.database import get_connection
from schemas.todo import TodoRead
from db.query.read_query import read_query

router = APIRouter(prefix=config.TODO_PREFIX)

@router.get("/{id}")
def read_todo_by_id(id: int):
    with get_connection() as conn, conn.cursor(row_factory=class_row(TodoRead)) as cur:
        record = cur.execute(read_query.READ_TODO_TASK_BY_ID, (id,)).fetchone()
        if record is None:
            raise HTTPException(status_code=404, detail="Todo not found.")
        return record
```
When executing `conn.cursor`, the `row_factory` argument specifies the `class_row()` function, which is the same as for fetching all data.
The difference is that `fetchone()` is executed instead of `fetchall()`.
By executing `fetchone()`, you can retrieve only one data item to be fetched.

Lastly, we will discuss updating and deleting data.
```
# backend/app/routers/todo.py

from core.config import config
from db.database import get_connection
from fastapi import APIRouter, HTTPException
from psycopg.rows import class_row
from schemas.todo import TodoUpdate
from db.query.update_query import update_query
from db.query.delete_query import delete_query

# routerのprefixを設定
router = APIRouter(prefix=config.TODO_PREFIX)

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
```
When issuing a query, use `conn.execute()`, so the flow of processing is the same as for INSERT.  
There is nothing special to mention.

## Summary  
This article described how to implement CRUD processing using psycopg3.  
Although we should probably delve a little deeper into the classes and functions defined, we believe that the information presented in this article is sufficient for a simple implementation of CRUD processing.

Also, although this article does not discuss psycopg3 connection pools, connection pools can be used to reduce the cost of DB connections.  
We may write about this in a future article.

Thank you for reading to the end.

## References
- [psycopg 3.2.0.dev1 documentation](https://www.psycopg.org/psycopg3/docs/index.html)
- [FastAPI: official documentation](https://fastapi.tiangolo.com/)

# FastAPIとpsycopg3を使ってCRUD処理を実装する

## はじめに
psycopg3の関連記事が少なく、私自身の備忘録も兼ねて、本記事を書きました。  
今回は、psycopgのconnection poolを使わずに、DB接続を行う方法を紹介します。  
psycopgのconnection poolの使い方について今後記事にするかもしれません。
- [connection poolの公式ドキュメントはこちら](https://www.psycopg.org/psycopg3/docs/advanced/pool.html#connection-pools)

また、この記事はpsycopg3について焦点を当てていますので、[免責事項](#免責事項)に記載しますが、それ以外の内容については他の記事を参考にしてください。

## 免責事項
[はじめに](#はじめに)で記載したように、本記事ではpsycopg3の操作に焦点を当てています。  
そのため、本記事で取り扱わない内容について、下記にまとめておきます。
- Pythonの基本的な使い方
- FastAPIの基本的な使い方
- PostgreSQLの基本的な使い方
- SQLの基本的な使い方
- Dockerの基本的な使い方
- Docker Composeの基本的な使い方
- Open APIについて

## 環境構築
環境差異をなくすために、Dockerを使って環境構築を行います。  
任意のディレクトリで、以下のコマンドを実行してください。
``` 
$ git clone https://github.com/jugeeem/fastapi_psycopg3_no_connection_pool.git
```
その後、以下のコマンドを実行してください。
```
docker-compose up -d
```
コンテナのビルドが完了しましたら、以下のURLにアクセスしてください。
```
http://127.0.0.1:8000/
```
その後、以下のURLにアクセスしてSwagger UIが表示されましたら、環境構築は完了です。
```
http://127.0.0.1:8000/docs
```

## 本文
まず、DB接続に必要な情報を環境変数に設定します。
`get_connection()`関数は、DB接続を行うための関数です。  
この関数をwith文でラップすることで、DB接続を行うことができます。with文を使わずに記述することも可能ですが、`commit()`や`close()`などを毎度記述する必要があり、記述漏れを未然に防ぐという意味もあり、公式ではベストプラクティスとしているようです。
```
# backend/app/db/database.py

import psycopg
from core.config import config

conninfo = f"user={config.DATABASE_USER} password={config.DATABASE_PASSWORD} host={config.DATABASE_HOST} port={config.DATABASE_PORT} dbname={config.DATABASE_DBNAME}"


def get_connection():
    return psycopg.connect(conninfo)
```
  
次に各ルーティング内で、DBの操作を行う部分について説明します。
まず、データの作成については、以下のように記述します。
```
# backend/app/routers/todo.py

from core.config import config
from db.database import get_connection
from schemas.todo import TodoCreate
from db.query.create_query import create_query

router = APIRouter(prefix=config.TODO_PREFIX)

@router.post("/")
def create_todo(todo: TodoCreate):
    with get_connection() as conn:
        conn.execute(
            create_query.CREATE_TODO_TASK,
            (todo.title, todo.description),
        )
    return {"message": "Todo created successfully."}
```
`http://127.0.0.1:8000/todo/`にPOSTリクエストを送信すると、`create_todo()`関数が実行されます。  
その際、`get_connection()`をwith文でラップしているため、DB接続が行われます。  
クエリを実行する際には、`conn.execute()`を使います。
`conn.execute()`の第一引数には、実行するクエリを指定します。
第二引数には、第一引数で指定したクエリ内のプレースホルダーに入れる値を指定します。  
では、実際にクエリを定義しているファイルを確認します。  
```
# backend/app/db/query/create_query.py

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
```
`%s`がプレースホルダーになります。  
`%s`の数と、第二引数のタプルの要素数が一致していないとエラーになります。
また、プレースホルダーには複数の型が存在し、適宜使い分ける必要があります。  


次に、データの取得については、以下のように記述します。
まず、全データの取得についてです。
```
# backend/app/routers/todo.py

from core.config import config
from db.database import get_connection
from schemas.todo import TodoRead
from db.query.read_query import read_query

router = APIRouter(prefix=config.TODO_PREFIX)

@router.get("/")
def read_todos():
    with get_connection() as conn, conn.cursor(row_factory=class_row(TodoRead)) as cur:
        records = cur.execute(read_query.READ_ALL_TODO_TASK).fetchall()
        return records
```
INSERTを実行するときと比べて、with文に変化があるのがわかりますね。  
データを取得する際には、`conn.cursor()`の`row_factory`引数にパラメータを指定します。
FastAPIでは、`row_factory`引数に`class_row()`関数を指定することで、取得したデータを指定したクラスのインスタンスに変換することができます。  
`cru.execute()`を実行した後に、`fetchall()`を実行することで、取得したデータをリストで取得することができます。  
発行するクエリはINSERTの時と同じで、プレースホルダに値を入れる必要があります。

次に、特定のデータの取得についてです。
```
# backend/app/routers/todo.py

from core.config import config
from db.database import get_connection
from schemas.todo import TodoRead
from db.query.read_query import read_query

router = APIRouter(prefix=config.TODO_PREFIX)

@router.get("/{id}")
def read_todo_by_id(id: int):
    with get_connection() as conn, conn.cursor(row_factory=class_row(TodoRead)) as cur:
        record = cur.execute(read_query.READ_TODO_TASK_BY_ID, (id,)).fetchone()
        if record is None:
            raise HTTPException(status_code=404, detail="Todo not found.")
        return record
```
`conn.cursor`を実行する際に、`row_factory`引数に`class_row()`関数を指定している点は、全データの取得と同じです。
異なるのは、`fetchall()`ではなく、`fetchone()`を実行している点です。
`fetchone()`を実行することで、取得したデータを1件だけ取得することができます。

最後に、データの更新と削除についてです。
```
# backend/app/routers/todo.py

from core.config import config
from db.database import get_connection
from fastapi import APIRouter, HTTPException
from psycopg.rows import class_row
from schemas.todo import TodoUpdate
from db.query.update_query import update_query
from db.query.delete_query import delete_query

# routerのprefixを設定
router = APIRouter(prefix=config.TODO_PREFIX)

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
```
クエリを発行する際には、`conn.execute()`を使いますので、処理の流れはINSERTの時と同じです。  
特筆する点はありません。

## まとめ  
本記事では、psycopg3を使ってCRUD処理を実装する方法について説明しました。  
本来であれば、定義されているクラスや関数についてもう少し掘り下げるべきなのかと思いますが、単純なCRUD処理を実装するだけであれば、本記事で紹介した内容で十分だと思います。

また、本記事ではpsycopg3のconnection poolについては触れていませんが、connection poolを使うことで、DB接続のコストを削減することができます。  
こちらについては、今後記事にするかもしれません。

最後まで読んでいただき、ありがとうございました。

## 参考文献
- [psycopg 3.2.0.dev1 documentation](https://www.psycopg.org/psycopg3/docs/index.html)
- [FastAPI: 公式ドキュメント](https://fastapi.tiangolo.com/)
