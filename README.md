##### transfer_json_to_sql.py
```
script:
python3 transfer_json_to_sql.py

result:
res.json -> reconstruct business.json, key would be restaurant id, which will be used to retreive res info by review 
(sqlite table) review -> include review info and restaurant location information 
```

##### inside_boundary_checker.py
```
input: lat, lng, shp file
output: boolean, true if in boundary, false if not in boundary
```

##### acs_access.py
```
input: zipcode, year
output: education attainment / Median Household Income / 
```

##### retrieve_sql_database_functions.py
```
To satisfy different retrieval requirements (for example retrieve all restaurants in one zipcode, and etc), lots of functions would be created in this file to be used in the future.  
```