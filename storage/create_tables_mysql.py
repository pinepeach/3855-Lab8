import sqlite3
import mysql.connector

conn = sqlite3.connect('readings.sqlite')

db_conn = mysql.connector.connect(host="architect.eastus2.cloudapp.azure.com", user="user", password="password", database="events")

db_cursor = db_conn.cursor()
db_cursor.execute('''
            CREATE TABLE sales
            (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            title VARCHAR(250) NOT NULL,
            store INTEGER NOT NULL,
            till_number INTEGER NOT NULL,
            transaction_number INTEGER NOT NULL,
            date VARCHAR(10) NOT NULL,
            sku INTEGER NOT NULL,
            name VARCHAR(250) NOT NULL,
            price VARCHAR(10) NOT NULL,
            date_created VARCHAR(100) NOT NULL)
            ''')

db_cursor.execute('''
            CREATE TABLE returns
            (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            title VARCHAR(250) NOT NULL,
            store INTEGER NOT NULL,
            till_number INTEGER NOT NULL,
            transaction_number INTEGER NOT NULL,
            date VARCHAR(10) NOT NULL,
            sku INTEGER NOT NULL,
            name VARCHAR(250) NOT NULL,
            reason VARCHAR(250) NOT NULL,
            date_created VARCHAR(100) NOT NULL)
            ''')

db_conn.commit()
db_conn.close()
