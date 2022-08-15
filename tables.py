# Module to maintain database connection and table
from importlib.resources import path
import mysql.connector as sql

# Function for lyrics
def dis_lyrics(song_name):
    q = f'SELECT SONG_NAME, LYRICS, PATH FROM MUSICDATA WHERE SONG_NAME LIKE \'%{song_name}%\''
    cursor_obj.execute(q)
    final_data = cursor_obj.fetchall()
    if cursor_obj.rowcount > 0:
        print('Records Found:')

        i = 0
        while i < len(final_data):
            print(i+1,':',final_data[i][0])
            i += 1
        while True:
            try:
                req = int(input("Enter your choice: "))
                if req not in range(1, len(final_data)+1):
                    print('Invalid Input. . .')
                    continue
                else:
                    break
            except:
                print("Invalid Input. . .")
                continue
        return final_data[req-1]
    else:
        print(f'{song_name} not found in database. . .')


#Function for admin commands
def query(q):
    try:
        cursor_obj.execute(q)
    except:
        print("Somethig wrong with query...")
        print("QUERY: ",q)
        return None
    result = cursor_obj.fetchall()
    if cursor_obj.rowcount == 0:
        print("No Releated data available...")
    else:
        for final_re in result:
            print(final_re)


#Function to perform to give result for search query
def db_search(item_queried, type):
    d_dict =  {
        1 : "SONG_NAME",
        2 : "S_ALBUM",
        3 : "S_ARTISTS",
        4 : "AL_ARTIST",
        5 : "YEAR"
    }
    query = f"SELECT * FROM MUSICDATA WHERE {d_dict[type]} LIKE \'%{item_queried}%\'"
    cursor_obj.execute(query)
    fetched = cursor_obj.fetchall()
    if cursor_obj.rowcount == 0:
        print("No such item found...")
    else:
        i = 0
        while i<len(fetched):
            print("--> "*10,f"Name  : {fetched[i][0]}", f"Album : {fetched[i][1]}", f"Path  : {fetched[i][-3]}",sep='\n')
            i+=1
        print('--> '*10)
        
        while True:
            playlist = input("Export as Playlist [Y/N]: ").strip().lower()
            if playlist not in ("y","n"):
                print("Invalid input. . . ")
                continue
            else:
                break
        
        if playlist == 'y':
            while True:
                p_title = input("Enter playlist title: ").strip().title()
                if len(p_title) == 0:
                    print("Enter a valid title. . .")
                else:
                    while True:
                        ply_path = input("Enter directory to create playlist: ").strip()
                        if len(ply_path) == 0 or '\\' not in ply_path:
                            print("Enter a valid path. . .")
                            continue
                        break
                    break
            while True:
                cover = input("Do you wish to keep a cover image[Y/N]: ").strip().lower()
                if cover not in ('y','n'):
                    print("Invalid input...")
                    continue
                else:
                    if cover == 'y':
                        while True:
                            cover_loc = input("Enter cover location: ").strip()
                            if len(cover_loc) == 0:
                                print("Enter a valid path...")
                                continue
                            else:
                                break
                    break
            
            with open(ply_path+'\\'+p_title+'.m3u', 'w') as f:
                f.write("#EXTM3U\n")
                if cover == 'y':
                    f.write(f"#EXTIMG: front cover\n{cover_loc}\n")
                for file in fetched:
                    f.write(f"#EXTINF: {file[-1]}, {file[2]+' - '+file[0]}\n{file[-2]}\n")
            print("created...")
                
            
#Function to check presence of data
def check_data(file, file_type, path, album):
    if file_type == "L":
        q = f"select l_name from lrcdata where l_name = \'{file}\' and l_path = \'{path}\'"
    else:
        q = f"select song_name from musicdata where song_name = \'{file}\' and s_album = \'{album}\'"
    cursor_obj.execute(q)
    cursor_obj.fetchall()
    return cursor_obj.rowcount

#Function to maintain LRC Data
def lrc_database(lrc_name, path):
    if check_data(lrc_name, "L", path, "None") == 0:
        try:
            lrc_query = f"INSERT INTO LRCDATA VALUES('{lrc_name}', '{path}')"
            cursor_obj.execute(lrc_query)
            conn.commit()
        except:
            print(f"Skipped: {path}")
            print("Query:",lrc_query)
    else:
        pass


# Function to maintain database related to music data
def music_database(song_name, song_album, song_artist, al_artist, bit_rate, lrc_stat, lyrics, year, path, dur, type):
    if check_data(song_name, 'M', path, song_album) == 0:
        try:
            song_query = f"INSERT INTO MUSICDATA VALUES('{song_name}', '{song_album}', '{song_artist}','{al_artist}','{bit_rate}', '{lrc_stat}', '{lyrics}', '{year}', '{path}',{dur}, '{type}')"
            cursor_obj.execute(song_query)
            conn.commit()
        except:
            print('Skipped: {}'.format(path))
            print('Query:',song_query)
    else:
        song_query = f"UPDATE MUSICDATA SET LRC_STAT =  \'{lrc_stat}\',LYRICS= \'{lyrics}\',PATH =\'{path}\' WHERE SONG_NAME = \'{song_name}\'"
        cursor_obj.execute(song_query)
        conn.commit()
        pass

#Main Function
def conn_main():
    global conn, cursor_obj
    
    conn = sql.connect(host = "localhost", user ="root", passwd ="Alien@420")        #default password is root
    cursor_obj = conn.cursor()
    print("-"*30)
    try:
        cursor_obj.execute("CREATE DATABASE MUSICDATA")
        print("CREATED NEW DATABASE. . .")
    except:
        pass
    conn.commit()
    cursor_obj.execute("USE MUSICDATA")
    print("SELECTED DATABASE ✔")
    
    try:
        cursor_obj.execute("CREATE TABLE MUSICDATA(SONG_NAME TEXT, S_ALBUM TEXT, S_ARTISTS TEXT, AL_ARTIST TEXT, B_RATE TEXT,LRC_STAT VARCHAR(10), LYRICS VARCHAR(10), YEAR VARCHAR(10), PATH TEXT, Duration INT, TYPE VARCHAR(50))")
        print("TABLE-1 ✔")
        conn.commit()
    except:
        print("TABLE-1 ✔")
        pass
    
    try:
        cursor_obj.execute("CREATE TABLE LRCDATA(L_NAME TEXT, L_PATH TEXT)")
        print("TABLE-2 ✔")
        conn.commit()
    except:
        print("TABLE-2 ✔")
        pass
    print('-'*30)

#Function to close connection with database
def close():
    try:
        conn.commit()                   # Database connection may not be closed properly
        cursor_obj.close()
        conn.close()
    except:
        pass

# P R O G R A M     E N D S #
