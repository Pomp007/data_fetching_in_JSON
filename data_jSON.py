import json
import openai
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def load_text_file(file_path):
    """Load content from a text file."""
    with open('test.txt', "r") as file:
        content = file.read()
    return content

# Step 2: Use OpenAI's LLM to extract data
def extract_data_with_llm(content, extraction_goal):
    """Extract data using OpenAI's LLM."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is not set. Please check your .env file.")
    
    openai.api_key = api_key
    
    # Define the prompt
    prompt = (
        f"You are a data extraction assistant. Extract the following information in JSON format: {extraction_goal}. "
        f"Ensure the JSON is syntactically correct and properly formatted. Here is the text:\n\n{content}\n\n"
        "Example output format:\n"
        "{\n"
        '  "states": [\n'
        '    {"state": "Maharashtra", "capital": "Mumbai"},\n'
        '    {"state": "Karnataka", "capital": "Bengaluru"}\n'
        "  ]\n"
        "}"
    )
  

    # Query the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use "gpt-4.o" if "gpt-4" is unavailable
        messages=[

            {"role": "system", "content": "You are a helpful assistant for text analysis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0 # Use lower temperature for consistent results
    )
    
    # Parse the response
    extracted_data = response['choices'][0]['message']['content']
    if not extracted_data.strip():
        raise ValueError("The extracted data is empty.")
    return extracted_data

def insert_data_into_mongodb(json_data):
    """Insert JSON data into MongoDB."""
    # Connect to MongoDB
    client = MongoClient("mongodb://root:example@localhost:27017/?authSource=admin")  # Adjust host/port if needed
    db = client["scraped_data"]  # Replace with your database name
    collection = db["extracted_info"]  # Replace with your collection name

    # Insert data
    if isinstance(json_data, list):
        collection.insert_many(json_data)
    else:
        collection.insert_one(json_data)
    
    print("Data inserted into MongoDB successfully.")

# Main function
def main():
    try:
        # Step 1: Load the text file
        file_path = "test.txt"  # Path to your text file
        print("Loading the text file...")
        content = load_text_file(file_path)
        print("Text file loaded successfully.")

        extraction_goal = "List of Indian states with their capitals and union territories with their capitals."

        # Step 2: Extract data
        print("Extracting data...")
        extracted_data = extract_data_with_llm(content, extraction_goal)
        print("Data extracted successfully.")

        print("Extracted Data (Raw):", extracted_data)

        if not extracted_data.strip().startswith("{") and not extracted_data.strip().startswith("["):
            print(f"Unexpected data format: {extracted_data}")
            raise ValueError("The extracted data is not in valid JSON format.")

        json_data = json.loads(extracted_data)

         # insert data into mongo 
        print("Inserting data into MongoDB...")
        insert_data_into_mongodb(json_data)
        print("Data inserted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
 
if __name__ == "__main__":
    main()