from pymongo import MongoClient


def get_client():
    try:
        if os.environ.get('USERNAME') == "linux":
            CONNECTION_STRING = "mongodb://localhost:27017"
            client = MongoClient(CONNECTION_STRING)
            print("Connected to DB locally")
        return client
    except:
        print("Not connected to DB")
