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
gentrification yearly eligibility and status by zipcode and cbsa
'''
gentrification_path = "zillow_data/gentrifying_and_eligible_neighborhoods.csv"


'''
yelp databse path
'''
yelp_db_path = "../yelp.db"
zillow_db_path = "../zillow.db"
gentrification_db_path = "../gentrification.db"


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
cols_opt = ['ZHVIPerSqft_AllHomes', 'ZHVI_1bedroom', 'ZHVI_2bedroom','ZHVI_3bedroom', 'ZHVI_4bedroom', 'ZHVI_5BedroomOrMore','ZHVI_AllHomes', 'ZHVI_BottomTier', 'ZHVI_CondoCoop', 'ZHVI_MiddleTier','ZHVI_SingleFamilyResidence', 'ZHVI_TopTier', 'ZRI_AllHomes']
cols_all = {} # key : colname , value : index in csv file

'''
business.json and review.json from yelp dataset website
'''
business_json_path = '../yelp_data/business.json'
review_json_path = '../yelp_data/review.json'


gentrification_eligibility_path = './data/gentrification_eligibility.csv'