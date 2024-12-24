from pymongo import MongoClient
from app.settings.config import mongo_db_url, mongo_db_name
from neo4j import GraphDatabase
from app.settings.config import neo4j_url, neo4j_user, neo4j_password

driver = GraphDatabase.driver(
    neo4j_url,
    auth=(neo4j_user, neo4j_password)
)


def get_mongo_client():
    try:
        return MongoClient(mongo_db_url)  # No `with` statement here
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None


def get_mongo_db(db_name=mongo_db_name):
    client = get_mongo_client()
    if client:
        if db_name not in client.list_database_names():
            print(f"Database {db_name} does not exist. It will be created.")
        return client[db_name]
    return None


def get_collection(collection_name):
    db = get_mongo_db()
    if db is not None:
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
        return db[collection_name]
    print(f"Collection {collection_name} not found in database.")
    return None
