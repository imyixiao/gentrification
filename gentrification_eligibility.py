import pandas as pd

gentrification_eligibility_df = pd.read_csv('/Users/hanley/Desktop/SI_699/Predicting_Gentrification/gentrification_eligibility.csv')

def check_gentrification_eligibility(zipcode, year):
    zipcode = int(zipcode)
    year = str(year)
    eligibility_num = gentrification_eligibility_df.loc[((gentrification_eligibility_df['year'] == 2017)
                                             &(gentrification_eligibility_df['RegionName_zip']==49445)), 'eligible_gentrification']
    if int(eligibility_num) == 1:
        result = 'Eligible'
    else:
        result = 'Not Eligible'
    return result

print(check_gentrification_eligibility(49445, 2017))