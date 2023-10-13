import math 
import numpy as np
import pandas as pd
import statsmodels.api as sm

def sigmoid(x):
  """
    Recalculates the model Factors
  """
  return 1 / (1 + math.exp(-x))


def grouper(x, bins, labels):
    
    if len(bins) != len(labels):
        return 'Bad Labels'
    
    for i in np.arange(len(bins)):
        if x < bins[i]:
            return labels[i]
        
    return 'NO_GROUP'


def set_manual(x, groups, labels):
    for g in groups:
        if x in g:
            return (labels[groups.index(g)]) 

    return 'ELEMENT NOT FOUND!: ' + str(x)


def get_model_data_set(df_ohc:pd.DataFrame, ohc_drops, tts_list) -> list:
    
    X_train = tts_list[0]
    X_test = tts_list[1]
    y_train = tts_list[2]
    y_test = tts_list[3]

    df = pd.concat([X_train, X_test])

    liste = [ pd.merge(left=df, right=df_ohc, on='contract_nr', how='left')
             ,pd.merge(left=X_train, right=df_ohc, on='contract_nr', how='left')
             ,pd.merge(left=X_test, right=df_ohc, on='contract_nr', how='left')
             ,pd.DataFrame(y_train)
             ,pd.DataFrame(y_test)]
            

    for ds in liste[:-2]:
        ds.set_index('contract_nr', inplace=True)
        ds.drop(ohc_drops, axis=1, inplace=True)
        
    return liste





def build_model(df:pd.DataFrame, column_manager:dict, group_file:dict,tts_list:list ) -> dict:
    """
        Builds the model and generates the output for plotting and model scoring.
    """
    model_dict = {}
    field_to_group_map = {}
    # create the columns_manager
    col_mapping = {}
    cols_to_OHE = []
    ###############################
    # Grouping
    for k, v in group_file['ranges'].items():
        current_name = v['name']
        number_bins = len(v['bins'])    
        
        # create Groupnames
        groupnames = [current_name + '_' + str(i+1) for i in range(number_bins)]
        
        # Group Data
        df[current_name] = df[k].apply(grouper, bins=v['bins'], labels=groupnames)

        # add to mapping dict
        col_mapping[k] = groupnames 
        field_to_group_map[k] = current_name
        cols_to_OHE = cols_to_OHE + [current_name]
        

    ###############################
    # Manual setting
    for k, v in group_file['manual_set'].items():
        current_name = v['name']
        number_bins = len(v['groups'])
        
        # create Groupnames
        groupnames = [current_name + '_' + str(i+1) for i in range(number_bins)]
            
        # Group Data
        df[current_name] = df[k].apply(set_manual, groups=v['groups'], labels=groupnames)

        # add to mapping dict
        col_mapping[k] = groupnames
        field_to_group_map[k] = current_name
        cols_to_OHE = cols_to_OHE + [current_name]


    ###############################
    # One Hot Encoding

    # column mapping
    for col in  group_file['dummies']:
        col_mapping[col] = list(df[col].unique())

    # liste aufbauen (OHC + die oben)
    cols_to_OHE = cols_to_OHE + group_file['dummies']


    # für jede Spalte den encoder anwenden. 
    ohc_drops = []
    ohc_keeps = []

    df_ohc = df[['contract_nr'] + cols_to_OHE]

    for col in cols_to_OHE:
        ohc_drops.append(df[col].value_counts().reset_index().iloc[0][col] )
        ohc_keeps = ohc_keeps + list(df[col].value_counts().reset_index().iloc[1:][col])

        df_ohc = pd.get_dummies(df_ohc, columns = [col], drop_first=False,  dtype=int, prefix='', prefix_sep='')
    

    ###############################
    # Join to the original data
    model_data = get_model_data_set(df_ohc, ohc_drops, tts_list)

    # wegschreiben
    column_manager['complete_mapping']=col_mapping   
    column_manager['ohc_keeps'] = ohc_keeps
    column_manager['ohc_drops'] = ohc_drops
    column_manager['field_to_group_map'] = field_to_group_map
    column_manager['plots'] = list(group_file['ranges'].keys()) + list(group_file['manual_set'].keys()) + group_file['dummies']
    ##############################################################
    ### Create the GLM and modelling                           ###
    ##############################################################

    # fit only on Train_set
    model = sm.GLM(  endog=model_data[3]
                    ,exog =model_data[1]
                    ,family=sm.families.Binomial() #Fill this
                   ).fit(maxiter=50)


    pred_test_df = pd.DataFrame(model.predict(model_data[2])).reset_index()
    pred_test_df.columns = ['contract_nr', 'predicted']
    test_df = pd.merge(left=df, right=pred_test_df, on='contract_nr', how='inner')

    pred_train = pd.DataFrame(model.predict(model_data[1])).reset_index()
    pred_train.columns = ['contract_nr', 'predicted']
    train_df = pd.merge(left=df, right=pred_train, on='contract_nr', how='inner')


    pred_full = pd.DataFrame(model.predict(model_data[0])).reset_index()
    pred_full.columns = ['contract_nr', 'predicted']
    full = pd.merge(left=df, right=pred_full, on='contract_nr', how='left')

    




    #################################################
    # Faktoren berechnen
    coefs = pd.DataFrame(model.params).reset_index()
    coefs.columns = ['groups', 'coef_raw']
    coefs['coef'] = coefs.coef_raw.apply(sigmoid)

    list_for_pd = []

    for k, v in column_manager['complete_mapping'].items():
        for val in v:
            list_for_pd.append({'field':k, 'groups':val})

    factors = pd.merge(left=pd.DataFrame(list_for_pd), right=coefs[['groups', 'coef']], on='groups', how='left').fillna(0.5)

    # P-Values
    P_vals = pd.DataFrame(model.summary().tables[1])
    P_vals.columns = ['group', 'coef', 'std_err', 'z', 'P', '[0.025', '0.975]'] 
    P_vals = P_vals[1:][['group','coef', 'P']]
    




    ###############################
    # create return value: model dict 
    model_dict['column_manager'] = column_manager
    model_dict['full_dataset'] = df
    model_dict['model'] = model
    model_dict['prediction_trainset'] = train_df
    model_dict['prediction_testset'] = test_df
    model_dict['prediction_full'] = full
    model_dict['factors'] = factors
    model_dict['P_vals'] = P_vals
    model_dict['md'] = model_data

    #return model_data
    return model_dict





