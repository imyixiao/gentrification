import sqlite3
import pandas 
from variable_collections import db_path, zillow_path, cols_required, cols_opt, cols_all
import csv    



'''
functions used to transfer csv format file to sql format tables
'''



'''
read zillow csv file to save all col names into global variable cols_all
in cols_all, key is col name, value is index, which will be used in other functions
'''
def read_zillow_header(zillow_path = zillow_path):
    cols_all = {}
    index = 0
    with open(zillow_path, 'r') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        for field in fieldnames:
            cols_all[field] = index
            index += 1
    infile.close()
    return cols_all
    



'''
create zillow sql table with col required and col_opt(defined in variable collections)
'''
def create_zillow_table(table_name, cols_opt = cols_opt):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    state = "CREATE TABLE IF NOT EXISTS " + table_name
    state += "  (id  INTEGER PRIMARY KEY   AUTOINCREMENT, " \
       " Date TEXT, " \
       " year  INT  , " \
       " month INT  , " \
       " RegionName CHAR(10)" 
    for col in cols_opt:
        state += "," + str(col) + "   INT "
    state += ")"
    #print(state)
    c.execute(state)
    print ("Table created successfully")
    conn.commit()
    conn.close()






def insert_from_csv_to_sql(csv_path = zillow_path, table_name = 'Zillow', cols = cols_opt, cols_all = cols_all):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    if not cols_all:
        cols_all = read_zillow_header()
    
    print("start insert data")
    zillow_file = open(csv_path, "r")
    reader = csv.reader(zillow_file)
    for row in reader:
        try:
            #print(row)
            date = row[0]
            region_name = row[1]
            year = date.split("-")[0]
            month = date.split("-")[1]
            new_date = year + "-" + month
            
            vals = [new_date, year, month, region_name]
            state = "INSERT INTO " + table_name + " (Date, year, month, RegionName"

            for col in cols:
                if len(row[cols_all[col]]) == 0:
                    vals.append(0)
                else:
                    vals.append(row[cols_all[col]])
                state += ", "
                state += col
            

            state += ") VALUES (?,?,?,?"
            for i in range(len(cols)):
                state += ",?"
            state += ");"

            print(vals)
            c.execute(state, vals)
            conn.commit()
            print("inserted " + str(region_name) + " in " + str(new_date))

        except Exception as e:
            print(str(e))
               
        
    conn.close()



if __name__ == "__main__":
    '''
    predefine that we need zillow table with cols including date, region_name, 
    and col_opt including several cols, we could use different col_opt
    '''
    create_zillow_table('Zillow')
    insert_from_csv_to_sql()