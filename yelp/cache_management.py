import json




def cache_load(cache_path):
    try:
        with open(cache_path) as fp:
            cache = json.load(fp)
            return cache
        fp.close()
    except:
        cache = {}
        with open(cache_path, 'w') as fp:
            json.dump(cache, fp)
        fp.close()
        return cache




def cache_write(cache_path, dict_content):
    with open(cache_path, 'w') as fp:
        json.dump(dict_content, fp)
    fp.close()




def cache_pop(cache_path, key):
    cache = cache_load(cache_path)
    cache.pop(key, None)
    cache_write(cache_path, cache)



def cache_pop_key_start_with(cache_path, start_part_of_key):
    cache = cache_load(cache_path)
    cache_copy = cache.copy()
    for key in cache.keys():
        if key.startswith(start_part_of_key):
            cache_copy.pop(key, None)
    cache_write(cache_path, cache_copy)
    return cache_copy.keys()