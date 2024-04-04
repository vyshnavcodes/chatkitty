from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() # Base class for models (optional)

# Define the database connection string (replace with your desired filename)
engine = create_engine('sqlite:///knowledge_base.db')

