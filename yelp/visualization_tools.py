from data_prep_for_visualization import retreive_restaurant_category_by_zipcode
from data_prep_for_visualization import get_all_categories_sorted_by_total_freq
from data_prep_for_visualization import get_timeseri_category_data
from retrieve_sql_database_functions import select_all_zillow_records_by_zipcode
from variable_collections import sql_cache_path
from cache_management import cache_load, cache_pop_key_start_with
from gentrification_eligibility import check_gentrification_eligibility
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


def plot_category_and_zillow_timeseri(category, zipcode, zillow_metric):
    
    #choose one category and check its time series data in this zipcode
    category_seri = get_timeseri_category_data(category, zipcode)
    print("category time seri data : ")
    print(category_seri)

    #get house prices seri data in this zipcode could choose metrics we want
    house_price_seri = select_all_zillow_records_by_zipcode(zipcode, fields = [zillow_metric])
    print("house price time seri data : " )
    print(house_price_seri)

    category_time = []
    category_freq = []
    for pair in category_seri:
        category_time.append(pair[0])
        category_freq.append(pair[1])
    
    house_time = []
    house_price = []
    gentri_status = []
    prev_year = 0
    prev_statu = 0
    for pair in house_price_seri:
        house_time.append(pair[0])
        house_price.append(pair[1])
        cur_year = pair[0].split("-")[0]
        if cur_year != prev_year:
            if check_gentrification_eligibility(zipcode, cur_year) == 'Eligible':
                res = 1
            else:
                res = 2
            gentri_status.append(res)
            prev_year = cur_year
            prev_statu = res
        else:
            gentri_status.append(prev_statu)
    
    #print(category_time)
    #print(category_freq)

    #10000 is eligible, 20000 is not 
    plt.plot(category_time, [c * 1000 for c in category_freq], 'r--', label='category line')
    plt.plot(house_time, house_price, 'bs', label= 'zillow ' + zillow_metric)
    plt.plot(house_time, [s * 10000 for s in gentri_status], 'g^', label = "eligibility")
    plt.legend(loc='upper right')
    plt.show()


if __name__ == "__main__":
    plot_category_and_zillow_timeseri('italian', '44113', 'ZHVI_SingleFamilyResidence')