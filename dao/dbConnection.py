import mysql.connector
from mysql.connector import Error
import pandas as pd

class DBConnection:

    _connection = None
    _host = "localhost"
    _user = "user_name"         # change to your own user's name
    _password = "password"      # change to your the user's password
    _database = "learnengdb"

    @classmethod
    def connect(cls):
        if cls._connection is None or not cls.is_connection_alive() :
            try:
                cls._connection = cls.create_db_connection(cls._host, cls._user, cls._password, cls._database)
                if cls._connection.is_connected():
                    print("MySQL Database connection successful")
            except Error as err:
                print(f"Failed to connect to the database : {err}")
        return cls._connection
    
    @classmethod
    def create_db_connection(cls, host_name, user_name, user_password, db_name):
        
        if cls._connection is None or not cls.is_connection_alive():
            
            connection = None
            try:
                connection = mysql.connector.connect(
                    host=host_name,
                    user=user_name,
                    passwd=user_password,
                    database=db_name
                )

            except Error as err:
                print(f"Error: '{err}'")

        return connection
    
    @classmethod
    def is_connection_alive(cls):
        try:
            if cls._connection is None or not cls._connection.is_connected():
                return False
            cls._connection.ping(reconnect=True, attempts=3, delay=5)
            return True
        except Error as e:
            print(f"Connection check failed: {e}")
            return False
        
    @classmethod
    def get_connection(cls):
        if not cls.is_connection_alive():
            print("db connection lost")
        elif cls._connection is None:
            raise Exception("Database not connected.")
        return cls._connection
    
    @classmethod
    def execute_query(cls, query):
        try:
            conn = cls.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)

            conn.commit()
        except Error as err:
            print(f"An error occurred during query execution: {err}")
            return None

    @classmethod
    def read_query(cls, query):
        result = None
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute(query)
            return cursor
        except Error as err:
            print(f"Error while retrieving data: {err}")

    @classmethod
    def fetch_all(cls, query):
        cursor = cls.read_query(query)

        result = cursor.fetchall() if cursor else []
        cursor.close()
        return result
    
    @classmethod
    def fetch_one(cls, query):
        try:
            conn = cls.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)

            result = cursor.fetchone()
            cursor.close()
            return result

        except Error as err:
            print(f"An error occurred during fetch_one: {err}")
            return None

    @classmethod
    def close_connection(cls):
        if cls._connection:
            cls._connection.close()
            cls._connection = None
            print("Connection closed")