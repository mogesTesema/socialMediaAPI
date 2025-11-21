from db_connection import DatabaseConnection

host_store = "database.db"
def create_post_table():
    with DatabaseConnection(host_storage=host_store) as db_connect:
        post_table_sql = "CREATE TABLE IF NOT EXISTS posts(post_id INTIGER UNIQUE PRIMARY KEY,post_body TEXT NOT NULL)"
        cursor = db_connect.cursor()

        cursor.execute(post_table_sql)

def creat_comment_table():
    with DatabaseConnection(host_store) as db_connect:
        comment_table_sql = "CREATE TABLE IF NOT EXISTS comments(comment_id INT UNIQUE PRIMARY KEY,comment_text TEXT,post_id INTIGER NOT NULL,FOREIGN KEY(post_id) REFERENCES posts(post_id))"
        cursor = db_connect.cursor()
        cursor.execute(comment_table_sql)

create_post_table()
creat_comment_table()

def create_post(post_text:str)-> int:
    with DatabaseConnection(host_storage=host_store) as db_connect:
        cursor = db_connect.cursor()
        post_text_sql = "INSERT INTO posts(post_body)values(?)"
        cursor.execute(post_text_sql,(post_text))
    created_post_id = cursor.execute("select post_id from posts where post_text=(?)",post_text)
    return created_post_id
    

