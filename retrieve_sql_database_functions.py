import sqlite3
from sqlite3 import Error
import json
from variable_collections import yelp_db_path, sql_cache_path, cols_opt, zillow_db_path



'''
store all functions needed to query records in database, result will be store in cache automatically

cache path and key 
sql_cache_path = "../data/sql_cache.json" will store all sql query result cache, 
the key in the cache is function_name + input param, 
for example, after we search select_all_restaurants_by_zipcode(48105), 
the result will be store under key of select_all_restaurants_by_zipcode_48105

'''


def create_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        print(e)
    return None



def cache_load(cache_path):
    try:
        with open(cache_path) as fp:
            cache = json.load(fp)
            return cache
        fp.close()
    except:
        cache = {}
        with open(cache_path, 'w') as fp:
            json.dump(cache, fp)
        fp.close()
        return cache


'''
input zipcode
output return all restaurants(fields including year and restarant id) in this zipcode 
'''
def select_all_restaurants_by_zipcode(zipcode):
    conn = create_connection(yelp_db_path)
    cur = conn.cursor()
    key = "select_all_restaurants_by_zipcode_" + str(zipcode) 
    sql_cache = cache_load(sql_cache_path)
    if key not in sql_cache:
        cur.execute(" SELECT res_id, review_year, review_month FROM Reviews Where zipcode = ?", (zipcode, ))
        rows = cur.fetchall()
        sql_cache[key] = rows
        with open(sql_cache_path, 'w') as fp:
                json.dump(sql_cache, fp)
        fp.close()
    return sql_cache[key]



'''
input zipcode, list of fields needed (optional)
output return all zillow record in this zipcode
'''
def select_all_zillow_records_by_zipcode(zipcode, fields = cols_opt, table_name = "Zillow"):
    conn = create_connection(zillow_db_path)
    cur = conn.cursor()
    key = "select_all_zillow_records_by_zipcode_" + str(zipcode) + str(fields)
    sql_cache = cache_load(sql_cache_path)

    if key not in sql_cache:

        state = " SELECT Date ,"
        for index, f in enumerate(fields):
            state += f
            if index != len(fields) - 1:
                state += " ,"
        state += " FROM "
        state += table_name
        state += " WHERE RegionName = ?"
        
        cur.execute(state, (zipcode, ))
        rows = cur.fetchall()
        sql_cache[key] = rows

        with open(sql_cache_path, 'w') as fp:
                json.dump(sql_cache, fp)
        fp.close()

    return sql_cache[key]


if __name__ == "__main__":
    print(select_all_restaurants_by_zipcode('44859'))
    print(select_all_zillow_records_by_zipcode('44859'))