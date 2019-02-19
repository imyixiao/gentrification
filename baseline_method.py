import json

cache_path = "cache.json"


'''
input: zipcode
output: dic of review cluster, key is year and value is dict (key is res id, and value is times of that res in reviews), saved as json
use cache 
'''
def retrieve_all_review_by_zipcode(zipcode, yelp_database_path, cache_path):
    cache = json.loads(cache_path)
    if zipcode in cache.Keys():
        return cache[zipcode]
    else:
        output = dict()
        



def retreive_restaurant_category_by_zipcode(zipcode):
    #retrieve_all_review_by_zipcode(zipcode)
    #for each year, get category distribution 
    ## consider weight? or not 
    #save json file 
    pass


if __name__ == '__main__':
    #dovisulization
    pass