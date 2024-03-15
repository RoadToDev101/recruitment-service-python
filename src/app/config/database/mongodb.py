from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Access a specific database
db = client['your_database_name']

# Access a specific collection
collection = db['your_collection_name']

# Perform database operations
# ...

# Close the connection
client.close()