import mysql.connector
from mysql.connector import Error
import pandas as pd

class DBConnection:

    _connection = None
    _host = "localhost"
    _user = "root"         # change to your own user's name
    _password = "shanyi"      # change to your the user's password
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
            cls.connect()
            print("db connection lost")
        elif cls._connection is None:
            raise Exception("Database not connected.")
        return cls._connection
    
    @classmethod
    def execute_query(cls, query, params=None):
        try:
            conn = cls.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
        except Exception as e:
            print(f"An error occurred during execute_query: {e}")
            raise

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
    def fetch_all(cls, query, params=None):
        try:
            conn = cls.get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"An error occurred during fetch_all: {e}")
            raise
    
    @classmethod
    def fetch_one(cls, query, params=None):
        try:
            conn = cls.get_connection()
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        except Exception as e:
            print(f"An error occurred during fetch_one: {e}")
            raise

    @classmethod
    def close_connection(cls):
        if cls._connection:
            cls._connection.close()
            cls._connection = None
            print("Connection closed")