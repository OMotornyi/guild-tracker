from collections import OrderedDict
from os import path
import json
def calculate_secondaries(player,stat,thresh):
    """ Calculates the number of mods for 'player' that meet certain threshold,
    i.e. mods for which the value of the secondary stat 'stat' >= threshold value 'thresh
    """
    tr_d=dict(zip(thresh,[0]*len(thresh)))
    for char in player['roster']:
        for mod in char['mods']:
            for secondary_stat in mod['secondaryStat']:
                if secondary_stat['unitStat']==stat:
                    for tr_one in thresh:
                        if secondary_stat['value']>=tr_one: tr_d[tr_one]+=1
                    break
    return tr_d   

def all_mods(player):
    """For the given player's roster obtained via swgoh.help API return a list of OrderedDict containing every equiped mod and corresponding stats.
    """
    row_list=[]
    for char in player['roster']:
        for mod in char['mods']:
            mod_dic=OrderedDict()
            mod_dic.update({'id':mod['id'],'allyCode':player['allyCode'],'Name':player['name'],"Character":char['nameKey'],
                           "Slot":mod['slot'],'tier':mod['tier'],'pips': mod['pips'],'lvl':mod['level'],
                           'set':mod['set'],'primary stat':mod['primaryStat']['unitStat']})
            
            for secondary_stat in mod['secondaryStat']:
                mod_dic.update({secondary_stat['unitStat']:secondary_stat['value']})
            row_list.append(mod_dic)
    return row_list

def get_unit_stat_loc(file_path):
    #from os import path
    if path.isfile(file_path):
        with open (file_path) as json_file:
            return json.load(json_file)