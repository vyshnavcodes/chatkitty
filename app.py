from flask import Flask, render_template, request

# Import libraries for SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import KnowledgeEntry

# Define your database connection string
SQLALCHEMY_DATABASE_URI = 'sqlite:///knowledge_base.db'  # Replace with your database URI

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Create a session factory
Session = sessionmaker(bind=engine)

# Function to load knowledge base from the database
def load_knowledge_base():
  """
  Loads knowledge base entries from the database.
  """
  session = Session()
  knowledge_base = session.query(KnowledgeEntry).all()  # Replace 'KnowledgeEntry' with your class name
  kb_dict = {entry.keyword: entry.response for entry in knowledge_base}
  session.close()
  return kb_dict

# Load knowledge base into a variable
knowledge_base = load_knowledge_base()

app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

# Function to add a new entry to the knowledge base
def add_entry(question, answer):
  """
  Adds a new entry to the knowledge base and saves it to the database.
  """
  session = Session()
  # Create a new KnowledgeEntry object
  new_entry = KnowledgeEntry(question=question, answer=answer)  # Replace 'KnowledgeEntry' with your class name
  # Add the new entry to the session
  session.add(new_entry)
  # Commit the changes to the database
  session.commit()
  session.close()
  return "Entry added successfully!"

@app.route('/submit', methods=["POST"])
def submit_entry():
  question = request.form["question"]
  answer = request.form["answer"]
  # Call the add_entry function to handle database interaction
  response = add_entry(question, answer)
  return response

@app.route('/chat', methods=['POST'])
def chat():
  # ... (existing logic to get user message)

  # Search knowledge base for relevant information
  response = knowledge_base.get(user_message.lower(), None)

  if response:
    return response
  else:
    return "sorry, I couldn't find anything related to that."

if __name__ == '__main__':
  app.run(debug=True)
