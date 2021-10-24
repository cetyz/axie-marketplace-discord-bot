# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 02:37:49 2021

@author: Charles
"""

import time
import numpy as np
import pandas as pd
import itertools

from wrapper import get_axie, get_axie_market_list
from gene_functions import decode_genes

# inheritance probabilities for DOMINANT genes
# dominant 37.5%
# r1 9.375%
# r2 3.125%

# no idea how inheritance works for recessive genes



axie1_id = 7793905
axie2_id = 7923772

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
                



# print(traits_dict)

df = pd.DataFrame()

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
    # print(part_values)
    
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
    
# going to drop ears and eyes for now. too many combinations

# combi_df = combi_df.loc[~combi_df['part_type'].isin(['Ears', 'Eyes'])]    
    
parts_list = []
probs_list = []

for i in possibility_dict.keys():
    for part in possibility_dict[i].keys():
        parts_list.append(part)
        probs_list.append(possibility_dict[i][part])
        
probs_df = pd.DataFrame(np.transpose([parts_list, probs_list]), columns=['part', 'probs'])

combi_df = combi_df.merge(probs_df, how='left', on='part')
combi_df['probs'] = combi_df['probs'].astype('float')

# print(combi_df['probs'].astype('float').unique())

probs_df_2 = combi_df[['combi_index', 'probs']].groupby('combi_index').prod().reset_index()

combi_df = combi_df.merge(probs_df_2, how='left', on='combi_index').sort_values(['probs_y', 'combi_index'], ascending=[False, True])

combi_df['req_name'] = combi_df['part_type'].str.lower() + '-' + combi_df['part'].str.replace(' ', '-').str.lower()

# print(combi_df[['combi_index', 'probs_y']].groupby(['combi_index', 'probs_y']).sum().reset_index().sum())

temp_counter = 0
for i in combi_df['combi_index'].unique().tolist():
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

    # print(int(results[0]['auction']['currentPrice'])/10e18)
    try:
        print(float(results[0]['auction']['currentPriceUSD']))
    except:
        pass
    
    temp_counter += 1
    
    if temp_counter > 10:
        break
    
    time.sleep(0.01)























