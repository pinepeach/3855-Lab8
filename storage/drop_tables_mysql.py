import mysql.connector
db_conn = mysql.connector.connect(host="architect.eastus2.cloudapp.azure.com", user="user", password="password", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
 DROP TABLE sales, returns
''')
db_conn.commit()
db_conn.close()