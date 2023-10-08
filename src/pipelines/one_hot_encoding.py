import json
import pandas as pd



def load_one_hot_encoder_ruleset(name:str) -> pd.DataFrame:
    try:
        with open(name) as json_file:
            ruleset = json.load(json_file)
            #print('ruleset loaded')
    except:
        print('ruleset could not be loaded.', name)
        return -1
    
    return ruleset



def check_schema(df: pd.DataFrame, col:str, schema:list):
    """
        Checks if the schema is respected and no new values exists
    """

    if set(df[col].unique()).issubset(schema):
        return True
    else:
        return False

def check_loose_exists(df, col, loose):
    """
        Checks if the column that is designated to be lost actually exists
    """
    if loose in list(df[col].unique()):
        #print('loose exists')
        return True
    else:
        return False


def get_dummies(df: pd.DataFrame, col:str, loose:str) -> pd.DataFrame:
    """
        Creates the dummies while keeping the original columns. these can be eliminated later by dropping one_hot_encode_rules.keys() from the columns.
        Labeling: 
            for plotting the data well, the OHE Columns will have the original name and the value spaced by a "@" character.
    """
    df[col + '_'] = df[col] 
    df = pd.get_dummies(df, columns = [col + '_'],  dtype=int)
    
    # loose the one designated  
    df.drop( col+'__'+loose, axis=1, inplace=True)

    df.columns = [x.replace('__','@') for x in df.columns]
    #print('dummies finished')
    return df


def one_hot_encoding(df:pd.DataFrame, ruleset_name:str):
    """
        combines all the functions into one.
    """
    ruleset=load_one_hot_encoder_ruleset(ruleset_name)

    for key, val in ruleset.items():

        schema = val['schema']
        loose = val['loose']

        if check_schema(df, key, schema):
            if check_loose_exists(df, key, loose):
                df = get_dummies(df, key, loose)
            else:
                print('loose column does not exist in data', key, loose, list(df[key].unique()))
                continue
        else: 
            print('Schema broken', key, schema, list(df[key].unique()))
            continue
        
        #print('done with', key)
    return df


