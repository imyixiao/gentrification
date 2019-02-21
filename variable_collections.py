'''
cache for baseline method
'''
baseline_cache_path = "./data/baseline_cache.json"


'''
restaurant json path (different from business json in format)
in business json, there are multiple dict (each for one restaurant)
in restaurant json, only one dict, key would be restaurant id for fast query restaurant
'''
res_json_path = '../yelp_data/res.json'


'''
zillow time series data by zipcode
'''
zillow_path = "../zillow_data/Zip_time_series.csv"


'''
yelp databse path
'''
db_path = "../yelp_data/yelp.db"


'''
when query sql database, cache is stored for furture use 
'''
sql_cache_path = "./data/sql_cache.json"


'''
zillow csv has lots of cols, and with huge data amount, 
we have functions of extracting part of cols vals and save in sql, 
required cols are cols always in new csv
opt cols are cols we want add in the base of required cols 
'''
cols_required = ['Date', 'RegionName']
cols_opt = ['MedianListingPrice_AllHomes','MedianListingPrice_CondoCoop','MedianListingPrice_SingleFamilyResidence','MedianListingPrice_DuplexTriplex']
cols_all = {} # key : colname , value : index in csv file

'''
business.json and review.json from yelp dataset website
'''
business_json_path = '../yelp_data/business.json'
review_json_path = '../yelp_data/review.json'