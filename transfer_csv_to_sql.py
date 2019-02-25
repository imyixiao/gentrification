import sqlite3
import pandas 
from variable_collections import yelp_db_path, zillow_path, cols_required, cols_opt, cols_all, zillow_db_path,\
    gentrification_path, gentrification_db_path
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
    conn = sqlite3.connect(zillow_db_path)
    c = conn.cursor()
    state = "CREATE TABLE IF NOT EXISTS " + table_name
    state += "  (id  CHAR(50) PRIMARY KEY, " \
       " Date TEXT, " \
       " year  INT  , " \
       " month INT  , " \
       " RegionName CHAR(10)" 
    for col in cols_opt:
        state += "," + str(col) + "   INT "
    state += ")"
    #print(state)
    c.execute(state)
    print ("Zillow table created successfully")
    conn.commit()
    conn.close()


'''
create gentrification sql table
'''
def create_gentrification_table(table_name, cols_opt = cols_opt):
    conn = sqlite3.connect(gentrification_db_path)
    c = conn.cursor()
    state = "CREATE TABLE IF NOT EXISTS " + table_name
    state += "  (id  CHAR(50) PRIMARY KEY , " \
       " year INT , " \
       " zipcode CHAR(10) , " \
       " median_home_value_zip INT , " \
       " median_home_value_metro INT , " \
       " median_income_zip INT , " \
       " median_income_cbsa INT , " \
       " education_count_zip INT , " \
       " education_count_cbsa INT , " \
       " cbsa INT , " \
       " eligible_gentrification INT , " \
       " population_count_zip INT , " \
       " population_count_cbsa INT , " \
       " education_pct_zip REAL , " \
       " education_pct_cbsa REAL , " \
       " pct_chg_income_zip REAL , " \
       " pct_chg_income_cbsa REAL , " \
       " pct_chg_houseval_zip REAL , " \
       " pct_chg_houseval_cbsa REAL , " \
       " pct_chg_education_zip REAL , " \
       " pct_chg_education_cbsa REAL , " \
       " gentrifying INT"

    # for col in cols_opt:
    #     state += "," + str(col) + "   INT "
    state += ")"
    # print(state)
    c.execute(state)
    print ("Gentrification table created successfully")
    conn.commit()
    conn.close()


'''
param:
cols : list of cols needed, including different metrics for example medium single house price
year_bar : only need record after this year
'''
def insert_from_csv_to_sql(csv_path = zillow_path, table_name = 'Zillow', cols = cols_opt, cols_all = cols_all, year_bar = 2005, db_path = zillow_db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    if not cols_all:
        try:
            cols_all = read_zillow_header()
        except:
            pass
    
    print("start insert data")
    zillow_file = open(csv_path, "r")
    reader = csv.reader(zillow_file)
    id = 0
    if table_name == 'Zillow':
        for row in reader:
            try:
                #print(row)
                date = row[0]
                region_name = row[1]
                year = date.split("-")[0]

                if int(year) < year_bar:
                    continue

                month = date.split("-")[1]
                new_date = year + "-" + month

                vals = [str(id), new_date, year, month, region_name]
                state = "INSERT INTO " + table_name + " (id, Date, year, month, RegionName"

                for col in cols:
                    if len(row[cols_all[col]]) == 0:
                        vals.append(0)
                    else:
                        vals.append(row[cols_all[col]])
                    state += ", "
                    state += col


                state += ") VALUES (?,?,?,?,?"
                for i in range(len(cols)):
                    state += ",?"
                state += ");"

                print(vals)
                c.execute(state, vals)
                conn.commit()
                print("inserted " + str(region_name) + " in " + str(new_date))
                id += 1

            except Exception as e:
                print(str(e))
    if table_name == 'Gentrification':
        next(reader, None)
        for row in reader:
            try:
                print(row)
                # print(len(row))
                year = row[1]
                zipcode = row[2]
                median_home_value_zip = row[3]
                median_home_value_metro = row[4]
                median_income_zip = row[5]
                median_income_cbsa = row[6]
                education_count_zip = row[7]
                education_count_cbsa = row[8]
                cbsa = row[9]
                eligible_gentrification = row[10]
                population_count_zip = row[11]
                population_count_cbsa = row[12]
                education_pct_zip = row[13]
                education_pct_cbsa = row[14]
                pct_chg_income_zip = row[15]
                pct_chg_income_cbsa = row[16]
                pct_chg_houseval_zip = row[17]
                pct_chg_houseval_cbsa = row[18]
                pct_chg_education_zip = row[19]
                pct_chg_education_cbsa = row[20]
                gentrifying = row[21]

                # if int(year) < year_bar:
                #     continue

                vals = [str(id), year, zipcode, median_home_value_zip, median_home_value_metro, median_income_zip, median_income_cbsa,
                        education_count_zip, education_count_cbsa, cbsa, eligible_gentrification, population_count_zip, population_count_cbsa,
                        education_pct_zip, education_pct_cbsa, pct_chg_income_zip, pct_chg_income_cbsa, pct_chg_houseval_zip,
                        pct_chg_houseval_cbsa, pct_chg_education_zip, pct_chg_education_cbsa, gentrifying]
                state = "INSERT INTO " + table_name + " (id, year, zipcode, median_home_value_zip, median_home_value_metro," \
                                                      "median_income_zip, median_income_cbsa, education_count_zip, " \
                                                      "education_count_cbsa, cbsa, eligible_gentrification, population_count_zip," \
                                                      "population_count_cbsa, education_pct_zip, education_pct_cbsa, pct_chg_income_zip," \
                                                      "pct_chg_income_cbsa, pct_chg_houseval_zip, pct_chg_houseval_cbsa," \
                                                      "pct_chg_education_zip, pct_chg_education_cbsa, gentrifying"

                # for col in cols:
                #     if len(row[cols_all[col]]) == 0:
                #         vals.append(0)
                #     else:
                #         vals.append(row[cols_all[col]])
                #     state += ", "
                #     state += col

                state += ") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?"
                # for i in range(len(cols)):
                #     state += ",?"
                state += ");"

                # print(vals)
                c.execute(state, vals)
                conn.commit()
                id += 1

            except Exception as e:
                print(str(e))
               
        
    conn.close()



if __name__ == "__main__":
    '''
    predefine that we need zillow table with cols including date, region_name, 
    and col_opt including several cols, we could use different col_opt
    '''
    create_zillow_table('Zillow')
    # insert_from_csv_to_sql()

    create_gentrification_table('Gentrification')
    insert_from_csv_to_sql(gentrification_path, 'Gentrification', cols_opt, cols_all, 2012, gentrification_db_path)