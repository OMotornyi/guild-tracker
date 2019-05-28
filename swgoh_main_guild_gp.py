#!/usr/bin/python3
import sys
import json
import requests
from swgoh_data_track import *
from datetime import datetime, timedelta
from swgoh_api import *
from swgoh_db import *
import sqlite3
from sqlite3 import Error

def main():
    database = "second.db"
    conn = db_create_connection(database)
    isValid=False
#     while not isValid:
#         compare_option = input("""Type 1 if you want to compare guild GP for two given dates, type 2 if you want to make  a guild GP dump and compare with
#          one date, type 0 if you want make only a fresh dump of guild GP""")
#         #d1 = datetime.strptime(guild_update_time, "%d/%m/%Y")
#         try: # strptime throws an exception if the input doesn't match the pattern
#             compare = int(compare_option)
#             isValid=True
# #Perhaps set another try here.
#             #print (d1, type(d1))  # 2003-07-15 00:00:00 <type 'datetime.datetime'>
#             "convert datetime object to a 10 character string"
#             #d2 = str(d1)[:10]
#             #print (d2, type(d2))# 2003-07-15 <type 'str'>
#         except ValueError:
#             #print (what_error)
#             print ("Try again! dd/mm/yyyy\n")
    guild_update_time=user_input_date()
    with conn:
        current_time=players_gp_snapshot (conn)
        
        conn.commit()
        compare_all_guild_gp(conn,guild_update_time,current_time,True)
if __name__ == '__main__':
    main()
