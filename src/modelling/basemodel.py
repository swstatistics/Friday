base_model = {
     'ranges':{
            'age_insured_person': 
                {'name':'age_group'
                ,'bins': [25, 31, 41, 54, 999]
                }
            ,'SF_KH_num': 
                { 'name': 'sf_tpl_group'
                ,'bins' : [0, 1, 4, 7, 11, 999]
                }
            ,'SF_VK_num' :
                {'name': 'sf_fc_group'
                ,'bins' :[0, 1, 4, 11, 20, 999]        
                }
            ,'car_age_at_purchase':
                {'name': 'car_age_pur_group'
                ,'bins' :[5, 11, 999]        
                }
            ,'car_age_contract_start':
                {'name': 'car_age_cont_group'
                ,'bins' :[3,7, 11,12,13,14,15,16,17,18, 999]        
                }
    }
    ,'manual_set':{
            'risk_predictor_zip_code':{'groups':[[1,4], [5,6,7],[2,3,8],[9]]
                                       ,'name':'region_group'}
            ,'deductible':{'groups':[[ '0/500','1000/500', '300/300','500/300','1000/300','300/150'], ['0/0'], ['0/150','0/300'],['1000/150','500/150']]
                                       ,'name':'deductable_group'}
    }
    ,'dummies': 
            [
                'profession_group'
                ,'payment_interval'
                ,'tariff_type'
                ,'policy_start'
                #,'comprehensive_product_included'
                ,'type_of_insurance'
                ,'insured_parties'
                ,'Friday_first'
            ]
}