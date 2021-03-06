import sqlite3
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sklearn
from matplotlib.colors import ListedColormap

from variable_collections_Jordan import zillow_db_path, gentrification_db_path, baseline_cache_path, zillow_path
from cache_management import cache_write, cache_load
from transfer_csv_to_sql import read_csv_header, create_zillow_table, read_csv_header_list

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

# gentrifying

def query_gentrification(gentrification_db_path):
    conn = sqlite3.connect(gentrification_db_path)
    c = conn.cursor()
    c.execute('SELECT year, RegionName_zip, gentrifying FROM gentrification')
    rows = c.fetchall()
    conn.close()
    return rows



def query_zillow(zillow_db_path, gentrification_db_path):
    rows = query_gentrification(gentrification_db_path)
    
    conn = sqlite3.connect(zillow_db_path)
    c = conn.cursor()

    ids = []
    status = []

    for row in rows:
        year = row[0]
        zip = row[1]
        eligi = row[2]
        c.execute(" SELECT id FROM Zillow Where year = ? and RegionName = ?", (year,zip ))
        res = c.fetchone()
        if res is not None:
            print(res[0])
            ids.append(res[0])
            status.append(eligi)
    
    res_dict = {}
    res_dict['ids'] = ids
    res_dict['status'] = status

    cache_write(baseline_cache_path, res_dict)
    conn.close()
    


def update_zillow():
    cache = cache_load(baseline_cache_path)
    ids = cache['ids']
    status = cache['status']

    conn = sqlite3.connect(zillow_db_path)
    c = conn.cursor()
    c.executemany('UPDATE Zillow SET  gentrifying = ? WHERE id=?', zip(status, ids))
    conn.commit()
    conn.close()



def get_useful_zillow_record():
    conn = sqlite3.connect(zillow_db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM Zillow WHERE gentrifying = 0 or gentrifying = 1")
    rows = c.fetchall()
    cache = cache_load(baseline_cache_path)
    cache['useful_zillow'] = rows
    cache_write(baseline_cache_path, cache)
    conn.close()
    return rows



'''
lots of zillow metrics data are missing 
this step is to choose metrics with less missing data, 
bars means 0.1 percent of missing values 

return, dict, key is col_name of zillow csv file, value is index in zillow sql table
'''
def choose_zillow_metrics(bar = 0.1):
    cache = cache_load(baseline_cache_path)
    if 'useful_zillow' in cache:
        rows = cache['useful_zillow']
    else:
        rows = get_useful_zillow_record()
        
    #get sorted cols in zillow with only zillow metrics
    headers_sorted = read_csv_header_list(zillow_path)
    remove_cols = ['RegionName', 'Date']

    #first 5 is not zillow metrics, and the very last index, the structure is [()()], each tuple has 80 long
    cols_na_count = {}
    cols_index = {}
    index = 5
    rows_len = len(rows)
    for c in headers_sorted:
        if c in remove_cols:
            continue
        cols_na_count[c] = 0
        cols_index[c] = index
        index += 1

    for row in rows:
        for col_name, index in cols_index.items():
            if col_name not in cols_na_count:
                continue
            if row[index] == 0:
                cols_na_count[col_name] += 1
                if cols_na_count[col_name] >= bar * rows_len:
                    cols_na_count.pop(col_name, None)
    
    
    res_dict = {}
    for col_name, val in cols_na_count.items():
        res_dict[col_name] = cols_index[col_name]
    
    return res_dict



'''
create sql table for chosen zillow col metrics
'''
def create_sql_table_for_useful(table_name, zillow_db_path, bar = 0.1):
    zillow_metrics = choose_zillow_metrics(bar)
    conn = sqlite3.connect(zillow_db_path)
    c = conn.cursor()
    state = "CREATE TABLE IF NOT EXISTS " + table_name
    state += "  (id  CHAR(50) PRIMARY KEY, " \
       " year  INT  , " \
       " RegionName CHAR(10), " \
       " gentrifying INT"
    for col in list(zillow_metrics.keys()):
        state += "," + str(col) + "   INT "
    state += ")"
    #print(state)
    c.execute(state)
    print ("table created successfully")
    conn.commit()
    conn.close()


'''
before insert data, prepare data for insertation 
'''
def data_prep_before_insert(baseline_cache_path, bar = 0.1):
    cache = cache_load(baseline_cache_path)
    if 'useful_zillow' in cache:
        rows = cache['useful_zillow']
    else:
        rows = get_useful_zillow_record()

    zillow_metrics = choose_zillow_metrics(bar)
    zillow_metrics['id'] = 0
    zillow_metrics['year'] = 2
    zillow_metrics['RegionName'] = 4
    zillow_metrics['gentrifying'] = 79
    #print(zillow_metrics.keys())

    vals_dict = {}
    for c in list(zillow_metrics.keys()):
        vals_dict[c] = []
    
    for row in rows:
        for col_name, index in zillow_metrics.items():
            vals_dict[col_name].append(row[index])
    
    print(vals_dict.keys())
    return vals_dict


'''
insert data, without any NA
'''
def insert_data_into_table(baseline_cache_path, zillow_db_path, table_name, bar = 0.1):
    vals_dict = data_prep_before_insert(baseline_cache_path, bar)
    
    conn = sqlite3.connect(zillow_db_path)
    c = conn.cursor()

    state = "INSERT INTO " + table_name + " ("
    after = ""
    vals = []
    order_dict = {}
    index = 0
    for col in list(vals_dict.keys()):
        state += col
        state += ","
        after += "?,"
        vals.append(vals_dict[col])
        order_dict[index] = col
        index += 1
    
    state = state[:-1]
    state += ") VALUES ("
    state += after[:-1]
    state += ");"

    for i in range(len(vals[0])):
        with_na = False
        vs = []
        for index in range(len(vals)):
            v = vals[index][i]
            vs.append(v)
            if order_dict[index] != 'gentrifying' and v == 0:
                with_na = True
                break
        if not with_na:
            c.execute(state, vs)
            conn.commit()
            print("inserted one record successfully")
        else:
            print("with na")

    conn.close()
        



def ml_train(db_path, res_col, related_cols, model):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(con = conn, sql="select * from Zillow_gentrification")
    y = df.pop(res_col)
    x = df[related_cols]
    print(y)
    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=17)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("\nAccuracy score : %f" %(accuracy_score(y_test, y_pred)))



