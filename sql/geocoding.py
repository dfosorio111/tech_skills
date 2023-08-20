import sqlite3 as sql
import json # array of array data file

# connection from Python to SQL database
conn = sql.connect('')

# SQL: Python handle
cur = conn.cursor()








# conn.commit() , execute SQL commands to database
conn.commit()

# close SQL handle
cur.close()



