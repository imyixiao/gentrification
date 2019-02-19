import json
from retrieve_sql_database_functions import select_all_restaurants_by_zipcode, cache_load
import operator



baseline_cache_path = "./data/baseline_cache.json"
res_json_path = '../data/res.json'


'''
input: zipcode
output: dict, key would be category, and value would be dict (key would be year, value would be frequency)
'''
def retreive_restaurant_category_by_zipcode(zipcode):
    baseline_cache = cache_load(baseline_cache_path)
    if zipcode not in baseline_cache:
        res_by_zipcode_list = select_all_restaurants_by_zipcode(zipcode)
        category_dictribution_by_zipcode = dict()
        zipcode_tol = dict()
        res_json = cache_load(res_json_path)
        for tuple_pair in res_by_zipcode_list:
            res_id = tuple_pair[0]
            year = tuple_pair[1]
            res_info = res_json[res_id]
            for c in res_info['categories']:
                if c not in category_dictribution_by_zipcode:
                    category_dictribution_by_zipcode[c] = dict()
                    zipcode_tol[c] = 0
                if year not in category_dictribution_by_zipcode[c]:
                    category_dictribution_by_zipcode[c][year] = 0
                category_dictribution_by_zipcode[c][year] += 1
                zipcode_tol[c] += 1
        baseline_cache[zipcode] = category_dictribution_by_zipcode
        baseline_cache[(str(zipcode) + "tol")] = zipcode_tol
        with open(baseline_cache_path, 'w') as fp:
                json.dump(baseline_cache, fp)
        fp.close()
    return baseline_cache[zipcode]




'''
input: zipcode 
output: list of categories of restaurant in this zipcide neighborhood, sorted by number of freq
'''
def get_all_categories_sorted_by_total_freq(zipcode):
    baseline_cache = cache_load(baseline_cache_path)
    if zipcode not in baseline_cache:
        retreive_restaurant_category_by_zipcode(zipcode)
    category_distribution = baseline_cache[(str(zipcode) + "tol")]
    sorted_category = sorted(category_distribution.items(), key=operator.itemgetter(1))
    return sorted_category




'''
input: category, zipcode
output: dictionary, key is year, value is freq, 
'''
def get_timeseri_category_data(category, zipcode):
    res_distribution = retreive_restaurant_category_by_zipcode(zipcode)
    try:
        output = res_distribution[category]
        return output
    except:
        print("category can not be found in this zipcode")



if __name__ == '__main__':
    #print(retreive_restaurant_category_by_zipcode(44113))
    print(get_all_categories_sorted_by_total_freq(44113))