import sys
import json
import requests
import numpy as np
import pandas as pd
from swgoh_api import *
from collections import OrderedDict

def all_mods(player,stat,thresh):
    #df_mods=pd.DataFrame(columns=['modId','allyCode','name',"Character","Slot","primary stat",'Tier'])
    row_list=[]
    for char in player['roster']:
        for mod in char['mods']:
            mod_dic=OrderedDict()
            mod_dic.update({'id':mod['id'],'allyCode':player['allyCode'],'Name':player['name'],"Character":char['nameKey'],
                           "Slot":mod['slot'],'tier':mod['tier'],'primary stat':mod['primaryStat']['unitStat']})
            
            for secondary_stat in mod['secondaryStat']:
                mod_dic.update({secondary_stat['unitStat']:secondary_stat['value']})
            row_list.append(mod_dic)
                #    df_mods=df_mods.append(dict(zip(df_mods.columns.to_list(),
                #                                    [mod['id']player['allyCode'],player['name'],char['nameKey'],mod['slot'],secondary_stat['value'],
                #                                     mod['tier'],secondary_stat['roll'],
                #                                     mod['primaryStat']['unitStat']])),ignore_index=True)
                    #for tr_one in thresh:
                    #    if secondary_stat['value']>=tr_one: tr_d[tr_one]+=1
                    #break
   # return mod_dic
    return pd.DataFrame.from_dict(row_list) 
allycode=int(input("Please enter the ally code of the player to fetch mods: "))
#project= {'language': 'eng_us','allycodes':928428534,'enums':True}
project= {'language': 'eng_us','allycodes':allycode,'enums':True}
one_payer=api_call(CONFIG, project, '%s/swgoh/players' % SWGOH_HELP)

all_my_mods=all_mods(one_payer[0],"UNITSTATSPEED",(1,10))

#all_my_mods.set_index(["Name","Character"]).sort_index().to_excel("my_mods.xlsx")
all_my_mods.set_index(["Name","Character"]).sort_index().to_csv(one_payer[0]['name']+'.csv')