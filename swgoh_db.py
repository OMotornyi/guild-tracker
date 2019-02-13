import sqlite3
from sqlite3 import Error
def select_gp_for_dif(conn,player_id,date_id):
     sql = '''SELECT gpchars,gpships, allycode, name
             FROM gp 
            INNER JOIN update_time on update_time.id = gp.updatetime_id
            INNER JOIN players on players.id=gp.player_id
            WHERE update_time.id=?
            AND players.id=?
      '''
     cur=conn.cursor()
     cur.execute(sql,[date_id,player_id])
     return cur.fetchone()
def create_gp(conn,gp):
    sql = '''INSERT INTO gp(player_id,updatetime_id,gpships,gpchars)
             VALUES(?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, gp)
    return cur.lastrowid
def create_timestamp(conn,time):
    sql = '''INSERT INTO update_time(snapshot) VALUES(?)'''
    cur = conn.cursor()
    cur.execute(sql,(time,))
    return cur.lastrowid
def select_player_id(conn,ally):
    cur=conn.cursor()
    cur.execute("SELECT id FROM players WHERE allycode=?",(ally,) )
    return cur.fetchone()[0]
def check_time(conn,time):
    cur=conn.cursor()
    cur.execute("SELECT count(*) FROM update_time WHERE snapshot =?",(time,))
    data=cur.fetchone()[0]
    if data ==0:
        return True
    else:
        return False
def create_player(conn,player):
    #add a player to DB
    sql = '''INSERT INTO players(allycode, name)
             VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, player)
    return cur.lastrowid
def check_player(conn,allyC):
    cur=conn.cursor()
    cur.execute("SELECT count(*) FROM players where allycode =?",(allyC,))
    data=cur.fetchone()[0]
    if data ==0:
        return True
    else:
        return False
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
def main():
    database = "/home/motornyi/SWGOH_API/second.db"
 
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """
 
    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""
    sql_create_players_table = """ CREATE TABLE IF NOT EXISTS players (
                                        id integer PRIMARY KEY,
                                        allycode integer UNIQUE NOT NULL,
                                        name text NOT NULL
                                    ); """
    sql_create_time_table = """ CREATE TABLE IF NOT EXISTS update_time (
                                        id integer PRIMARY KEY,
                                        snapshot text UNIQUE NOT NULL
                                    ); """    
    sql_create_gp_table= """ CREATE TABLE IF NOT EXISTS gp (
                                        id integer PRIMARY KEY,
                                        player_id integer,
                                        updatetime_id integer,
                                        gpships integer,
                                        gpchars integer,
                                        FOREIGN KEY (player_id) REFERENCES players (id),
                                        FOREIGN KEY (updatetime_id) REFERENCES update_time (id)

                                    ); """
    # create a database connection
    conn = create_connection(database)
    with conn:
        # create projects table
#        create_table(conn, sql_create_projects_table)
        # create tasks table
 #       create_table(conn, sql_create_tasks_table)
 #       player=(928428534,'Lossberg')
 #       player_id=create_player(conn,player)
 #       print(player)
        # player=(3,'Lossberg')
        # player_id=create_player(conn,player);
        # print(player_id)
        #conn.close()
        create_table(conn, sql_create_players_table)
        create_table(conn,sql_create_time_table)
        create_table(conn,sql_create_gp_table)

 
if __name__ == '__main__':
    main()