import pandas as pd 
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
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import numpy as np

nlp_feature_path = '../../avg_nlp_monday.csv'


def prepare_df_unbalanced(gentried_num, res_col):
    whole_df = pd.read_csv(nlp_feature_path)
    n = round(gentried_num * 0.8)
    sample_yes = whole_df.ix[whole_df[res_col] == 1].sample(n=n, replace=False, random_state=0)
    sample_no = whole_df.ix[whole_df[res_col] == 0].sample(n=n, replace=False, random_state=0)
    train_df = pd.concat([sample_yes, sample_no]).dropna()
    test_df = whole_df[~whole_df.isin(train_df)].dropna()
    return train_df,test_df



def ml_classfier_compare(train_df, test_df, res_col, feature_cols):
    X_train = train_df[feature_cols].values
    y_train = train_df.pop(res_col).values
    X_test = test_df[feature_cols].values
    y_test = test_df.pop(res_col).values

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

    names = ['knn','svc-linear','svc','gaussian','decision tree','random forest','mlp','adaboost','gnb']

    for i in range(len(names)):
        classifiers[i].fit(X_train, y_train)
        y_pred = classifiers[i].predict(X_test)
        print("Model " + names[i] + " Accuracy score : %f" %(accuracy_score(y_test.round(), y_pred.round())))
        print("Model " + names[i] + " Recall score : %f" %(recall_score(y_test.round(), y_pred.round()))) 
        print("Model " + names[i] + " F1 : %f" %(f1_score(y_test.round(), y_pred.round(),average='weighted'))) 

    
def run_classifer(gentried_num_list, res_col_list, feature_col_list):
    for i in range(len(res_col_list)):
        print("--------------------------------------")
        print("Predict Result for" + res_col_list[i])
        train_df, test_df = prepare_df_unbalanced(gentried_num_list[i],res_col_list[i])
        ml_classfier_compare(train_df, test_df, res_col_list[i], feature_col_list)


if __name__ == "__main__":
    gentried_num_list = [665,1211,2000]
    res_col_list = ['gentrifying_pct_chg_income_homeval_educ','gentrifying_pct_chg_income_homeval','gentrifying_pct_chg_homeval']
    feature_col_list = ['avg(sentiment_binary)','avg(num_longer_five)','avg(avg_syllables_per_word)','avg(readability)','avg(avg_wordlen)','avg(proportion_words_longer_five)']
    run_classifer(gentried_num_list, res_col_list, feature_col_list)