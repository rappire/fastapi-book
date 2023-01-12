from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient
import app.config as config


class MongoDB:
    def __init__(self):
        self.client = None
        self.engine = None

    def connect(self):
        self.client = AsyncIOMotorClient(config.MONGO_URL)
        self.engine = AIOEngine(client=self.client, database=config.MONGO_DB_NAME)
        print("DB connect : complete")

    def disconnect(self):
        self.client.close()


mongodb = MongoDB()
