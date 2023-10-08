import pandas as pd

from pathlib import Path
from typing import Final

import sys
sys.path.append(Path(__file__).parent.parent.parent.resolve())

from src.pipelines.one_hot_encoding import one_hot_encoding



def load_data(data_path:str) -> pd.DataFrame:
    """
        The Data will be loaded from the excel File. 
    """
    try:
        df =  pd.read_excel(data_path)
        # get rid of empty spaces in headers
        df.columns = [x.replace(' ', '_') for x in df.columns]

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
    df['risk_predictor_zip_code'].dropna(inplace=True)

    # policy_start: in YEB only Change of Insurer is possible and also the most likely one (but not necessarily correct)
    df.loc[(df.policy_start.isna()) & (df.type_of_insurance != "Change of Insurer"), 'policy_start'] = "YOB"
    df.loc[(df.policy_start.isna()) & (df.type_of_insurance == "Change of Insurer"), 'policy_start'] = "YEB"
    
    return df


def create_new_columns(df: pd.DataFrame) -> pd.DataFrame:

    ## 2. Creating new columns
    df['sf_class_tpl_num'] = df['bonus_malus_class_liability'].apply(lambda x : float(str(x).replace('SF', '').replace('1/2', '0.5').replace('M', '95').replace('S', '96')) )
    df['sf_class_fc_num'] = df['bonus_malus_class_comprehensive'].apply(lambda x : float(str(x).replace('SF', '').replace('1/2', '0.5').replace('M', '95').replace('S', '96')) )
    df['number_of_installments'] = df['payment_interval'].apply(lambda x : 12 if x == 'Monthly' else 1)

    return df


def load_and_transform(data_path:Path, ruleset_path:Path) -> pd.DataFrame:
    """ 
        Loading and preprocessing data for further modelling.
    """

    data = (
            load_data(data_path)
            .pipe(validate_data)
            .pipe(missing_value_treatement)
            .pipe(one_hot_encoding, ruleset_path)
    )

    return data


