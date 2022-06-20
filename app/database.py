from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings as env
import psycopg2
import time
from psycopg2.extras import RealDictCursor

# structure of URL is 
# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{env.database_username}:{env.database_password}@{env.database_hostname}:{env.database_port}/{env.database_name}'

# engine is responsible to establish connection between SQLAlchemy and
# Postgres database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# to actually talk to SQL database, need to open a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# all models to create tables extend Base class
Base = declarative_base()

# Dependency that is called every time a request is made
# returns session which is interface between python and postgres db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         # connect to existing database
#         # cursor_factory tells you which values map to which column
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='Sqlbet345!',
#                                 cursor_factory=RealDictCursor)
        
#         # open a cursor to perform database operations
#         cur = conn.cursor()
#         print("Database connection was successful!")
#         break  
#         # cur.close() # close cursor
#         # conn.close() # close connection
#     except Exception as error:
#         print("Connection to database failed.")
#         print(error)
#         time.sleep(2)