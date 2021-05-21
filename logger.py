import datetime
from motor import motor_asyncio

class DatabaseLogger:
    def __init__(self, motor_client, database_name: str, collection_name: str):
        self._client = motor_client
        self._database = self.client[database_name]
        self._collection = self.database[collection_name]

    @property
    def client(self):
        return self._client

    @property
    def database(self):
        return self._database

    @property
    def collection(self):
        return self._collection

    async def log_command(self, user_id: str, message: str, command: str, notes: str = None):
        if notes:
            await self.collection.insert_one({'type': 'command', 'user_id': user_id, 'message': message, 'command': command, 'datetime': datetime.datetime.utcnow(), 'notes': notes})
        else:
            await self.collection.insert_one({'type': 'command', 'user_id': user_id, 'message': message, 'command': command, 'datetime': datetime.datetime.utcnow()})

    async def log_error(self, module_name: str, error_description: str, notes: str = None):
        if notes:
            await self.collection.insert_one({'type': 'error', 'module_name': module_name, 'error_description': error_description, 'notes': notes})
        else:
            await self.collection.insert_one({'type': 'error', 'module_name': module_name, 'error_description': error_description})
