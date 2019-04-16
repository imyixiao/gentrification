import sqlite3
from variable_collections import yelp_db_path, yelp_merge_gentr_cache, res_json_path
from cache_management import cache_load, cache_write
import operator
import math
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd

import pandas
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

'''
for each record, get restaurant ids, unique 
get top 20 categories from those restaurants, save all category result

list all top 20 categories, 
and at the same time, get frequence of those category appear in records
'''

def category_feature_extract():

    merge_yelp_cache = cache_load(yelp_merge_gentr_cache)
    res_cache = cache_load(res_json_path)

    category_dict_top20 = dict() #global top 20 distribution
    category_distribution_cache = dict() # key->year_zipcode, value->dict, distribution

    print("fetch data from sql")
    conn = sqlite3.connect(yelp_db_path)
    c = conn.cursor()
    c.execute("SELECT year, zipcode FROM Yelp_gentrification")
    rows = c.fetchall()

    print("traverse all records")
    for row in rows:
        year = row[0]
        zipcode = row[1]
        key = str(year) + "_" + zipcode
        
        sub_category_distribution = dict()
        res_all = set( info[2] for info in merge_yelp_cache[key]['yelp_info'])

        for res in res_all:
            try:
                category_list = res_cache[res]['categories'].split(",")
                for c in category_list:
                    lower_c = c.lower().strip()
                    if lower_c not in sub_category_distribution:
                        sub_category_distribution[lower_c] = 0
                    sub_category_distribution[lower_c] += 1
            except:
                continue

        category_distribution_cache[key] = sub_category_distribution
        print(sub_category_distribution)
        sorted_category = sorted(sub_category_distribution.items(), key=operator.itemgetter(1), reverse = True)
        

        for i in range(math.ceil(len(sorted_category) * 0.1)):
            if sorted_category[i][0] not in category_dict_top20:
                category_dict_top20[sorted_category[i][0]] = 0
            category_dict_top20[sorted_category[i][0]] += 1
        
        print("finish one record!")

    cache_write('../category_top20.json', category_dict_top20)
    cache_write('../category_distribution.json', category_distribution_cache,)

def sort(limit = 50):
    category_top20 = cache_load('../category_top20.json')
    sorted_category = sorted(category_top20.items(), key=operator.itemgetter(1), reverse = True)
    return sorted_category

def draw(limit = 50):
    sorted_category = sort(limit)
    x = []
    y = []
    labels = []
    ymin = 10000
    ymax = 0

    for i in range(len(sorted_category)):
        if i >= limit:
            break
        category = sorted_category[i][0]
        num = sorted_category[i][1]
        y.append(num)
        x.append(i)
        labels.append(category)
        i += 1
        if num < ymin:
            ymin = num 
        if num > ymax:
            ymax = num
    
    plt.barh(range(limit), y, height=0.7, color='green', alpha=0.8)     
    plt.yticks(range(limit), labels)
    plt.xlim(ymin, ymax)
    plt.xlabel("Frequance of being popular category in neighborhoods")
    for px, py in enumerate(y):
        plt.text(py + 0.2, px - 0.1, '%s' % py)
    plt.show()


def add_top_category_feature_and_build_csv(limit = 50):
    csv_dict = dict()
    category_distribution_cache = cache_load("../category_distribution.json")

    print("fetch data from sql")
    conn = sqlite3.connect(yelp_db_path)
    c = conn.cursor()
    c.execute("SELECT year_zip, gentri_status FROM Yelp_gentrification")
    rows = c.fetchall()

    sorted_category = sort(limit)
    i = 0
    for pair in sorted_category:
        if i >= limit:
            break
        c = pair[0]
        vals = []
        for row in rows:
            key = row[0]
            category_dict = category_distribution_cache[key]
            if c in category_dict:
                vals.append(category_dict[c])
            else:
                vals.append(0)
        csv_dict[c] = vals
        i += 1
    
    csv_dict['key'] = [ row[0] for row in rows ]
    csv_dict['gentri_status'] = [ row[1] for row in rows ]
    
    df = pd.DataFrame.from_dict(csv_dict)
    df.to_csv("../category.csv")


def ml_classfier_compare(data_path, res_col, related_cols, model_list, names):
    print(related_cols)
    df = pandas.read_csv(data_path)
    y = df.pop(res_col)
    x = df[related_cols]
    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=17)
    print(X_train)
    for i in range(len(names)):
        model_list[i].fit(X_train, y_train)
        y_pred = model_list[i].predict(X_test)
        print("Model " + names[i] + " Accuracy score : %f" %(accuracy_score(y_test, y_pred)))
        #X_columns = x.columns
        #res = list(zip(X_columns, model_list[i].feature_importances_))
        #print(res)


if __name__ == "__main__":
    #category_feature_extract()
    # sort()
    # add_top_category_feature_and_build_csv(16)

    sorted_category = sort()
    cols_needed = []
    i = 0
    for pair in sorted_category:
        if i >= 16:
            break 
        cols_needed.append(pair[0])
        i += 1
    
    classifiers = [
        KNeighborsClassifier(3),
        SVC(kernel="linear", C=0.025),
        SVC(gamma=2, C=1),
        GaussianProcessClassifier(1.0 * RBF(1.0)),
        DecisionTreeClassifier(max_depth=5),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        MLPClassifier(alpha=1),
        AdaBoostClassifier(),
        GaussianNB()]

    names = ['knn','svc-linear','svc','gaussian','decision tree','random forest','mlp','adaboost','gnb',]
    ml_classfier_compare('../category.csv', 'gentri_status', cols_needed, classifiers, names)
