from variable_collections import rev_json_path, rev_nlp_json_path
from cache_management import cache_load, cache_write

'''
extract nlp feature and keep them in json file
just template on how things work, if you want to use hadoop, or any other tech
feel free to change details 

YOU JOB HERE:
1. add different extract feature functions to extract different nlp feature, each function is used to extract one feature 
2. after finish that function, add the information of feature name, and feature function name in table 
   - 'text_len' , extract_feature_text_len() (an example)
   - 
   -
   -

3. run add_feature function to save the feature in local file for further analysis 
'''

'''
read review json file, and get text, review id 
for each record, apply your "extract_feature" function to extract one feature
and save nlp feature in rev_nlp_json_path

in my local set, i set rev_json_path, rev_nlp_json_path in variable_collections file, feel free to use your own
by not using default value
'''
def add_feature(feature_name, extract_feature_function ,rev_cache_path = rev_json_path, rev_nlp_cache_path = rev_nlp_json_path):
    rev_dict = cache_load(rev_cache_path)
    rev_nlp_dict = cache_load(rev_nlp_cache_path)
    for k, v in rev_dict.items():
        review_id = k
        text = v['text']
        feature = extract_feature_function(text)
        if review_id not in rev_nlp_dict:
            rev_nlp_dict[review_id] = {}
        rev_nlp_dict[review_id][feature_name] = feature
    cache_write(rev_nlp_cache_path, rev_nlp_dict)



#just a example 
def get_text_len(text):
    return text.length


if __name__ == "__main__":
    add_feature('text_len', get_text_len)