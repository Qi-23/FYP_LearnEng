import mysql.connector
from mysql.connector import Error
import pandas as pd
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection



# connection = create_db_connection("localhost", "qi", "2310", "learnengdb")


insert_scenario = """
INSERT INTO scenario VALUES
();
"""


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

q1 = """
SELECT *
FROM editor;
"""
# results = read_query(connection, q1)

# for result in results:
#   print(result)

x = {"asdf", "ased", "ged"}
print(type(x))