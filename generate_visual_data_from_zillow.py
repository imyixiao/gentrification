import pandas 

from variable_collections import zillow_path, cols_needed


'''
functions here will be used to satify different requirements of data preparation for 
data visualization
'''


'''
input: zillow_path
output: get part of cols information from Zip_time_series, and save in zip_part_time_zeries
with required cols including time(format as yyyy-mm), zipcode, 
and optional cols in cols needed 
'''
def generate_part_info_csv_table(zillow_part_info_path, zipcode, cols_optional = cols_needed):
    zillow_whole = pandas.read_csv(zillow_path)
    cols = ['Date','RegionName']
    cols.extend(cols_optional)
    
    all_vals = dict()
    for c in cols:
        all_vals[c] = [] 
    
    for index, row in zillow_whole.iterrows():
        if index > 10:
            break;
        if str(row['RegionName']) != (str(zipcode)):
            continue
        date_list = row['Date'].split("-")
        new_date = date_list[0] + "-" + date_list[1]
        all_vals['Date'].append(new_date)
        all_vals['RegionName'].append(zipcode)
        for opt_col in cols_optional:
            all_vals[opt_col].append(row[opt_col])
    
    zillow_part = pandas.DataFrame(all_vals)
    zillow_part.to_csv(zillow_part_info_path, encoding='utf-8', index=False)
    return zillow_part


if __name__ == "__main__":
    generate_part_info_csv_table('./data/zillow_part.csv', 44113)  
