import pandas as pd
from variable_collections import gentrification_eligibility_path




def check_gentrification_eligibility(zipcode, year):
    zipcode = int(zipcode)
    year = str(year)
    gentrification_eligibility_df = pd.read_csv(gentrification_eligibility_path)

    eligibility_num = gentrification_eligibility_df.loc[((gentrification_eligibility_df['year'] == year)
                                             &(gentrification_eligibility_df['RegionName_zip'] == zipcode)), 'eligible_gentrification']
    if int(eligibility_num) == 1:
        result = 'Eligible'
    else:
        result = 'Not Eligible'
    return result


if __name__ == "__main__":
    print(check_gentrification_eligibility(49445, 2017))