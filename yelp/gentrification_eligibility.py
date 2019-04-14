import pandas as pd
from variable_collections import gentrification_eligibility_path, gentrification_db_path, yelp_db_path,gentrification_csv_path,category_feature_with_eligibility, gentrification_csv_path_with_key, category_feature_with_eligibility

import sqlite3
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import statistics
import pandas as pd

from category_feature import ml_classfier_compare 
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

def check_gentrification_eligibility(zipcode, year):
    zipcode = int(zipcode)
    year = int(year)
    gentrification_eligibility_df = pd.read_csv(gentrification_eligibility_path)
    eligibility_num = gentrification_eligibility_df.loc[((gentrification_eligibility_df['year'] == year)
                                             &(gentrification_eligibility_df['RegionName_zip'] == zipcode))]
    try:
        #print(eligibility_num)

        res = eligibility_num.to_dict('list')['eligible_gentrification'][0]
        
        if res == 1:
            return 'Eligible'
        else:
            return 'Not Eligible'
    
    except:
        print('can not find this (zipcode, year) pair in dataset')
        return 'Not Eligible'



def count_zipcode_gentrfication_eligibity():
    conn = sqlite3.connect(gentrification_db_path)
    c = conn.cursor()
    c.execute('SELECT RegionName_zip FROM gentrification')
    rows = c.fetchall()
    uniq_rows = set(r[0] for r in rows)
    print(uniq_rows.__len__())
    conn.close()



def count_merge_zipcode_with_yelp():
    conn = sqlite3.connect(yelp_db_path)
    c = conn.cursor()
    c.execute("SELECT zipcode FROM Yelp_gentrification")
    rows = c.fetchall()
    uniq_rows = set(r[0] for r in rows)
    print(uniq_rows.__len__())
    conn.close()



def review_distribution():
    conn = sqlite3.connect(yelp_db_path)
    c = conn.cursor()
    c.execute("SELECT zipcode, rev_num FROM Yelp_gentrification")
    rows = c.fetchall()
    res = {}
    for row in rows:
        zipcode = row[0]
        rev_num = row[1]
        if zipcode not in res:
            res[zipcode] = []
        res[zipcode].append(rev_num)
    distri = []
    for _,v in res.items():
        distri.append(statistics.median(v))
    plt.hist(distri, range=[0,500])
    plt.xlabel("medium review number in neighborhood of different years")
    plt.ylabel("number of neighborhoods")
    plt.show()


def add_zipcode_year():
    gentri_df = pd.read_csv('../data/gentrification_csv_path_with_key.csv')
    years = []
    zipcodes = []
    for _, row in gentri_df.iterrows():
        key = row['key']
        year = key.split("_")[0]
        zipcode = key.split("_")[1]
        years.append(year)
        zipcodes.append(zipcode)
    gentri_df["year"] = years
    gentri_df["zipcode"] = zipcodes
    gentri_df.to_csv("../data/gentri_status.csv")
    print(set(years))


def prepare_category_csv_file():
    #add key col into cleaned gentrification table 
    gentrification_df = pd.read_csv(gentrification_csv_path)
    new_key = []
    for _, row in gentrification_df.iterrows():
        year = row['year']
        zipcode = str(row['zipcode'])
        while len(zipcode) < 5:
            zipcode = zipcode + '0'
        key = str(year) + "_" + zipcode
        new_key.append(key)
    gentrification_df['key'] = new_key
    gentrification_df.to_csv(gentrification_csv_path_with_key)
    #merge gentrificarion csv table with category table
    gentri_df = pd.read_csv(gentrification_csv_path_with_key)
    category_df = pd.read_csv(category_feature_with_eligibility)
    merged_pd = pd.merge(gentri_df, category_df, on="key")
    merged_pd.to_csv("./data/category_with_new_def.csv")

def merge_avg_nlp_with_gentr():
    gentri_df = pd.read_csv(gentrification_csv_path_with_key)
    avg_df = pd.read_csv('../avg_nlp.csv')
    merged_pd = pd.merge(gentri_df, avg_df, on="key")
    merged_pd.to_csv("./data/avg_df_gentri.csv")

def run_classifer():
    merged_pd = pd.read_csv("./data/category_with_new_def.csv")
    res_cols = ['gentrifying_pct_chg_income_homeval_educ','gentrifying_pct_chg_income_homeval','gentrifying_pct_chg_homeval']
    all_cols = list(merged_pd)
    feature_cols = [c for c in all_cols if c not in res_cols and c not in ['key'] and 'Unnamed' not in c]
    print(feature_cols)

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
    for res_c in res_cols:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Result for " + res_c)
        print("--------------------------------------")
        ml_classfier_compare('./data/category_with_new_def.csv', res_c, feature_cols, classifiers, names)


