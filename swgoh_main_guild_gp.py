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
    with conn:
        guild_update_time=players_gp_snapshot (conn)
        conn.commit()
        compare_all_guild_gp(conn,"13/02/2019",guild_update_time,True)
if __name__ == '__main__':
    main()
