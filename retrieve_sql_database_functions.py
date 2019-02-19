import sqlite3
from sqlite3 import Error
import json


db_path = "../../yelp.db"
sql_cache_path = "./data/sql_cache.json"


'''
store all functions needed to query records in database, result will be store in cache automatically

cache path and key 
sql_cache_path = "../data/sql_cache.json" will store all sql query result cache, 
the key in the cache is function_name + input param, 
for example, after we search select_all_restaurants_by_zipcode(48105), 
the result will be store under key of select_all_restaurants_by_zipcode_48105

'''


def create_connection():
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        print(e)
    return None



def cache_load(cache_path):
    cache = dict()
    try: 
        cache = json.loads(cache_path)
        return cache
    except:
        with open(cache_path, 'w') as fp:
            json.dump(cache, fp)
        fp.close()
        return cache


'''
input zipcode
output return all restaurants(fields including year and restarant id) in this zipcode 
'''
def select_all_restaurants_by_zipcode(zipcode):
    conn = create_connection()
    cur = conn.cursor()
    key = "select_all_restaurants_by_zipcode_" + str(zipcode) 
    sql_cache = cache_load(sql_cache_path)
    if key not in sql_cache:
        cur.execute(" SELECT res_id, review_year FROM Reviews Where zipcode = ?", (zipcode, ))
        rows = cur.fetchall()
        sql_cache[key] = rows
        with open(sql_cache_path, 'w') as fp:
                json.dump(sql_cache, fp)
        fp.close()
    return sql_cache[key]


if __name__ == "__main__":
    select_all_restaurants_by_zipcode(44115)