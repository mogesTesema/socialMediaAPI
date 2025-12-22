import databases
import sqlalchemy
from storeapi.config import config

DATABASE_URL = config.DATABASE_URL
metadata = sqlalchemy.MetaData()
user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, nullable=False, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("confirmed", sqlalchemy.Boolean, default=False),
)

refreshtoken_table = sqlalchemy.Table(
    "refreshtokens",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("jti", sqlalchemy.String, nullable=False),
    sqlalchemy.Column(
        "user_email", sqlalchemy.ForeignKey("users.email"), nullable=False
    ),
    sqlalchemy.Column("revoked", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("hashed_token", sqlalchemy.String, nullable=False),
)

post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("image_url", sqlalchemy.String),
)

comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column(
        "post_id", sqlalchemy.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    ),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
)


like_table = sqlalchemy.Table(
    "likes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey("posts.id"), nullable=False),
)

connect_args={"check_same_thread": False} if "sqlite" in config.DATABASE_URL else {}
engine = sqlalchemy.create_engine(
    url=DATABASE_URL, connect_args=connect_args
)
db_args = {"min_size":1,"max_size":5} if "postgres" in DATABASE_URL else {} 
def db_connection():

    metadata.create_all(engine)
    database = databases.Database(DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK,**db_args)

    return database
 