#!/usr/bin/python3

import sys
import json
import requests
from datetime import datetime, timedelta
from swgoh_api import *


#d2 = api_swgoh_guilds(CONFIG,{
#        'structure':True,
#        'language': 'eng_us',
#        'allycodes': [ 928428534 ],
#})
if False:
  gp_total = api_swgoh_guilds(CONFIG,{
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
else:
 with open ("MECQ_GP.json",'r') as json_file:
		gp_total=json.load(json_file)
 with open ("MECQ_GP_1.json",'r') as json_file:
		gp_1=json.load(json_file)
 with open ("MECQ_GP_2.json",'r') as json_file:
		gp_2=json.load(json_file)
#print(json.dumps(gp_1[0]['roster'][0	],indent=4))
#print(json.dumps(d2, indent=4))
#print(d2)
#print(json.dumps(gp_total[0]['roster'],indent=4))
#print(gp_total[0]['updated'])
for x in gp_2[0]['roster']:
	x["gpChar_dif"]=0
	#print(x)
	for i,y in enumerate(gp_1[0]['roster']):
		if y["allyCode"]==x["allyCode"]:
			x["gpChar_dif"]=x['gpChar']-y['gpChar']
			gp_1[0]['roster'].pop(i)
	#		print(len(gp_1[0]['roster']))
			break
	#print(x)
for x in gp_2[0]['roster']:
	print(x['name'],x['gpChar_dif'])
#now = datetime.now()
#timestamp = datetime.timestamp(now)
#print( timestamp)
#dt_object = datetime.fromtimestamp(gp_total[0]['updated']/1000)
#print("dt_object =", dt_object.date())
#print(dt_object.day,dt_object.month,dt_object.year)
#dic=d2[0]
#for x in dic["roster"]:#
#	print(x["name"])
#	print(x['gpChar'])
#for x,y in dic.items():
#	print(x)
#print(len(dic['roster']))
#with open ("guild2.json","w") as write_file:
#    json.dump(d2,write_file,indent=4)