def run_classifer_avg_nlp():
    merged_pd = pd.read_csv("./data/avg_df_gentri.csv")
    res_cols = ['gentrifying_pct_chg_income_homeval_educ','gentrifying_pct_chg_income_homeval','gentrifying_pct_chg_homeval']
    all_cols = list(merged_pd)
    feature_cols = [c for c in all_cols if c not in res_cols and c not in ['key'] and 'Unnamed' not in c]


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
    for res_c in res_cols:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("Result for " + res_c)
        print("--------------------------------------")
        ml_classfier_compare('./data/avg_df_gentri.csv', res_c, feature_cols, classifiers, names)



def run_classifer_unbalanced():
    merged_pd = pd.read_csv("./data/category_with_new_def.csv")
    res_cols = ['gentrifying_pct_chg_income_homeval_educ','gentrifying_pct_chg_income_homeval','gentrifying_pct_chg_homeval']
    all_cols = list(merged_pd)
    feature_cols = [c for c in all_cols if c not in res_cols and c not in ['key'] and 'Unnamed' not in c]

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

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Result for gentrifying_pct_chg_income_homeval_educ")
    print("--------------------------------------")
    n = round(709 * 0.14)
    sample_yes = merged_pd.ix[merged_pd.gentrifying_pct_chg_income_homeval_educ == 1].sample(n=n, replace=False, random_state=0)
    sample_no = merged_pd.ix[merged_pd.gentrifying_pct_chg_income_homeval_educ == 0].sample(n=n, replace=False, random_state=0)
    df_1 = pd.concat([sample_yes, sample_no])
    df_1.to_csv("./data/category_with_new_def_unbalanced_1.csv")
    ml_classfier_compare('./data/category_with_new_def_unbalanced_1.csv', 'gentrifying_pct_chg_income_homeval_educ', feature_cols, classifiers, names)

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Result for gentrifying_pct_chg_income_homeval")
    print("--------------------------------------")
    n = round(709 * 0.25)
    sample_yes = merged_pd.ix[merged_pd.gentrifying_pct_chg_income_homeval == 1].sample(n=n, replace=False, random_state=0)
    sample_no = merged_pd.ix[merged_pd.gentrifying_pct_chg_income_homeval == 0].sample(n=n, replace=False, random_state=0)
    df_2 = pd.concat([sample_yes, sample_no])
    df_2.to_csv("./data/category_with_new_def_unbalanced_2.csv")
    ml_classfier_compare('./data/category_with_new_def_unbalanced_2.csv', 'gentrifying_pct_chg_income_homeval', feature_cols, classifiers, names)


def run_classifer_unbalanced_avg_nlp():
    merged_pd = pd.read_csv("./data/avg_df_gentri.csv")
    res_cols = ['gentrifying_pct_chg_income_homeval_educ','gentrifying_pct_chg_income_homeval','gentrifying_pct_chg_homeval']
    all_cols = list(merged_pd)
    feature_cols = [c for c in all_cols if c not in res_cols and c not in ['key'] and 'Unnamed' not in c]

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

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Result for gentrifying_pct_chg_income_homeval_educ")
    print("--------------------------------------")
    n = round(709 * 0.14)
    sample_yes = merged_pd.ix[merged_pd.gentrifying_pct_chg_income_homeval_educ == 1].sample(n=n, replace=False, random_state=0)
    sample_no = merged_pd.ix[merged_pd.gentrifying_pct_chg_income_homeval_educ == 0].sample(n=n, replace=False, random_state=0)
    df_1 = pd.concat([sample_yes, sample_no])
    df_1.to_csv("./data/avg_nlp_unbalanced_1.csv")
    ml_classfier_compare('./data/avg_nlp_unbalanced_1.csv', 'gentrifying_pct_chg_income_homeval_educ', feature_cols, classifiers, names)

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Result for gentrifying_pct_chg_income_homeval")
    print("--------------------------------------")
    n = round(709 * 0.25)
    sample_yes = merged_pd.ix[merged_pd.gentrifying_pct_chg_income_homeval == 1].sample(n=n, replace=False, random_state=0)
    sample_no = merged_pd.ix[merged_pd.gentrifying_pct_chg_income_homeval == 0].sample(n=n, replace=False, random_state=0)
    df_2 = pd.concat([sample_yes, sample_no])
    df_2.to_csv("./data/avg_nlp_unbalanced_2.csv")
    ml_classfier_compare('./data/avg_nlp_unbalanced_2.csv', 'gentrifying_pct_chg_income_homeval', feature_cols, classifiers, names)



if __name__ == "__main__":
    # print(check_gentrification_eligibility('44112', '2017'))
    # prepare_category_csv_file()
    # run_classifer_unbalanced()
    # merge_avg_nlp_with_gentr()
    # run_classifer()
    # run_classifer_avg_nlp()
    # run_classifer_unbalanced_avg_nlp()
    add_zipcode_year()