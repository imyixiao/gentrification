import pandas as pd
from variable_collections import gentrification_eligibility_path


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
        



if __name__ == "__main__":
    print(check_gentrification_eligibility('44112', '2017'))