def get_plot_data(erg:dict, field_name:str, on_test_data:bool)-> pd.DataFrame:
    """
        Connects the original Data with the predictions and adds the coefficients to the output.
    """
    try:
        group_name = erg['column_manager']['field_to_group_map'][field_name] 
        # load Data for plotting
        
        if on_test_data:
            plot_df = erg['prediction_testset'][['contract_nr', field_name, group_name,'payment_fault', 'predicted']].copy()
        else:
            plot_df = erg['prediction_trainset'][['contract_nr', field_name, group_name,'payment_fault', 'predicted']].copy()
        
        # load factors (sigmiod)
        coefs = erg['factors'].loc[erg['factors']['field'] == field_name]
        # merge
        plot_df = pd.merge(left=plot_df, right=coefs, left_on=group_name, right_on='groups', how='left')
    except:
        # load Data for plotting
        if on_test_data:
            plot_df = erg['prediction_testset'][['contract_nr', field_name, 'payment_fault', 'predicted']].copy()
        else:
            plot_df = erg['prediction_trainset'][['contract_nr', field_name, 'payment_fault', 'predicted']].copy()
        
        
        # load factors (sigmiod)
        coefs = erg['factors'].loc[erg['factors']['field'] == field_name]
        # merge
        if coefs.shape[0] == 0:
            plot_df['coef'] = 0.5
        else:
            plot_df = pd.merge(left=plot_df, right=coefs, left_on=field_name, right_on='groups', how='left')
    
    # group by original values
    plot_df_grp = plot_df.groupby(field_name).agg({'contract_nr':'count','payment_fault':'mean', 'predicted':'mean', 'coef':'min' }).reset_index()
    
    # Umbenennen
    plot_df_grp.columns = [x if x != 'contract_nr' else 'Exposure' for x in [field_name, 'contract_nr', 'payment_fault', 'predicted', 'coef'] ]
    return plot_df_grp

