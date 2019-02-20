import sqlite3
import pandas 

db_path = "../yelp_data/yelp.db"
zillow_path = "../zillow_data/Zip_time_series.csv"
cols_required = ['Date', 'RegionName']
cols_opt = ['MedianListingPrice_AllHomes','MedianListingPrice_CondoCoop','MedianListingPrice_SingleFamilyResidence','MedianListingPrice_DuplexTriplex']

'''
functions used to transfer csv format file to sql format tables
'''


'''
create zillow table
'''
def create_zillow_table(table_name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    state = "CREATE TABLE IF NOT EXISTS " + table_name
    state += "  (id  INTEGER PRIMARY KEY   AUTOINCREMENT, " \
       " Date TEXT, " \
       " year  INT  , " \
       " month INT  , " \
       " RegionName CHAR(10)" 
    for col in cols_opt:
        state += "," + str(col) + "   TEXT "
    state += ")"
    #print(state)
    c.execute(state)
    print ("Table created successfully")
    conn.commit()
    conn.close()


def insert_from_csv_to_sql(csv_path = zillow_path, table_name = 'Zillow', cols = cols_opt):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    zillow_pd = pandas.read_csv(zillow_path)
    for index, row in zillow_pd.iterrows():
        try:
            date = row['Date']
            date_list = date.split("-")
            year = date_list[0]
            month = date_list[1]
            new_date = year + "-" + month
            region_name = row['RegionName']
            state = "INSERT INTO " + table_name + " (Date, year, month, RegionName"
            vals = [new_date, year, month, region_name]
            for c in cols:
                vals.append(row[c])
                state += ", "
                state += c
            state += ") VALUES (?,?,?,?"
            for i in range(len(c)):
                state += ",?"
            state += ");"
            c.execute(state, zip(vals))
            conn.commit()
        except ValueError:
                print("Skipping invalid row" + row)
    conn.close()


def generate_part_info_csv_table(zillow_part_info_path, cols_optional = cols_opt):
    zillow_whole = pandas.read_csv(zillow_path)
    cols = ['Date','RegionName']
    cols.extend(cols_optional)
    
    all_vals = dict()
    for c in cols:
        all_vals[c] = [] 
    
    for index, row in zillow_whole.iterrows():
        if index > 10:
            break;
        print(index)
        all_vals['Date'].append(row['Date'])
        all_vals['RegionName'].append(row['RegionName'])
        for opt_col in cols_optional:
            all_vals[opt_col].append(row[opt_col])
    
    zillow_part = pandas.DataFrame(all_vals)
    zillow_part.to_csv(zillow_part_info_path, encoding='utf-8', index=False)
    return zillow_part



if __name__ == "__main__":
    #create_zillow_table('Zillow')
    generate_part_info_csv_table('./data/zillow_part.csv')