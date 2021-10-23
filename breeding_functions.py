# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 02:37:49 2021

@author: Charles
"""

from wrapper import get_axie
from gene_functions import decode_genes

# inheritance probabilities for DOMINANT genes
# dominant 37.5%
# r1 9.375%
# r2 3.125%

# no idea how inheritance works for recessive genes



axie1_id = 7829650
axie2_id = 7891371

axie1_gene_str = get_axie(axie_id=axie1_id)['genes']
axie2_gene_str = get_axie(axie_id=axie2_id)['genes']


axie1_genes = decode_genes(axie1_gene_str)
axie2_genes = decode_genes(axie2_gene_str)

print(axie1_genes.dHorn)

