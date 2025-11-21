from storeapi.models.data.db_connection import DatabaseConnection

host_store = "database.db"
def create_post_table():
    with DatabaseConnection(host_storage=host_store) as db_connect:
        post_table_sql = "CREATE TABLE IF NOT EXISTS posts(post_id INTEGER PRIMARY KEY AUTOINCREMENT,post_text TEXT NOT NULL)"
        cursor = db_connect.cursor()

        cursor.execute(post_table_sql)

def creat_comment_table():
    with DatabaseConnection(host_store) as db_connect:
        comment_table_sql = "CREATE TABLE IF NOT EXISTS comments(comment_id INTEGER PRIMARY KEY AUTOINCREMENT,comment_text TEXT,post_id INTEGER NOT NULL,FOREIGN KEY(post_id) REFERENCES posts(post_id))"
        cursor = db_connect.cursor()
        cursor.execute(comment_table_sql)

create_post_table()
creat_comment_table()

async def create_post(post_text:str)-> int:
    with DatabaseConnection(host_storage=host_store) as db_connect:
        cursor = db_connect.cursor()
        post_text_sql = "INSERT INTO posts(post_text) VALUES(?)"
        cursor.execute(post_text_sql,(post_text,))
        cursor.execute("SELECT post_id FROM posts where post_text=?",(post_text,))
        created_post_id = cursor.fetchone()[0]
    return created_post_id
    

