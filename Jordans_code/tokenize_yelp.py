import sqlite3 as sqlite
from sqlite3 import Error
import sys
import os

# import PySpark

# from pyspark import SparkConf, SparkContext


db = "../data/yelp/yelp.db"
table_name = "Reviews"


### Connect to database, get the text from a review

def connect_db(db = db):
    try:
        conn= sqlite.connect(db)
        cur = conn.cursor()
    except:
        print("Could not connect to database")


#insert avg word length, what else?

# check if column exists in database, otherwise, insert column in database
# needs table name, column name, column type, db name
def connect_check_column(column_name):
    global db
    global table_name

    column_type = "CHAR(50)"

    conn= sqlite.connect(db)
    cursor = conn.execute("select * from {}".format(table_name))

    colnames = cursor.description
    columns = [row[0] for row in colnames]

    if column_name not in columns:
        cursor.execute('ALTER TABLE {} ADD COLUMN {} {};'.format(table_name, column_name, column_type))
        print("Inserted column {} in table".format(column_name))
    else:
        print("{} already exists in table".format(column_name))

# connect_check_column("text7")

### Insert into database
def populate_df(column_name):
    global db
    global table_name

    # connection = connect_check_column(column_name)
    # connection=connect_db()
    conn= sqlite.connect(db)
    cur = conn.cursor()
    trial = "o"
    insert_statement = '''
        INSERT INTO Reviews({})
        VALUES(?)
        '''.format(column_name)
    cur.execute(insert_statement, trial)
    # conn.commit()
    # conn.close()

populate_df("text5")