import sqlite3 as sqlite
from sqlite3 import Error
import sys
import os
import regex as re
import tqdm
import sqlalchemy
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import spacy,en_core_web_sm
from collections import Counter

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
def connect_check_column(column_name, column_type):
    global db
    global table_name

    # column_type = "TEXT"
    conn= sqlite.connect(db)
    cursor = conn.cursor()

    try:
        cursor.execute('ALTER TABLE {} ADD COLUMN {} {};'.format(table_name, column_name, column_type))
        print("Inserted column {} in table".format(column_name))
    except Exception as e: 
        print(e)


# select text from a row in db
# need to read in tokenized text as a
# need to specify column
def select_rows():
    global db
    global table_name

    variable = "e"

    conn = sqlite.connect(db)
    cur = conn.cursor()
    cur2 = conn.cursor()

    for row in cur.execute("SELECT * FROM Reviews" ):
        cur2.execute('''UPDATE Reviews SET text5 = ?''', (variable))


# select_rows()


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
        INSERT INTO Reviews(trial2, text5)
        VALUES("1", "2")
        '''
    cur.execute(insert_statement)
    # conn.commit()
    # conn.close()



# populate_df("text5")

        # INSERT INTO Reviews (re.escape(column_name))

if __name__ == "__main__":
    # main()
    connect_check_column("test2", "TEXT")



# add column 
#  look at def add_review_month_in_review_table(path = yelp_db_path) in transfer_json_to_sql.py
