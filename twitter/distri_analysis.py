import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

gentri_table = "../data/gentri_status.csv"
twitter = "../data/twitter.csv"


def distri_year():
    gentri_df = pd.read_csv(gentri_table)
    twitter_df = pd.read_csv(twitter)
    gentri_distri = {}
    twitter_distri = {}

    for _, row in gentri_df.iterrows():
        year = row['year']
        zipcode = row['zipcode']
        if year not in gentri_distri:
            gentri_distri[year] = set()
        gentri_distri[year].add(zipcode)

    for _, row in twitter_df.iterrows():
        year = row['year']
        zipcode = row['zipcode']
        if year not in twitter_distri:
            twitter_distri[year] = set()
        twitter_distri[year].add(zipcode)
    
    gentri_count = {}
    for k,v in gentri_distri.items():
        gentri_count[k] = len(v)
    
    twitter_count = {}
    for k,v in twitter_distri.items():
        twitter_count[k] = len(v)
    
    print(gentri_count)
    print(twitter_count)


def distri_zipcode_by_year(the_year = 2013):
    twitter_df = pd.read_csv(twitter)
    data = []
    for the_year in range(2013, 2018):
        res = []
        twitter_distri = {}
        for _, row in twitter_df.iterrows():
            year = row['year']
            zipcode = row['zipcode']
            if int(year) != the_year:
                continue
            if zipcode not in twitter_distri:
                twitter_distri[zipcode] = 0
            twitter_distri[zipcode] += 1
        for _,v in twitter_distri.items():
            res.append(v)
        data.append(res)
    plt.boxplot(data)
    plt.xticks([1, 2, 3, 4, 5], ['2013','2014','2015','2016','2017'])
    plt.show()

if __name__ == "__main__":
    distri_zipcode_by_year()