def ml_classfier_compare(db_path, res_col, related_cols, model_list, names):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(con = conn, sql="select * from Zillow_gentrification")
    y = df.pop(res_col)
    x = df[related_cols]
    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=17)
    for i in range(len(names)):
        model_list[i].fit(X_train, y_train)
        y_pred = model_list[i].predict(X_test)
        print("Model " + names[i] + " Accuracy score : %f" %(accuracy_score(y_test, y_pred)))





if __name__ == '__main__':
    #query_zillow(zillow_db_path, gentrification_db_path)
    #update_zillow()
    #print(get_useful_zillow_record())
    #print(choose_zillow_metrics(0.05))
    #create_sql_table_for_useful('Zillow_gentrification', zillow_db_path)
    #data_prep_before_insert(baseline_cache_path)
    #insert_data_into_table(baseline_cache_path, zillow_db_path, 'Zillow_gentrification')
    cols_needed = list(choose_zillow_metrics().keys())
    #print(cols_needed)
    #ml_train(zillow_db_path, 'eligible_gentrification', ['MedianRentalPricePerSqft_Studio','PctOfListingsWithPriceReductionsSeasAdj_AllHomes'])
    names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Gaussian Process",
            "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
            "Naive Bayes", "QDA"]
    classifiers = [
        KNeighborsClassifier(3),
        SVC(kernel="linear", C=0.025),
        SVC(gamma=2, C=1),
        GaussianProcessClassifier(1.0 * RBF(1.0)),
        DecisionTreeClassifier(max_depth=5),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        MLPClassifier(alpha=1),
        AdaBoostClassifier(),
        GaussianNB(),
        QuadraticDiscriminantAnalysis()]
    ml_classfier_compare(zillow_db_path, 'gentrifying', cols_needed, classifiers, names)












    

    
    
