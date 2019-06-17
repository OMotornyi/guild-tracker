import sys
import json
import requests
import numpy as np
import pandas as pd
from swgoh_api import *
from collections import OrderedDict

def all_mods(player):
    #df_mods=pd.DataFrame(columns=['modId','allyCode','name',"Character","Slot","primary stat",'Tier'])
    row_list=[]
    for char in player['roster']:
        for mod in char['mods']:
            mod_dic=OrderedDict()
            mod_dic.update({'id':mod['id'],'allyCode':player['allyCode'],'Name':player['name'],"Character":char['nameKey'],
                           "Slot":mod['slot'],'tier':mod['tier'],'pips': mod['pips'],'lvl':mod['level'],'set':mod['set'],'primary stat':mod['primaryStat']['unitStat']})
            
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
    return row_list
    return pd.DataFrame.from_dict(row_list) 
allycode=int(input("Please enter the ally code of one of the guild's payer: "))
#project= {'language': 'eng_us','allycodes':928428534,'enums':True}
#project= {'language': 'eng_us','allycodes':allycode,'enums':True}
#one_payer=api_call(CONFIG, project, '%s/swgoh/players' % SWGOH_HELP)
guild=get_guild_full(CONFIG, allycode)
df=pd.DataFrame()
for g in guild:
    df=pd.concat([df,pd.DataFrame(data=g['roster'])])
df.set_index("allyCode",inplace=True)
df['gpChar'] = df['gpChar']/10**6
df['gpShip'] = df['gpShip']/10**6
df['gp'] = df['gp']/10**6

project= {'language': 'eng_us','allycodes':df.reset_index()["allyCode"].tolist(),'project':
          {'arena':1,'name':1,"allyCode":1,'guildRefId':1,"guildName":1,'roster':
           {'defId':1,'gear':1,'gp':1,"combatType":1}}}
players=api_call(CONFIG, project, '%s/swgoh/players' % SWGOH_HELP)
guildname=players[0]['guildName']
for player in players:
    df_player=pd.DataFrame(player['roster'])
    df.loc[player['allyCode'],'gp11+']=df_player[
        (df_player['combatType']==1) & (df_player['gear']>=11)]["gp"].sum()/10**6/df.loc[player['allyCode'],'gpChar']
    df.loc[player['allyCode'],'arena']=player['arena']['char']['rank']
list_of_rows=[]
for i in range(0,len(df),10):#len(df)
    project= {'language': 'eng_us', 'enums':True,'allycodes':df.iloc[i:i+10].reset_index()["allyCode"].tolist(),'project':
              {"allyCode":1, 'name':1, 'roster':
               {'nameKey':1, 'mods':1}}}
    players=api_call(CONFIG, project, '%s/swgoh/players' % SWGOH_HELP)
    for player in players:
        list_of_rows.extend(all_mods(player))
all_guild_mods=pd.DataFrame(list_of_rows)
#all_guild_mods.set_index(["Name","Character"]).sort_index().to_csv('guild_mods.csv')
all_guild_mods.to_csv(guildname+'_mods.csv')
df.to_csv(guildname+"_members.csv")



#all_my_mods=all_mods(one_payer[0],"UNITSTATSPEED",(1,10))

#all_my_mods.set_index(["Name","Character"]).sort_index().to_excel("my_mods.xlsx")
#all_my_mods.set_index(["Name","Character"]).sort_index().to_csv(one_payer[0]['name']+'.csv')