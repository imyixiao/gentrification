import sqlite3
from variable_collections import yelp_db_path, yelp_merge_gentr_cache, res_json_path
from cache_management import cache_load, cache_write
'''
for each record, get restaurant ids, unique 
get top 20 categories from those restaurants, save all category result

list all top 20 categories, 
and at the same time, get frequence of those category appear in records
'''


def category_feature_extract():
	merge_yelp_cache = cache_load(yelp_merge_gentr_cache)
	res_cache = cache_load(res_json_path)
	category_dict = dict()
	conn = sqlite3.connect(yelp_db_path)
	c = conn.cursor()
	c.execute("SELECT year, zipcode FROM Yelp_gentrification")
	rows = c.fetchall()
	for row in rows:
    	year = row[0]
		zipcode = row[1]
		key = year + "_" + zipcode
		gentri_status = merge_yelp_cache[key]['gentri_status']
		yelp_info = merge_yelp_cache[key]['yelp_info']
		res_all = set()
		for info in yelp_info:
				res_all.add(info[2])

 



if __name__ == "__main__":
    pass 
