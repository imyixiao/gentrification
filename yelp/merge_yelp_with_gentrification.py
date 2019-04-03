from variable_collections import yelp_db_path, gentrification_db_path, baseline_cache_path, zillow_db_path, gentri_chunk_cache_path, yelp_merge_gentr_cache, sep_yelp_db
from cache_management import cache_load, cache_write
import sqlite3
import json
from variable_collections import all_rev_ids_path,rev_json_path, review_json_path, rev_json_clean_path
import ijson

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




'''
filter data with na yelp info
merged data to sql
'''
def merge_data_to_sql(merge_data_cache_path, yelp_db):
    merge_cache = cache_load(merge_data_cache_path)

    keys = []
    years = []
    zipcodes = []
    gentri_status = []
    rev_nums = []
    rev_ids_str = []

    rev_ids_all = []

    for key, val in merge_cache.items():
        if len(val['yelp_info']) == 0:
            continue
        keys.append(key)
        years.append(key.split("_")[0])
        zipcodes.append(key.split("_")[1])
        gentri_status.append(val['gentri_status'])
        rev_ids = []
        for info in val['yelp_info']:
            rev_ids.append(info[0])
        rev_ids_all.extend(rev_ids)
        rev_nums.append(len(rev_ids))
        revs = ",".join(rev_ids)
        rev_ids_str.append(revs)

    all_rev_ids = dict()
    all_rev_ids['all_ids'] = rev_ids_all
    cache_write('./data/all_rev_ids.json',all_rev_ids)

    #create table 
    conn = sqlite3.connect(yelp_db)
    c = conn.cursor()
    state = "CREATE TABLE IF NOT EXISTS Yelp_gentrification\
        (year_zip  CHAR(50)  PRIMARY KEY     NOT NULL, \
        year INT, \
        zipcode     CHAR(10),\
        gentri_status INT, \
        rev_ids  TEXT, \
        rev_num INT)"
    c.execute(state)
    print ("Table created successfully")
    conn.commit()
    
    #insert data into table 
    state = "INSERT INTO Yelp_gentrification (year_zip, year, zipcode, gentri_status, rev_ids, rev_num) VALUES (?,?,?,?,?,?);"
    c.executemany(state, zip(keys, years, zipcodes, gentri_status, rev_ids_str, rev_nums))
    print("insert successully")
    conn.commit()

    conn.close()


def reformate():
    reformated_rev_info = dict()
    with open(review_json_path) as input:
        for line in input:
            res_dict = json.loads(line.rstrip(';\n'))
            review_id = res_dict['review_id']
            business_id = res_dict['business_id']
            user_id = res_dict['user_id']
            text = res_dict['text']
            info = dict()
            info['user_id'] = user_id
            info['res_id'] = business_id
            info['text'] = text
            reformated_rev_info[review_id] = info
            print("add one record!")
    print("start to save!")
    with open(rev_json_path, 'w') as fp:
        json.dump(reformated_rev_info, fp)

# '''
# all_rev_ids_path:all rev_ids we need
# rev_json_path: the json file we need created, key is review id(only select in all_rev_ids collections)
# review_json_path: original review files 
# '''
# def review_json_clean_and_reformat():
#     with open("../rev_reformated.json", "r") as f:
#         reformated_rev_info = json.load(f)
#     f.close()
#     print("here")
#     all_ids = cache_load(all_rev_ids_path)['all_ids']
#     selected_rev_info = dict()
#     print("start to select!")
#     for id in all_ids:
#         print(id)
#         selected_rev_info[id] = reformated_rev_info[id]
#     print("final step!")
#     with open(rev_json_clean_path, 'w') as fp:
#         json.dump(selected_rev_info, fp)



if __name__ == "__main__":
    #print(seperate_gentri_to_chunks(gentrification_db_path, './data/gentri_chunk.json'))
    '''
    num = seperate_gentri_to_chunks(gentrification_db_path, gentri_chunk_cache_path)
    for i in range(num):
        query_yelp_with_year_and_zip(gentri_chunk_cache_path, yelp_db_path, yelp_merge_gentr_cache, i, num - 1)
    '''
    #sep_yelp_table(yelp_db_path, 2012, 2018, sep_yelp_db)
    #merge_data_to_sql(yelp_merge_gentr_cache, yelp_db_path)
    # cache = cache_load('./data/all_rev_ids.json')
    # print(len(cache['all_ids']))
    #reformate()
    #review_json_clean_and_reformat()
    f = open(rev_json_path, 'r')
    obj = ijson.items(f, 'JG3RmJwtIELWIGNoCfDGeA')
    for o in obj:
        print(str(o))