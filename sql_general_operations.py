import sqlite3
import csv

from variable_collections import zillow_db_path, gentrification_path, gentrification_db_path
from transfer_csv_to_sql import read_csv_header

'''
general way to create table
if with primary key, set with_primary_key true, and add primary_key_type, otherwise, set 
'''
def create_table(cols, types, table_name, db_path, with_primary_keys = False, primary_key_type = '', primary_key = ''):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    state = "CREATE TABLE IF NOT EXISTS " + table_name
    if not with_primary_keys:
        state += "  (id  CHAR(50) PRIMARY KEY " 
    else:
        state += " ( " + primary_key + " " + primary_key_type + " PRIMARY KEY "

    for i in range(len(cols)):
        state +=  ", " + str(cols[i]) + " " + str(types[i])
    state += ")"
    #print(state)
    c.execute(state)
    print ("table created successfully")
    conn.commit()
    conn.close()


def read_csv_table_header(csv_path):
    cols_all = {}
    index = 0
    with open(csv_path, 'r') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        for field in fieldnames:
            cols_all[field] = index
            index += 1
    infile.close()
    return cols_all


def add_col_to_table(db_path, table_name, col, type):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    state = "alter table " + table_name + " add column " + col + " " + type
    c.execute(state)
    conn.commit()
    conn.close()


'''
insert all data from csv to sql table
'''
def insert_data_from_csv(db_path, csv_path, table_name, primary_key = '', with_primary_key = False):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    cols_all = read_csv_header(csv_path)
    cols_name = [c for c in list(cols_all) if c]
    print(cols_name)

    if not cols_all:
        raise Exception('this csv table is empty')
        
    print("start insert data")
    csv_file = open(csv_path, "r")
    reader = csv.reader(csv_file)
    next(reader, None)
    id = 0

    for row in reader:
        try:
            if with_primary_key:
                state = "INSERT INTO " + table_name + " (" + primary_key 
                vals = [row[cols_all[primary_key]]]
            else:
                state = "INSERT INTO " + table_name + " (id"
                vals = [id]

            for col in cols_name:
                if col == primary_key or len(col) == 0:
                    continue
                if len(row[cols_all[col]]) == 0:
                    vals.append(0)
                elif col == 'RegionName_zip':
                    v = str(row[cols_all[col]])
                    for i in range(5 - len(v)):
                        v += "0"
                    vals.append(v)
                else:
                    vals.append(row[cols_all[col]])
                state += ","
                state += col

            state += ") VALUES (?"
            
            if with_primary_key:
                number_ques = len(cols_name) - 1
            else:
                number_ques = len(cols_name)
            
            for i in range(number_ques):
                state += ",?"
            
            state += ");"
            print(vals)
            c.execute(state, vals)
            conn.commit()
            print("inserted one record successfully")
            id += 1
        except Exception as e:
            print(str(e))      
    conn.close()






if __name__ == "__main__":
    #add_col_to_table(zillow_db_path, 'Zillow', 'eligible_gentrification', 'INT')
    cols = ['year', 'RegionName_zip', 'ZHVI_MiddleTier_zip', 'ZHVI_MiddleTier_metro', 'Median_Income_acs_zip', 'Median_Income_acs_cbsa', 'Education_acs_zip', 'Education_acs_cbsa', 'cbsa', 'eligible_gentrification', 'Population_acs_zip', 'Population_acs_cbsa', 'Education_pct_zip', 'Education_pct_cbsa']
    types = ['INT', 'CHAR(20)','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','FLOAT','INT', 'FLOAT', 'FLOAT', 'FLOAT', 'FLOAT']
    #create_table(cols, types, 'gentrification', gentrification_db_path)
    insert_data_from_csv(gentrification_db_path, gentrification_path, 'gentrification')
