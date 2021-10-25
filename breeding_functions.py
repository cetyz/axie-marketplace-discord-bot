# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 02:37:49 2021

@author: Charles
"""

import time
import numpy as np
import pandas as pd
import itertools

from wrapper import get_axie, get_axie_market_list, get_breed_count
from gene_functions import decode_genes
from generic_functions import fetch_axs_price, fetch_slp_price



def get_breeding_cost(axie1_breed_count, axie2_breed_count):
    
    axs_cost_usd, axs_cost_eth = fetch_axs_price()
    slp_cost_usd, slp_cost_eth = fetch_slp_price()
    
    slp_req_dict = {
        0: 300,
        1: 450,
        2: 750,
        3: 1200,
        4: 1950,
        5: 3150,
        6: 5100
    }
    
    axie1_slp_req = slp_req_dict[axie1_breed_count]
    axie2_slp_req = slp_req_dict[axie2_breed_count]
    
    axie1_slp_cost_usd = axie1_slp_req * slp_cost_usd
    axie1_slp_cost_eth = axie1_slp_req * slp_cost_eth
    axie2_slp_cost_usd = axie2_slp_req * slp_cost_usd
    axie2_slp_cost_eth = axie2_slp_req * slp_cost_eth
    
    total_cost_usd = axs_cost_usd + axie1_slp_cost_usd + axie2_slp_cost_usd
    total_cost_eth = axs_cost_eth + axie1_slp_cost_eth + axie2_slp_cost_eth
    
    return total_cost_usd, total_cost_eth
    

def get_axie_price(axie_id):
    
    
    # if axie is on sale, get current price in eth and usd
    # if axie is not on sale, return nan
    
    results = get_axie(axie_id=axie_id)
    if not results:
        raise ValueError('Axie not found')
    elif not results['auction']:
        eth_price, usd_price = np.nan, np.nan
    else:
        eth_price = np.round(int(results['auction']['currentPrice'])/10e18, 4)
        usd_price = np.round(float(results['auction']['currentPriceUSD']), 2)

    return eth_price, usd_price
    

def get_expected_revenue(axie1_id, axie2_id, verbose=False, csv_out=False):

# inheritance probabilities for DOMINANT genes
# dominant 37.5%
# r1 9.375%
# r2 3.125%

# no idea how inheritance works for recessive genes



# axie1_id = 7793905
# axie2_id = 7923772

    axie1_gene_str = get_axie(axie_id=axie1_id)['genes']
    axie2_gene_str = get_axie(axie_id=axie2_id)['genes']


    axie1_genes = decode_genes(axie1_gene_str)
    axie2_genes = decode_genes(axie2_gene_str)

    traits_dict = {
        # in the order of d, r1, r2
        'Eyes': [],
        'Eyes_dom': [],
        'Mouth': [],
        'Mouth_dom': [],
        'Ears': [],
        'Ears_dom': [],
        'Horn': [],
        'Horn_dom': [],
        'Back': [],
        'Back_dom': [],
        'Tail': [],
        'Tail_dom': []
        }

    dom_dict = {
        'd': 0.375,
        'r1': 0.09375,
        'r2': 0.03125
        }

    parts_list = ['Eyes', 'Mouth', 'Ears', 'Horn', 'Back', 'Tail']

    for genes in ['axie1_genes', 'axie2_genes']:
        for attr in dir(eval(genes)):
            
            # handle Eyes, then Mouth, then Ears, then Horn, then Back, then Tail
        
            for part in parts_list:
                if part in attr:
                    dominance =  attr.replace(part, '')
                    traits_dict[part].append(eval(genes+'.'+attr))
                    traits_dict[part+'_dom'].append(dom_dict[dominance])
                
    
    # df = pd.DataFrame()
    
    axie_df = pd.DataFrame(traits_dict)
    # print(axie_df)
    
    possibility_dict = {
        'Eyes': {},
        'Mouth': {},
        'Ears': {},
        'Horn': {},
        'Back': {},
        'Tail': {}    
        }
    
    for part in parts_list:
        
        temp_df = axie_df[[col for col in axie_df.columns if part in col]]
        
        temp_df = temp_df.groupby(part).sum().reset_index()
        
        part_values = temp_df[part].values

        
        for i in part_values:
            possibility_dict[part][i] = temp_df.loc[temp_df[part]==i][part+'_dom'].values[0]
        
        
    combi_list = []   
        
    for i in possibility_dict.keys():
        
        combi_list.append(list(possibility_dict[i].keys()))
        
        
    combinations = list(itertools.product(*combi_list))
    
    combi_df = pd.DataFrame()
    
    for i, combi in enumerate(combinations):
        
        temp_df = pd.DataFrame()
        temp_df['part'] = combi
        temp_df['part_type'] = ['Eyes', 'Mouth', 'Ears', 'Horn', 'Back', 'Tail']
        temp_df['combi_index'] = i
        
        
        combi_df = pd.concat([combi_df, temp_df])
        
    parts_list = []
    probs_list = []
    
    for i in possibility_dict.keys():
        for part in possibility_dict[i].keys():
            parts_list.append(part)
            probs_list.append(possibility_dict[i][part])
            
    probs_df = pd.DataFrame(np.transpose([parts_list, probs_list]), columns=['part', 'probs'])
    
    combi_df = combi_df.merge(probs_df, how='left', on='part')
    combi_df['probs'] = combi_df['probs'].astype('float')
    
    probs_df_2 = combi_df[['combi_index', 'probs']].groupby('combi_index').prod().reset_index()
    
    combi_df = combi_df.merge(probs_df_2, how='left', on='combi_index').sort_values(['probs_y', 'combi_index'], ascending=[False, True])
    
    combi_df['req_name'] = combi_df['part_type'].str.lower() + '-' + combi_df['part'].str.replace(' ', '-').str.lower()
    
    price_data = []
    
    combis = len(combi_df['combi_index'].unique().tolist())
    
    checkpoints = np.round(np.linspace(0, 800, num=20), 0)
    
    print('Scanning the market for', combis, 'combinations')
    
    for h, i in enumerate(combi_df['combi_index'].unique().tolist()):
        
        if verbose:
            if h in checkpoints:
                print(h+1, '/', combis)
        
        combi_data = [i]
        
        parts = list(combi_df[combi_df['combi_index']==i]['req_name'].values)
        
        results = get_axie_market_list(
            size = 1,
            sort = 'PriceAsc',
            auction_type = 'Sale',
            owner = None,
            parts = parts,
            classes = 'Plant',
            stages = 4,
            pureness = None,
            breed_count = 0,
            hp = [],
            skill = [],
            speed = [],
            morale = [],
        )
    
        if not len(results):
            combi_data.append(np.nan)
            combi_data.append(np.nan)
        
        else:
            combi_data.append(int(results[0]['auction']['currentPrice'])/10e18)
            combi_data.append(np.round(float(results[0]['auction']['currentPriceUSD']), 2))
        
        price_data.append(combi_data)
        
        time.sleep(0.01)
        
    price_df = pd.DataFrame(data=price_data, columns=['combi_index', 'eth_price', 'usd_price'])
    
    combi_df = combi_df.merge(price_df, how='left', on='combi_index')
    combi_df['expected_eth'] = combi_df['probs_y'] * combi_df['eth_price'].fillna(combi_df['eth_price'].min())
    combi_df['expected_usd'] = combi_df['probs_y'] * combi_df['usd_price'].fillna(combi_df['usd_price'].min())
    
    if csv_out:
        combi_df.to_csv('out.csv', index=False)
    
    revenue_df = combi_df[['combi_index', 'expected_eth', 'expected_usd']].groupby(['combi_index', 'expected_eth', 'expected_usd']).sum().reset_index()
    
    expected_eth, expected_usd = revenue_df['expected_eth'].sum(), revenue_df['expected_usd'].sum()
    
    return(expected_eth, expected_usd)




if __name__ == '__main__':
    
    # print(get_expected_revenue(7793905, 7930458, True, False))
    
    print(get_breed_count(7793905))























