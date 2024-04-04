import csv

def load_knowledge_base(filename):
    """Loads knowledgebase entries from a CSV file.

    Args:
        filename: The path to the CSV file containing knowledge base data.
    """

    knowledge_base = {}
    with open(filename, 'r', encoding="utf8") as csvfile:  # Use the provided filename
        reader = csv.DictReader(csvfile)

        for row in reader:
            question = row['question'].lower()
            answer = row['answer']
            knowledge_base[question] = answer

    return knowledge_base
