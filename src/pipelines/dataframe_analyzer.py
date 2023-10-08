import numpy as np
import pandas as pd


def get_values(df:pd.DataFrame, field:str, max_values:int =20, normalize: bool =True):
    """
    Displays the value_counts of a column in a DataFrame. 
    If there are to many different values in a column (this threshold can be set in max_values), only the number will be printed.
    To show the absolute Values, set normalize=False, else True

    """
    if df[field].value_counts().shape[0] < max_values:
        if normalize:
            display(pd.DataFrame(np.round(df[field].value_counts(normalize = True).reset_index(),2)))
        else:
            display(pd.DataFrame(df[field].value_counts().reset_index()))
    else:
        print(field, ': ', df[field].value_counts().shape[0], ' values' )
    print('\n')















