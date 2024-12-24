import os
from dotenv import load_dotenv

load_dotenv()


mongo_db_url = os.environ['MONGO_DB_URL']
mongo_db_name = os.environ['MONGO_DB_NAME']
collection_name = os.environ['COLLECTION_NAME']

neo4j_url = os.environ['NEO4J_URI']
neo4j_user = os.environ['NEO4J_USER']
neo4j_password = os.environ['NEO4J_PASSWORD']

api_key_open_cage = os.environ['YOUR_API_KEY_OpenCage']