import numpy as np
import pandas as pd
import re

from pathlib import Path
from typing import Final

import sys
sys.path.append(Path(__file__).parent.parent.parent.resolve())



def load_data(data_path:str) -> pd.DataFrame:
    """
        The Data will be loaded from the excel File. 
    """
    try:
        df =  pd.read_excel(data_path)
        # get rid of empty spaces in headers // turn double __ to single _
        df.columns = [ re.sub(r'_+', '_', x)   for x in [re.sub(r'\s+', '_', x) for x in df.columns]]
        return df
    except:
        print('Data could not be loaded.')
        return None



def validate_data(df:pd.DataFrame) -> pd.DataFrame:
    """
        This function will check, if all values are in a certain range or fit specific values. 
        This insures, that models don't crash.

        The implementation is simple but time consuming  and will not be done in this project.
        This function could be used universally 
    """    
    return df



def missing_value_treatement(df: pd.DataFrame)->pd.DataFrame:

    # number_of_payment_faults is NA when there has been no faults, so 0 is the appropriate value
    df['number_of_payment_faults'].fillna(0, inplace=True)

    # policies without a comprehensive_product will be set to "KH" => this helps in the one-hot-encoding
    df['comprehensive_product_included'].fillna('KH', inplace=True)

    # policies without a risk_predictor_zip_code will be removed, since there is no way to predict this value
    df = df.loc[~df.risk_predictor_zip_code.isna()]

    # policy_start: in YEB only Change of Insurer is possible and also the most likely one (but not necessarily correct)
    df.loc[(df.policy_start.isna()) & (df.type_of_insurance != "Change of Insurer"), 'policy_start'] = "YOB"
    df = df.loc[~df.policy_start.isna() ] 
    
    return df


def create_new_columns(df: pd.DataFrame) -> pd.DataFrame:

    ## 2. Creating new columns
    df['SF_KH_num'] = df['bonus_malus_class_liability'].apply(lambda x : float(str(x).replace('SF', '').replace('1/2', '0.5').replace('M', '-1').replace('S', '-0.1')) )
    df['SF_VK_num'] = df['bonus_malus_class_comprehensive'].apply(lambda x : float(str(x).replace('SF', '').replace('1/2', '0.5').replace('M', '-1').replace('S', '-0.1')) )
    df['payment_fault'] = df['number_of_payment_faults'].apply(lambda x : 1 if x > 0 else 0)
    df['young_driver'] = df['age_insured_person'].apply(lambda x : 1 if int(x) <25 else 0)
    df['Friday_first'] = np.where((df['car_age_at_purchase'] == df['car_age_contract_start'] ) & (df['type_of_insurance']!='Change of Insurer' ) ,'Friday','OtherInsurer')
    df['deductible'] = (df['deductible_fully_comprehensive'].astype(str) + '/' + df['deductible_partially_comprehensive'].astype(str))


    return df


def load_and_transform(data_path:Path, ruleset_path:Path) -> pd.DataFrame:
    """ 
        Loading and preprocessing data for further modelling.
    """

    data = (
            load_data(data_path)
            .pipe(validate_data)
            .pipe(missing_value_treatement)
            .pipe(create_new_columns)
    )

    return data


