import sqlite3



def creat_user_table(user):
    con = sqlite3.connect(f"users.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS userT(\
    id INTEGER,
    username TEXT
    )""")
    con.commit()
    cur.execute(f"SELECT id FROM userT WHERE id = {user.id}")
    data = cur.fetchone()
    if data is None:
        cur.execute("INSERT INTO userT VALUES(?, ?);", (user.id, user.user_name))
        con.commit()
        return True
    else:
        return False

def creat_users_pl_table(user_id,pl_name):
    try:
        con = sqlite3.connect(f'{user_id}.db')
        cur = con.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {pl_name} (\
        nameOfSong TEXT,
        songId TEXT
        )""")
    except: return False
    else:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS user_pl(\
        pl_names TEXT
        )""")
        con.commit()
        cur.execute(f"SELECT pl_names FROM user_pl WHERE pl_names = '{pl_name}'")
        data = cur.fetchone()
        if data is None:
            cur.execute(f"INSERT INTO user_pl(pl_names) VALUES('{pl_name}')")
            con.commit()
            cur.close()
            con.close()
            return True
        else:return False
def get_list_song(user_id,pl_name):
    con = sqlite3.connect(f"{user_id}.db")
    cur = con.cursor()
    arr = list()
    for i in cur.execute(f"""SELECT nameOfSong FROM {pl_name}""").fetchall():
        for k in i:
            arr.append(k)
    return arr
def insert_song(user_id,list_name,name,id):
    con = sqlite3.connect(f'{user_id}.db')
    cur = con.cursor()
    cur.execute(f"SELECT songId TEXT FROM {list_name} WHERE songId  = '{id}'")
    data = cur.fetchone()
    if data is None:
        cur.execute(f"INSERT INTO {list_name} VALUES(?, ?);", (name, id))
        con.commit()
def user_lists(user_id):
    try:
        userlist = list()
        con = sqlite3.connect(f'{user_id}.db')
        cur = con.cursor()
        for i in cur.execute(f"SELECT * FROM user_pl"):
            userlist.append(i[0])
        return userlist
    except:
        return False
def songs(user_id,name,id):
    con = sqlite3.connect(f'{user_id}.db')
    cur = con.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS songs(\
            nameOfSong TEXT,
            songId TEXT
            )""")
    cur.execute(f"SELECT songId TEXT FROM songs WHERE songId = '{id}'")
    data = cur.fetchone()
    if data is None:
        m = name.split('.m')[0]
        cur.execute(f"INSERT INTO songs VALUES(?, ?);", (m, id))
        con.commit()
def last_song(user_id,name):
    try:
        con = sqlite3.connect(f'{user_id}.db')
        cur = con.cursor()
        res = cur.execute(f"SELECT songId FROM songs WHERE nameOfSong = '{name}'").fetchall()
        return res[0][0]
    except:return False
def insert_song_into_list(user_id,list_name,name,id):
    try:
        con = sqlite3.connect(f'{user_id}.db')
        cur = con.cursor()
        cur.execute(f"SELECT nameOfSong FROM {list_name} WHERE nameOfSong = '{name}'")
        data = cur.fetchone()
        if data is None:
            m = name.split('.m')[0]
            cur.execute(f"INSERT INTO {list_name} VALUES(?, ?);", (m, id))
            con.commit()
            return True
    except:
        return False

def listenTo(user_id,list_name):
    con = sqlite3.connect(f'{user_id}.db')
    cur = con.cursor()
    arr = list()
    for i in cur.execute(f"""SELECT songId FROM {list_name}""").fetchall():
        for k in i:
            arr.append(k)
    return arr

def chat(user_id,music):
    try:
        con = sqlite3.connect(f'{user_id}.db')
        cur = con.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS chat(\
                    info INTEGER
                    )""")
        cur.execute(f"INSERT INTO chat(info) VALUES('{music}')")
        con.commit()
    except:print("asas1")

def delChat(user_id):
    try:
        con = sqlite3.connect(f'{user_id}.db')
        cur = con.cursor()
        arr = list()
        for i in cur.execute(f"""SELECT info FROM chat""").fetchall():
            for k in i:
                arr.append(k)
        cur.execute('DROP TABLE chat')
        return arr
    except:return False

def delSong(user_id,pln,name):
    try:
        con = sqlite3.connect(f'{user_id}.db')
        cur = con.cursor()
        cur.execute(f'DELETE FROM {pln} WHERE nameOfSong="{name}"')
        con.commit()
        return True
    except:return False

def delList(user_id,pln):
    try:
        con = sqlite3.connect(f'{user_id}.db')
        cur = con.cursor()
        cur.execute(f'DROP TABLE {pln}')
        cur.execute(f'DELETE FROM user_pl WHERE pl_names="{pln}"')
        con.commit()
        return True
    except:return False

