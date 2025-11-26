import databases
import sqlalchemy
from config import config

DATABASE_URL = config.DATABASE_URL
metadata = sqlalchemy.MetaData()

post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.column("body",sqlalchemy.String)
)

comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.column("body",sqlalchemy.String),
    sqlalchemy.column("post_id",sqlalchemy.ForeignKey("posts.id"),nullable=False)
)

engine = sqlalchemy.create_engine(
    url=DATABASE_URL,
    connect_args={"check_same_thread":False}
    )

metadata.create_all(engine)
database = databases.Database(DATABASE_URL, force_rollback=config.FORCE_ROLL_BACK)