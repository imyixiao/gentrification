import json
from retrieve_sql_database_functions import select_all_restaurants_by_zipcode, cache_load
from transfer_json_to_sql import reconstruct_business_json
import operator
from variable_collections import baseline_cache_path, res_json_path



'''
input: zipcode
output: dict, key would be category, and value would be dict (key would be time(formate as yyyy-mm), value would be frequency)
'''
def retreive_restaurant_category_by_zipcode(zipcode):
    baseline_cache = cache_load(baseline_cache_path)
    if zipcode not in baseline_cache:

        res_by_zipcode_list = select_all_restaurants_by_zipcode(zipcode)
        category_dictribution_by_zipcode = dict()
        category_tol = dict()

        res_cache_temp = cache_load(res_json_path)
        if not res_cache_temp:
            reconstruct_business_json()
            res_json = cache_load(res_json_path)
        else:
            res_json = res_cache_temp

        for triple in res_by_zipcode_list:
            res_id = triple[0]
            year = triple[1]
            month = triple[2]
            if month < 10:
                alter_month = "0" + str(month)
            else:
                alter_month = str(month)
            time = str(year) + "-" + alter_month
            res_info = res_json[res_id]

            try:
                categories = res_info['categories'].split(",")
                for c in categories:
                    c = c.strip().lower()
                    if(len(c) == 0):
                        continue
                    if c not in category_dictribution_by_zipcode:
                        category_dictribution_by_zipcode[c] = dict()
                        category_tol[c] = 0
                    if time not in category_dictribution_by_zipcode[c]:
                        category_dictribution_by_zipcode[c][time] = 0
                    category_dictribution_by_zipcode[c][time] += 1
                    category_tol[c] += 1
            except:
                continue
        
        baseline_cache[zipcode] = category_dictribution_by_zipcode
        baseline_cache[(str(zipcode) + "tol")] = sorted(category_tol.items(), key=operator.itemgetter(1), reverse = True)

        with open(baseline_cache_path, 'w') as fp:
            json.dump(baseline_cache, fp)
        fp.close()
        
    return baseline_cache




'''
input: zipcode 
output: list of categories of restaurant in this zipcide neighborhood, sorted by number of freq
'''
def get_all_categories_sorted_by_total_freq(zipcode):
    baseline_cache = cache_load(baseline_cache_path)
    if zipcode not in baseline_cache:
        retreive_restaurant_category_by_zipcode(zipcode)
    return [l[0] for l in baseline_cache[(str(zipcode) + "tol")]]




'''
input: category, zipcode
output: dictionary, key is time(formate as yyyy-mm), value is freq, 
'''
def get_timeseri_category_data(category, zipcode):
    res_distribution = retreive_restaurant_category_by_zipcode(zipcode)
    try:
        output = res_distribution[zipcode][category]
        sorted_output = sorted(output.items(), key=operator.itemgetter(0))
        return sorted_output
    except:
        print("category can not be found in this zipcode")