#### important data
```
res.json
rev.json
path: drive/data/
description: reformated and cleaned yelp data, res.json inlcude all resturant data, rev.json inlude all review data, 
in those two json file, a dict is provided, in dict, key is id.
------------------------------------------------------------------

Zillow_gentrification.csv 
path: drive/data/Zillow_gentrification.csv 
description: merge zillow data with gentrification eligibility data by year and zipcode, 5 zillow metrics have been chosen, all NA values have been removed. our baseline method is based on this data 
-----------------------------------------------------------------

Yelp_gentrification
formate1: sql table(year, zipcode, gentrification status, yelp review ids in this year and zipcode, num of reviews), already filter out 0 reviews record
path: drive/data/yelp.db

formate2: json 
path: drive/data/yelp_merge_gentri_cache.json (key is year_zipcode), not filter out 0 reviews record
'yelp_info':review_id list, lots of value are empty
descripion: merge yelp review data and gentrification data, our advanced method should base on this data 
-----------------------------------------------------------------

all_rev_ids.json
path: drive/data/
description: all the review ids could be found matched with gentrification data, do not extract features from review not in this cluster... it's not helpful in training models
------------------------------------------------------------------


```

#### environment setting before running code
```
#clone github to local, in terminal 
1. git init
2. git clone https://github.com/imyixiao/gentrification.git
3. cd gentrification

#set environment
conda env create -f ./new_env.yaml

#activate environmrnt
source activate new_env

#if you want to deactivate environment 
source deactivate new_env

#when you run functions, should activate environment
```
