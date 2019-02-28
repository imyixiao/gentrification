from variable_collections import yelp_db_path, gentrification_db_path, baseline_cache_path, zillow_db_path, gentri_chunk_cache_path, yelp_merge_gentr_cache, sep_yelp_db
from cache_management import cache_load, cache_write
import sqlite3


'''
seperate gentrification to chunks to finish task seperately
avoid crash~ 
'''
def seperate_gentri_to_chunks(gentri_path, cache_path):
    c = cache_load(cache_path)
    if c:
        return len(c.keys())

    conn = sqlite3.connect(gentri_path)
    c = conn.cursor()
    c.execute("SELECT year, RegionName_zip, eligible_gentrification FROM gentrification")
    rows = c.fetchall()

    num = 0
    count = 0
    chunk = []
    for row in rows:
        if count >= 100:
            cache = cache_load(cache_path)
            key = "chunk" + str(num)
            cache[key] = chunk
            cache_write(cache_path, cache)
            num += 1
            count = 0
            chunk = []

        chunk.append(row)
        count += 1
    
    if len(chunk) > 0:
        cache = cache_load(cache_path)
        key = "chunk" + str(num)
        cache[key] = chunk
        cache_write(cache_path, cache)
        num += 1
    
    conn.close()
    
    return num



def sep_yelp_table(yelp_db_path, min_year, max_year, new_yelp_db):
    conn = sqlite3.connect(yelp_db_path)
    c = conn.cursor()

    for i in range(max_year - min_year):
        year = min_year + i
        c.execute("Select review_id, user_id, res_id, zipcode from Reviews where review_year = ?" , (year, ))
        rows = c.fetchall()

        state = "CREATE TABLE IF NOT EXISTS yelp_" + str(year)
        state += "(review_id  CHAR(50)  PRIMARY KEY     NOT NULL, \
        user_id  CHAR(50)   NOT NULL,\
	    res_id  CHAR(50)   NOT NULL,\
        zipcode        CHAR(10),\
	    year  INT)"

        c.execute(state)
        print ("Table created successfully")
        conn.commit()

        review_id = []
        user_id = []
        res_id = []
        zipcode = []
        years = []

        for row in rows:
            review_id.append(row[0])
            user_id.append(row[1])
            res_id.append(row[2])
            zipcode.append(row[3])
            years.append(year)
        
        state = "INSERT INTO yelp_" + str(year)
        state += " (review_id, user_id, res_id, zipcode, year) VALUES (?,?,?,?,?);"
        c.executemany(state, zip(review_id, user_id, res_id, zipcode, years))
        print("insert one year successully")
        conn.commit()
    
    conn.close()
    



'''
return yelp query res
and write to cache
'''
def query_yelp_with_year_and_zip(gentri_chunk_cache_path, yelp_db, res_cache_path, chunk_id, tol):
    gentri_chunk_cache = cache_load(gentri_chunk_cache_path)
    if not gentri_chunk_cache:
        gentri_chunk_cache = seperate_gentri_to_chunks(gentrification_db_path, gentri_chunk_cache_path)
    
    key = "chunk" + str(chunk_id)
    gentri_rows = gentri_chunk_cache[key]

    conn = sqlite3.connect(yelp_db)
    c = conn.cursor()
    cache = cache_load(res_cache_path)

    for row in gentri_rows:
        year = row[0]
        zipcode = row[1]
        gentri_status = row[2]
        state = "Select review_id, user_id, res_id from yelp_" + str(year)
        state += " where year = ? and zipcode = ?"
        c.execute(state, (year, zipcode))
        res = c.fetchall()
        key = str(year) + "_" + str(zipcode)
        print(key)
        val = dict()
        val['gentri_status'] = gentri_status
        val['yelp_info'] = res
        cache[key] = val
    
    cache_write(res_cache_path, cache)
    print(str(chunk_id) + " of " + str(tol) + " finished!")



if __name__ == "__main__":
    #print(seperate_gentri_to_chunks(gentrification_db_path, './data/gentri_chunk.json'))
    
    num = seperate_gentri_to_chunks(gentrification_db_path, gentri_chunk_cache_path)
    for i in range(num):
        query_yelp_with_year_and_zip(gentri_chunk_cache_path, yelp_db_path, yelp_merge_gentr_cache, i, num - 1)
    
    #sep_yelp_table(yelp_db_path, 2012, 2018, sep_yelp_db)
