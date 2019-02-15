#!/usr/bin/python3

import sys
import json
import requests
from datetime import datetime, timedelta
from swgoh_api import *
from swgoh_db import *
import sqlite3
from sqlite3 import Error

def compare_player_gp (conn,time1, time2,player):
    database = "second.db"
    conn = db_create_connection(database)
    #datetime1=datetime.strptime(time1,'%d/%m/%Y')
    ##print (datetime1)
    #print(datetime1.strftime('%d/%m/%Y'))
    #print (time1,time2)
    #time1=datetime1.strftime('%d/%m/%Y')
    #with conn:
    time1_id=db_get_timestamp(conn,time1)
    #print(time1_id)
    time2_id=db_get_timestamp(conn,time2)
    #print(time2_id)
    if   time1_id[0]==0 or time2_id[0]==0:
     #   if time1
        print ("This character GP is not present in DB")
        return
    #print ("Both time stamps present")
    #print (time1_id)
    #print(time2_id)
    #player=db_query_player_id_name(conn,allycode)
    comp1 = db_query_gp_date(conn,player[0],time1_id[1])  
    #print (comp1)
    comp2 = db_query_gp_date(conn,player[0],time2_id[1])   
    print(player[1],"Character GP delta:",abs(comp1[0]-comp2[0]),"Ships GP delta:",abs(comp1[1]-comp2[1]))
    return (comp1,comp2)
def compare_all_guild_gp (conn, time1, time2, to_file):
    all_guild_player=db_query_all_players_id_name(conn)
    if to_file: 
        file = open("test_file.dat","w")
        file.write("%-28s %-10s %-10s \n"%("Name","Characters","Ships"))
    for player in all_guild_player:
        player_gp_dif=compare_player_gp(conn,time1,time2,player)
        if to_file: 
            file.write("%-28s %10i %10i \n"%(player[1],abs(player_gp_dif[0][0]-player_gp_dif[1][0]),abs(player_gp_dif[0][1]-player_gp_dif[1][1])))
    if to_file: file.close()
    return
def players_gp_snapshot (conn):
    guild_roster = api_swgoh_guilds(CONFIG,{
    #        'structure':True,
            'language': 'eng_us',
            'allycodes': [ 928428534 ],
            'project': {
                'roster': {
                    'allyCode': 1,
                    'name': 1,
                    'gp': 1,
                    'gpChar':1,
                    'gpShip': 1,
                },
                'updated': 1,
            },
    })
    
    updated_datetime = datetime.fromtimestamp(guild_roster[0]['updated']/1000)
    updated_date=updated_datetime.strftime('%d/%m/%Y')

    if db_get_timestamp(conn,updated_date)[0]==0:
        timestamp_id=db_insert_timestamp(conn,updated_date)
        #print(timestamp_id)
        #print(updated_date)
        for player_full in guild_roster[0]['roster']:
            player=(player_full['allyCode'],player_full['name'])
#        print(player)
            if db_check_player(conn,player_full['allyCode']):
                player_id=db_insert_player(conn,player)
                #print(player_id)
            else:
                player_id=db_query_player_id(conn,player_full['allyCode'])   
            gp_sql=(player_id,timestamp_id,player_full['gpShip'],player_full['gpChar'])
            gp_id=db_insert_gp(conn,gp_sql)
        return updated_date
    else:
        print("You have already updated the database today")
        return updated_date
    
#
# with conn:
#     up_time = datetime.fromtimestamp(gp_2[0]['updated']/1000)
#         #print(up_time)
#     str_up=up_time.strftime('%d/%m/%Y')

#     #first we check if the dump to db was already made today
#     if check_time(conn,str_up):
#         #add a new timestamp record to update_time table

#         timestamp_id=create_timestamp(conn,str_up)
#         for x in gp_2[0]['roster']:
#             player=(x['allyCode'],x['name'])
# #        print(player)
#             if check_player(conn,x['allyCode']):
#                 player_id=create_player(conn,player)
#                 print(player_id)
#             player_id=select_player_id(conn,x['allyCode'])
#             gp_sql=(player_id,timestamp_id,x['gpShip'],x['gpChar'])
#             gp_id=create_gp(conn,gp_sql)
#             #print(player_id,timestamp_id)
#             comp = select_gp_for_dif(conn,player_id,1)
#             #print(x)
#             #print(comp)
#             #print(x['name'],"Character GP NEW",x['gpChar'],"Ships GP NEW:",x['gpShip'])
#             #print(x['name'],"Character GP OLD:",comp[1],"Ships GP OLD:",comp[2])
#             print(x['name'],"Character GP delta:",-comp[0]+x['gpChar'],"Ships GP delta:",-comp[1]+x['gpShip'])

#         # else:
#         #     print("player already in the DB")

#     else:
#         print("You have already updated today")
    
# #print(json.dumps(gp_1[0]['roster'][0	],indent=4))
# #print(json.dumps(d2, indent=4))
# #print(d2)
# #print(json.dumps(gp_total[0]['roster'],indent=4))
# #print(gp_total[0]['updated'])
# # for x in gp_2[0]['roster']:
# # 	x["gpChar_dif"]=0
# # 	#print(x)
# # 	for i,y in enumerate(gp_1[0]['roster']):
# # 		if y["allyCode"]==x["allyCode"]:
# # 			x["gpChar_dif"]=x['gpChar']-y['gpChar']
# # 			gp_1[0]['roster'].pop(i)
# # 	#		print(len(gp_1[0]['roster']))
# # 			break
# # 	#print(x)
# # for x in gp_2[0]['roster']:
# # 	print(x['name'],x['gpChar_dif'])
# #now = datetime.now()
# #timestamp = datetime.timestamp(now)
# #print( timestamp)
# #dt_object = datetime.fromtimestamp(gp_total[0]['updated']/1000)
# #print("dt_object =", dt_object.date())
# #print(dt_object.day,dt_object.month,dt_object.year)
# #dic=d2[0]
# #for x in dic["roster"]:#
# #	print(x["name"])
# #	print(x['gpChar'])
# #for x,y in dic.items():
# #	print(x)
# #print(len(dic['roster']))
# #with open ("guild2.json","w") as write_file:
# #    json.dump(d2,write_file,indent=4)