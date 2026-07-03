import psycopg
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg.rows import dict_row
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# engine connects our code to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# session allow us to execute sql queries and get results
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base is the class that our models will inherit from, it contains the metadata of the database
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# while True:
#     try:
#         # here we are connecting to the database and creating a cursor
#         conn = psycopg.connect(host='localhost', port=5432, dbname='fastapi', user='postgres', password='0520505', row_factory=dict_row)
#         cursor = conn.cursor() # with this we can execute sql queries
#         print("Database connection was successful")
#         break
#     except Exception as e:
#         print("Database connection failed")
#         print(f'Error: {e}')
#         break
