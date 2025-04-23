import mysql.connector
from mysql.connector import pooling
import os, json
from dotenv import load_dotenv


load_dotenv()

config_string = os.getenv("config")
config = json.loads(config_string)

class Database:
  def __init__(self, name: str = "connection_pool", size:int = 5):
    self.name = name
    self.size = size
    self.pool = pooling.MySQLConnectionPool(
      pool_name=name,
      pool_size=size,
      **config)
  
  def get_connection(self)->mysql.connector.MySQLConnection:
    return self.pool.get_connection()
  
  def select_all(self, query:str, parameters: dict | tuple | None = None) -> list[dict]:
    connection = self.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        if parameters is not None:
          cursor.execute(query, parameters)
        else:
          cursor.execute(query)
        return cursor.fetchall()
    finally:
      cursor.close()
      connection.close()

    
  def select_one(self, query:str, parameters: dict | tuple | None = None) -> dict | None:
    connection = self.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        if parameters is not None:
          cursor.execute(query, parameters)
        else:
          cursor.execute(query)
        return cursor.fetchone()
    finally:
      cursor.close()
      connection.close()
  
  def insert(self, query:str, values: dict | tuple):
    connection = self.get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
      cursor.execute(query, values)
      connection.commit()
    finally:
      cursor.close()
      connection.close()




