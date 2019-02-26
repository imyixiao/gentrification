from data_prep_for_visualization import retreive_restaurant_category_by_zipcode
from data_prep_for_visualization import get_all_categories_sorted_by_total_freq
from data_prep_for_visualization import get_timeseri_category_data
from retrieve_sql_database_functions import select_all_zillow_records_by_zipcode
from variable_collections import sql_cache_path
from cache_management import cache_load, cache_pop_key_start_with
from gentrification_eligibility import check_gentrification_eligibility
from visualization_tools import plot_category_and_zillow_timeseri
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt





if __name__ == '__main__':
    #use zipcode 44113 as our case analysis neighborhood
    print(get_all_categories_sorted_by_total_freq(84047))
    #given restaurant category, zipcode, metrics, and plot
    #plot_category_and_zillow_timeseri('italian', '83402', 'ZHVI_SingleFamilyResidence')












    

    
    
