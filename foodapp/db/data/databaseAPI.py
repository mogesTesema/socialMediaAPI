from foodapp.db.data.db_connection import DatabaseConnection

host_store = "database.db"
def create_post_table(host_store=host_store):
    with DatabaseConnection(host_storage=host_store) as db_connect:
        post_table_sql = "CREATE TABLE IF NOT EXISTS posts(post_id INTEGER PRIMARY KEY AUTOINCREMENT,post_text TEXT NOT NULL)"
        cursor = db_connect.cursor()
        cursor.execute(post_table_sql)

def creat_comment_table(host_store=host_store):
    with DatabaseConnection(host_store) as db_connect:
        comment_table_sql = "CREATE TABLE IF NOT EXISTS comments(" \
        "comment_id INTEGER PRIMARY KEY AUTOINCREMENT," \
        "comment_text TEXT NOT NULL,post_id INTEGER NOT NULL," \
        "FOREIGN KEY(post_id) REFERENCES posts(post_id) ON DELETE CASCADE)"
        cursor = db_connect.cursor()
        cursor.execute(comment_table_sql)

create_post_table()
creat_comment_table()

async def create_post(post_text:str)-> int:
    with DatabaseConnection(host_storage=host_store) as db_connect:
        cursor = db_connect.cursor()
        post_text_sql = "INSERT INTO posts(post_text) VALUES(?)"
        cursor.execute(post_text_sql,(post_text,))
        # cursor.execute("SELECT post_id FROM posts where post_text=?",(post_text,)) # wrong id retrieve method
        created_post_id = cursor.lastrowid
    return created_post_id


async def create_comment(post_id:int,comment_text:str):
    with DatabaseConnection(host_store) as db_connect:
        cursor = db_connect.cursor()
        comment_sql = "INSERT INTO comments(comment_text,post_id) VALUES(?,?)"
        post_id_sql = "SELECT post_id FROM posts where post_id=?"
        cursor.execute(post_id_sql,(post_id,))
        try:
            (db_post_id,) = cursor.fetchone() # unpack post_id since cursor.fetchone() returns (post_id,)
        except Exception:
            db_post_id = None
        if db_post_id == post_id:
            cursor.execute(comment_sql,(comment_text,post_id))
            comment_id = cursor.lastrowid
    if not db_post_id:
        raise FileNotFoundError
    return comment_id


async def get_post_comments(post_id:int):
    with DatabaseConnection(host_storage=host_store) as db_connect:
        cursor = db_connect.cursor()
        all_comments_sql = "SELECT comment_id,comment_text FROM comments where post_id=?"
        cursor.execute(all_comments_sql,(post_id,))
        all_comment = cursor.fetchall()
    return all_comment
    
async def get_post(post_id:int):
    with DatabaseConnection(host_storage=host_store) as db_connect:
        cursor = db_connect.cursor()
        post_query_sql = "SELECT post_text FROM posts where post_id=(?)"
        cursor.execute(post_query_sql,(post_id,))
        try:
            (post_text,)= cursor.fetchone()
        except Exception:
            return ""
    return post_text


async def get_all_posts():
    with DatabaseConnection(host_storage=host_store) as db_connect:
        cursor = db_connect.cursor()
        all_posts_sql = "SELECT post_id,post_text FROM posts LIMIT 50"
        cursor.execute(all_posts_sql)
        all_posts = cursor.fetchall()
    return all_posts

async def delete_post(post_id:int):
    with DatabaseConnection(host_storage=host_store) as db_connect:
        cursor = db_connect.cursor()
        delete_post_sql = "DELETE FROM posts where post_id=?"
        cursor.execute(delete_post_sql,(post_id,))

    
async def update_comment(comment_id,comment_text,post_id=0):
    with DatabaseConnection(host_storage=host_store) as db_connect:
        cursor = db_connect.cursor()
        update_comment_sql = "UPDATE comments SET comment_text=? where comment_id=?"
        cursor.execute(update_comment_sql,(comment_text,comment_id))