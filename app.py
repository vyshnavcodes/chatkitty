from flask import Flask, render_template, request, jsonify

# Import libraries for SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fuzzywuzzy import process
import csv

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
  knowledge_base = session.query(KnowledgeEntry.keyword, KnowledgeEntry.response).all()
  kb_dict = {entry.keyword: entry.response for entry in knowledge_base}
  session.close()
  return kb_dict

# Load knowledge base into a variable
knowledge_base = load_knowledge_base("sample_data.csv")

app = Flask(__name__)

def process_message(user_message):
  """Processes the user's message using simple keyword matching.

  Args: 
      user_message: The user's message on a string.

  Returns:
         A string containing the chatbot's response on the knowledgebase.
  """

  #lowercase the message for case-insensitive matching
  lower_message = user_message.lower()

  #Use fuzzy matching to find the closest match in the knowledgebase
  matches = process.extractOne(lower_message, knowledge_base.keys(), score_cutoff=80)

  #check if a close match is found
  if matches:
    matched_keyword, score = matches
    
    return knowledge_base[matched_keyword]
  else:
    #if no match found, provide a default response
    return "Sorry, I couldn't help you with that. Is there anything else I could help you with?".format(user_message)
  

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
  #get the user's message from the request data
  user_message = request.json.get('message')

  #process the user message (we'll add logic here later)
  response = process_message(user_message)

  #return a JSON response with the chatbot's response
  return jsonify({'response': response})

  # Search knowledge base for relevant information
  response = knowledge_base.get(user_message.lower(), None)

  if response:
    return response
  else:
    return "sorry, I couldn't find anything related to that."

if __name__ == '__main__':
  app.run(debug=True)
