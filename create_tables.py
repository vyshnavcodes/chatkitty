from models import Base

#Import the engine from db_connection.py
#Assuming db_connection.py is in the same directory

Base.metadata.create_all(engine)

