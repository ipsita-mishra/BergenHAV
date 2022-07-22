import sqlite3, logging

def dbconnect():
    try:
        sqliteConnection = sqlite3.connect('housing.db')

    except sqlite3.Error as error:
        logging.error("Error occurred in dbconnect")
    return sqliteConnection

def dbdisconnect(sqliteConnection):
    sqliteConnection.commit()
    sqliteConnection.close()

