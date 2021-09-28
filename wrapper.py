# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 21:43:50 2021

@author: Charles
"""

import numpy as np
import requests as r
import json

url = 'https://axieinfinity.com/graphql-server-v2/graphql'

# "0x60f1dcc9a01c4f0f6a511d99efc48a96d243e7e9"

def get_axie_market_list(
        size = 20,
        sort = 'PriceAsc',
        auction_type = 'Sale',
        owner = None,
        parts = None,
        classes = None,
        stages = 4,
        pureness = None,
        breed_count = None,
        hp = [],
        skill = [],
        speed = [],
        morale = [],
    ):
    """
    
    Parameters
    ----------
    size : int, optional
        Number of results to return. The default is 20.
    sort : str, optional
        Results sort method. PriceAsc, PriceDesc, IdAsc, IdDesc, Latest. The default is 'PriceAsc'.
    auction_type : str, optional
        Whether or not axie for sale. All, Sale, NotForSale. The default is 'Sale'.
    owner : str, optional
        Ronin address of the owner. The default is None.
    parts : list of str, optional
        Parts to filter for. Example: ['tail-yam', 'horn-rose-bud']. The default is None.
    classes : list of str, optional
        Classes to filter for. Example: ['Beast', 'Aquatic']. Beast, Aquatic, Plant, Bird, Bug, Reptile, Mech, Dawn, Dusk. The default is None.
    stages : int, optional
        Egg or Mature axies. The default is 4.
    pureness : list of int, optional
        Purity of axies. Example: [1, 3]. The default is None.
    breed_count : list of int, optional
        Breed count of axies. Example: [1, 4]. The default is None.
    hp : list of int, optional
        HP filter. [<min>, <max>.] The default is [].
    skill : list of int, optional
        Skill filter. [<min>, <max>]. The default is [].
    speed : list of int, optional
        Speed filter. [<min>, <max>]. The default is [].
    morale : list of int, optional
        Morale filter. [<min>, <max>]. The default is [].

    Returns
    -------
    JSON with results in str.

    """

    body = {"operationName":"GetAxieBriefList",
            "variables": json.dumps({
                "from":0,
                "size": size,
                "sort": sort,
                "auctionType": auction_type,
                "owner": owner,
                "criteria":{
                    # "region": 'null',
                    "parts": parts,
                    # "bodyShapes": 'null',
                    "classes": classes,
                    "stages": stages,
                    # "numMystic": 'null',
                    "pureness": pureness,
                    # "title": 'null',
                    # "breedable": 'null',
                    "breedCount": breed_count,
                    "hp": hp,
                    "skill": skill,
                    "speed": speed,
                    "morale": morale
                    }
                }),
           "query": "query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n birthDate\n breedCount\n  image\n  genes\n  title\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n"
           }

    response_text = r.post(url, data=body).text
    data = json.loads(response_text)
    axies = data['data']['axies']['results']
    return(axies)
    

# body = {"operationName":"GetAxieDetail","variables":{"axieId":"2245218"},"query":"query GetAxieDetail($axieId: ID!) {\n  axie(axieId: $axieId) {\n    ...AxieDetail\n    __typename\n  }\n}\n\nfragment AxieDetail on Axie {\n  id\n  image\n  class\n  chain\n  name\n  genes\n  owner\n  birthDate\n  bodyShape\n  class\n  sireId\n  sireClass\n  matronId\n  matronClass\n  stage\n  title\n  breedCount\n  level\n  figure {\n    atlas\n    model\n    image\n    __typename\n  }\n  parts {\n    ...AxiePart\n    __typename\n  }\n  stats {\n    ...AxieStats\n    __typename\n  }\n  auction {\n    ...AxieAuction\n    __typename\n  }\n  ownerProfile {\n    name\n    __typename\n  }\n  battleInfo {\n    ...AxieBattleInfo\n    __typename\n  }\n  children {\n    id\n    name\n    class\n    image\n    title\n    stage\n    __typename\n  }\n  __typename\n}\n\nfragment AxieBattleInfo on AxieBattleInfo {\n  banned\n  banUntil\n  level\n  __typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    __typename\n  }\n  __typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  __typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  __typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n"}






if __name__ == '__main__':
    
    classes = ['Aquatic']
    parts = ['tail-nimo', 'mouth-risky-fish', 'horn-dual-blade', 'horn-little-branch', 'horn-pocky', 'back-goldfish']
    pureness = [5]
    speed = [54, 55, 56, 57]
    
    axies = get_axie_market_list(parts=parts, classes=classes, speed=speed)
    
    for axie in axies:
        print('ID:', axie['id'])
        print('Price:', np.round(float(axie['auction']['currentPrice'])/10e18, 4))
        print('USD:', axie['auction']['currentPriceUSD'])
        print()
    
