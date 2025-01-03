from pymongo import MongoClient

def verify_mongodb_connection():
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://root:example@localhost:27017/")  # Replace with your MongoDB URI
        # List available databases
        databases = client.list_database_names()
        
        print("Connection to MongoDB was successful!")
        print("Available Databases:", databases)
        
    except Exception as e:
        print("An error occurred while connecting to MongoDB:")
        print(e)

if __name__ == "__main__":
    verify_mongodb_connection()
