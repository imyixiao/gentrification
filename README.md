#### my folder structure
```
gentrification/
  code(my github repo)/
     baseline_method.py
     ...(all code)
     data/
        baseline_cache.json
        sql_cache.json
  yelp_data/
     business.json
     res.json
     review.json
     yelp.db
```

##### transfer_json_to_sql.py
```
script:
python3 transfer_json_to_sql.py

result:
res.json -> reconstruct business.json, key would be restaurant id, which will be used to retreive res info by review 
(sqlite table) review -> include review info and restaurant location information 
```

##### transfer_csv_to_sql.py
```
transfer zillow csv file to sql
```


##### variable_collections.py
```
all global variables, could be imported to different files
```

##### inside_boundary_checker.py
```
input: lat, lng, shp file
output: boolean, true if in boundary, false if not in boundary
```

##### retrieve_sql_database_functions.py
```
To satisfy different retrieval requirements (for example retrieve all restaurants in one zipcode, and etc), 
lots of functions would be created in this file to be used in the future.  
```

##### generate_visual_data_from_zillow.py
```
contains functions to satisify different data preparation requirements for visualization
```

##### baseline_method.py
```
baseline method code
```