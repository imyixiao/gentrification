import sqlite3
from variable_collections import yelp_db_path

'''
for each record, get restaurant ids, unique 
get top 20 categories from those restaurants, save all category result

list all top 20 categories, 
and at the same time, get frequence of those category appear in records
'''
def category_feature_extract():
    conn = sqlite3.connect(yelp_db_path)
    c = conn.cursor()
    c.execute("SELECT year, zipcode, gentri_status,rev_ids,rev_num FROM Yelp_gentrification")
    rows = c.fetchall()
    for row in rows:
        year = row[0]
        zipcode = row[1]
        gentri_status = row[2]
        rev_id_list



if __name__ == "__main__":
    pass 