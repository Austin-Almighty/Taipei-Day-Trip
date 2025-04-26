from .db_connect import Database

shared_pool = Database(name="shared_pool", size=10)