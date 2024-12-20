from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb+srv://karthick:123@cluster0.fzmnu.mongodb.net/?authSource=cluster0&authMechanism=SCRAM-SHA-1')  # Replace with your MongoDB URI
db = client['test']  # Replace with your database name
collection = db['users']  # Replace with your collection name

# Check if the connection is established
try:
    # Attempt to send a ping to the MongoDB server
    client.admin.command('ping')
    print("MongoDB connection established successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Insert a user
def insertdata(user_data):
    result = collection.insert_one(user_data)
    

# Retrieve all users to check if the email exists
def get_all_users():
    users = collection.find()  # Fetch all users from the database
    return list(users)  # Return a list of users
# Retrieve the inserted user

# Retrieve a user by email
def get_user_by_email(email):
    try:
        user = collection.find_one({'email': email})  # Find the user document with the matching email
        return user  # Returns None if no user is found
    except Exception as e:
        print(f"Error retrieving user by email: {e}")
        return None

def update_user_password(email, new_password):
    """Update the user's password in MongoDB."""
    result = collection.update_one({'email': email}, {'$set': {'password': new_password}})
    return result.modified_count > 0  # Returns True if a document was updated