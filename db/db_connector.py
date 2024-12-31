import os

import certifi
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient

load_dotenv()

connection_uri = os.getenv('LAST_PASS_CLONE_MONGODB_CONNECTION_URI')
client = MongoClient(connection_uri, tlsCAFile=certifi.where())
db = client["pass-guard-db"]


def connect_db(success_callback):
    try:
        client.admin.command('ping')  # Send a ping to confirm a successful connection
        if success_callback is not None:
            success_callback()
    except Exception as e:
        print(e)
