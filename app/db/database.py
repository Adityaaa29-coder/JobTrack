import ssl
import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import DeclarativeBase,Session


class Base(DeclarativeBase):
    pass

load_dotenv()

database_url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST", "127.0.0.1"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
    database=os.getenv("MYSQL_DATABASE", "jobtrack_db"),
)

ssl_context = ssl.create_default_context(cafile="ca.pem")

engine = create_engine(
    database_url,
    connect_args={"ssl": ssl_context},
    pool_pre_ping=True,
)


def test_mysql_connection():
    with engine.connect() as connection:
        return connection.execute(text("SELECT 1")).scalar_one()


def get_db():
    with Session(engine) as db:
        yield db
