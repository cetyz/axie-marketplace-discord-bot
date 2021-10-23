# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 17:47:37 2021

@author: Charles
"""

from wrapper import get_axie
import gene_functions

genes = get_axie(axie_id=7793905)['genes']

axie_genes = gene_functions.decode_genes(genes)

print(axie_genes.r2Horn)