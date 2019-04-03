import sqlite3
import json
from inside_boundary_checker import us_lower48_checker 
from variable_collections import business_json_path, res_json_path, review_json_path, yelp_db_path



'''
script:
python3 transfer_json_to_sql.py

result:
res.json -> reconstruct business.json, key would be restaurant id, which will be used to retreive res info by review 
(sqlite table) review -> include review info and restaurant location information 
'''


'''
create restaurant table, this table is used to fast retrieve res location information
which will be used to insert location data into review table
'''
def create_res_table():
    conn = sqlite3.connect(yelp_db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Restaurants
       (id  CHAR(50)  PRIMARY KEY     NOT NULL,
       name           TEXT   ,
       address        TEXT ,
       zipcode        CHAR(10),
	   lat     DECIMAL(12,9),
	   lng   DECIMAL(12,9),
	   stars   FLOAT)""")
    print ("Table created successfully")
    conn.commit()
    conn.close()




'''
create review table, add zipcode, lat, lng information into table
this table will be the main data source we will use in the future
'''
def create_review_table():
    conn = sqlite3.connect(yelp_db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Reviews
       (review_id  CHAR(50)  PRIMARY KEY     NOT NULL,
	   user_id  CHAR(50)   NOT NULL,
	   res_id  CHAR(50)   NOT NULL,
       lat    DECIMAL(12,9),
	   lng  DECIMAL(12,9),
       zipcode        CHAR(10),
	   review_year  INT,
	   review_date  TEXT,
	   text    TEXT,
	   useful   INT,
	   funny INT,
	   cool INT,
	   star   FLOAT)''')
    print ("Table created successfully")
    conn.commit()
    conn.close()


'''
version 2: add a new field, review month
create review table, add zipcode, lat, lng information into table
this table will be the main data source we will use in the future
'''
def create_review_table_v2():
    conn = sqlite3.connect(yelp_db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Reviews
       (review_id  CHAR(50)  PRIMARY KEY     NOT NULL,
	   user_id  CHAR(50)   NOT NULL,
	   res_id  CHAR(50)   NOT NULL,
       lat    DECIMAL(12,9),
	   lng  DECIMAL(12,9),
       zipcode        CHAR(10),
	   review_year  INT,
       review_month INT, 
	   review_date  TEXT,
	   text    TEXT,
	   useful   INT,
	   funny INT,
	   cool INT,
	   star   FLOAT)''')
    print ("Table created successfully")
    conn.commit()
    conn.close()


'''
reconstruct business json file, key is restaurant id, value is retaurant dict 
'''
def reconstruct_business_json():
    res_json = dict()
    with open(business_json_path) as inputData:
        for line in inputData:
            try:
                res_dict = json.loads(line.rstrip(';\n'))
                id = res_dict['business_id']
                zipcode = res_dict['postal_code']
                lat = res_dict['latitude']
                lng = res_dict['longitude']
                if not us_lower48_checker(lat, lng, zipcode):
                    continue   
                res_json[id] = res_dict
            except ValueError:
                print("Skipping invalid line" + line)
        with open(res_json_path, 'w') as fp:
            json.dump(res_json, fp)



'''
insert basic information from business.json to res table
'''
def insert_res_from_json():
    conn = sqlite3.connect(yelp_db_path)
    c = conn.cursor()
    with open(business_json_path) as inputData:
        for line in inputData:
            try:
                res_dict = json.loads(line.rstrip(';\n'))
                id = res_dict['business_id']
                name = res_dict['name']
                address = res_dict['address']
                zipcode = res_dict['postal_code']
                lat = res_dict['latitude']
                lng = res_dict['longitude']
                stars = res_dict['stars']
                c.execute("""INSERT INTO Restaurants (id,name,address,zipcode,lat, lng, stars) VALUES \
                (?,?,?,?,?,?,?);""", (id, name, address, zipcode, lat, lng, stars))
                conn.commit()
                #print(id)
            except ValueError:
                print("Skipping invalid line" + line)
    conn.close()


'''
insert basic review information from review.json to review table
'''
def insert_review_from_json():
    conn = sqlite3.connect(yelp_db_path)
    c = conn.cursor()
    with open(res_json_path) as res_file:
        res_json = json.load(res_file)
        with open(review_json_path) as input_data:
            for line in input_data:
                try:
                    rev_dict = json.loads(line.rstrip(';\n'))
                    review_id = rev_dict['review_id']
                    user_id = rev_dict['user_id']
                    res_id = rev_dict['business_id']
                    review_date = rev_dict['date']
                    review_year = review_date.split("-")[0]
                    text = rev_dict['text']
                    star = rev_dict['stars']
                    useful = rev_dict['useful']
                    funny = rev_dict['funny']
                    cool = rev_dict['cool']
                    lat = res_json[res_id]['latitude']
                    lng = res_json[res_id]['longitude']
                    zipcode = res_json[res_id]['postal_code']
                    c.execute("""INSERT INTO Reviews (review_id,user_id,res_id,review_date,review_year,text,star,useful,funny,cool,lat, lng, zipcode) VALUES \
                    (?,?,?,?,?,?,?,?,?,?,?,?,?);""", (review_id,user_id,res_id,review_date,review_year,text,star,useful,funny,cool, lat, lng, zipcode))
                    conn.commit()
                    #print(review_id)
                except:
                    continue
        input_data.close()
    res_file.close()
    conn.close()



'''
version 2: add a new field, review month
insert basic review information from review.json to review table
'''
def insert_review_from_json_v2():
    conn = sqlite3.connect(yelp_db_path)
    c = conn.cursor()
    with open(res_json_path) as res_file:
        res_json = json.load(res_file)
        with open(review_json_path) as input_data:
            for line in input_data:
                try:
                    rev_dict = json.loads(line.rstrip(';\n'))
                    review_id = rev_dict['review_id']
                    user_id = rev_dict['user_id']
                    res_id = rev_dict['business_id']
                    review_date = rev_dict['date']
                    review_year = review_date.split("-")[0]
                    review_month = review_date.split("-")[1]
                    text = rev_dict['text']
                    star = rev_dict['stars']
                    useful = rev_dict['useful']
                    funny = rev_dict['funny']
                    cool = rev_dict['cool']
                    lat = res_json[res_id]['latitude']
                    lng = res_json[res_id]['longitude']
                    zipcode = res_json[res_id]['postal_code']
                    c.execute("""INSERT INTO Reviews (review_id,user_id,res_id,review_date,review_year,review_month, text,star,useful,funny,cool,lat, lng, zipcode) VALUES \
                    (?,?,?,?,?,?,?,?,?,?,?,?,?);""", (review_id,user_id,res_id,review_date,review_year,review_month, text,star,useful,funny,cool, lat, lng, zipcode))
                    conn.commit()
                    #print(review_id)
                except:
                    continue
        input_data.close()
    res_file.close()
    conn.close()


def test_func():
    print('test')

'''
in previous version, review table has no field of review month, 
we could either run creat table and insert data again(time consuming)
or run this function to add field and insert data
'''
def add_review_month_in_review_table(path = yelp_db_path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    
    c.execute('alter table Reviews add column review_month integer')
    conn.commit()
    
    rev_ids = []
    rev_months = []
    rows = c.execute('SELECT review_id, review_date FROM Reviews')
    for row in rows:
        rev_ids.append(row[0])
        #print(row[1])
        rev_months.append(row[1].split("-")[1])
    
    #print(rev_ids)
    #print(rev_months)
    c.executemany('UPDATE Reviews SET review_month = ? WHERE review_id=?', zip(rev_months, rev_ids))
    conn.commit()

    conn.close()


if __name__ == '__main__':
    #create_res_table()
    #print("create review table")
    #create_review_table()

    #print("reconstruct business json")
    #reconstruct_business_json()

    #print("insert review data into sql table")
    #insert_review_from_json()
    add_review_month_in_review_table()