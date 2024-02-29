from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import Settings

settings=Settings()



#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
 
# Using the sqlalchemy against raw sql interactions with the database
# @app.get("/sqlalchemy")
# def test_posts(db:Session = Depends(get_db)):
# posts =  db.query(models.Post).all()
# return {"Data": posts}
        
        
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password=12345,
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break

#     except Exception as Error:
#         print("Connecting to database failed")
#         print("Error: ", Error)
#         time.sleep(3)



# def get_db():
#     # Connect to the PostgreSQL database
#     db = psycopg2.connect(
#         host='localhost',
#         database='fastapi',
#         user='postgres',
#         password=12345,
#         cursor_factory=RealDictCursor
#     )
    
#     # Create a cursor object for database interaction
#     cursor = db.cursor()

#     try:
#         # Yield the cursor to the dependent function
#         yield cursor
#     finally:
#         # Cleanup: close the cursor and the database connection
#         cursor.close()
#         db.close()




 
 