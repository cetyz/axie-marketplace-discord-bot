# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 17:27:56 2021

@author: Charles
"""

import json

class AxieGenes():
    def __init__(self):
        # ignoring stuff like region, tag, etc.
        # d, r1, r2
        
        # lowercase for binary str
        self.class_ = None
        self.eyes = None
        self.mouth = None
        self.ears = None
        self.horn = None
        self.back = None
        self.tail = None
        
        # self.r1_class_ = None
        # self.r1_eyes = None
        # self.r1_mouth = None
        # self.r1_ears = None
        # self.r1_horn = None
        # self.r1_back = None
        # self.r1_tail = None
        
        # self.r2_class_ = None
        # self.r2_eyes = None
        # self.r2_mouth = None
        # self.r2_ears = None
        # self.r2_horn = None
        # self.r2_back = None
        # self.r2_tail = None
        
        # uppercase for decoded str
        self.dClass = None
        self.dEyes = None
        self.dMouth = None
        self.dEars = None
        self.dHorn = None
        self.dBack = None
        self.dTail = None
        
        self.r1Class = None
        self.r1Eyes = None
        self.r1Mouth = None
        self.r1Ears = None
        self.r1Horn = None
        self.r1Back = None
        self.r1Tail = None    
        
        self.r2Class = None
        self.r2Eyes = None
        self.r2Mouth = None
        self.r2Ears = None
        self.r2Horn = None
        self.r2Back = None
        self.r2Tail = None            
        
        
classes_dict = {
	"0000": 'Beast', "0001": 'Bug', "0010": 'Bird', "0011": 'Plant',
    "0100": 'Aquatic', "0101": 'Reptile', "1000": 'Mech', "1010": 'Dusk', 
    "1001": 'Dawn', 
    "00000": 'Beast', "00001": 'Bug', "00010": 'Bird', "00011": 'Plant',
	"00100": 'Aquatic', "00101": 'Reptile', "10000": 'Mech', "10001": 'Dawn', 
    "10010": 'Dusk',
}

def get_traits_json():
    with open('traits.json') as f:
        return(json.load(f))
    
def decode_genes(genes_hex_string):
    
    b_str = bin(int(genes_hex_string, 16))
    length = len(b_str)
    
    genes = AxieGenes()
    
    if length == 256:
        b_str = b_str.replace('0b', '00', 1)
        
        genes.class_ = b_str[0:4]
        genes.eyes = b_str[64:96]
        genes.mouth = b_str[96:128]
        genes.ears = b_str[128:160]
        genes.horn = b_str[160:192]
        genes.back = b_str[192:224]
        genes.tail = b_str[224:256]
    
        genes.Class = classes_dict[genes.class_]
        genes.dEyes, genes.r1Eyes, genes.r2Eyes  = get_part(genes.eyes, 'eyes')
        genes.dMouth, genes.r1Mouth, genes.r2Mouth  = get_part(genes.mouth, 'mouth')
        genes.dEars, genes.r1Ears, genes.r2Ears  = get_part(genes.ears, 'ears')
        genes.dHorn, genes.r1Horn, genes.r2Horn  = get_part(genes.horn, 'horn')
        genes.dBack, genes.r1Back, genes.r2Back  = get_part(genes.back, 'back')
        genes.dTail, genes.r1Tail, genes.r2Tail = get_part(genes.tail, 'tail')
    
    return(genes)
        
        
def get_part(part_bin_full, part_type, bin_length=256,):
    """

    Parameters
    ----------
    part_bin_full : TYPE
        DESCRIPTION.
    part_type : TYPE
        DESCRIPTION.
    bin_length : TYPE, optional
        DESCRIPTION. The default is 256.

    Returns
    -------
    d_trait : TYPE
        DESCRIPTION.
    r1_trait : TYPE
        DESCRIPTION.
    r2_trait : TYPE
        DESCRIPTION.

    """
    
    part_type = part_type.lower()
    if bin_length == 256:
        d_part_class_bin = part_bin_full[2:6]
        r1_part_class_bin = part_bin_full[12:16]
        r2_part_class_bin = part_bin_full[22:26]
        
        d_part_class = classes_dict[d_part_class_bin].lower()
        r1_part_class = classes_dict[r1_part_class_bin].lower()
        r2_part_class = classes_dict[r2_part_class_bin].lower()
        
        d_part_bin = part_bin_full[6:12]
        r1_part_bin = part_bin_full[16:22]
        r2_part_bin = part_bin_full[26:32]
        
        traits = get_traits_json()
        
        d_trait = traits[d_part_class][part_type][d_part_bin]['global']
        r1_trait = traits[r1_part_class][part_type][r1_part_bin]['global']
        r2_trait = traits[r2_part_class][part_type][r2_part_bin]['global']
        
        
        return d_trait, r1_trait, r2_trait
        
        
        
        
        
        
        
        
        
        
        
        