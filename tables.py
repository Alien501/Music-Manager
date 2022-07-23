# Module to maintain database connection and table
import mysql.connector as sql

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
    query = "SELECT * FROM MUSICDATA WHERE {} LIKE \'%{}%\'".format(d_dict[type], item_queried)
    cursor_obj.execute(query)
    fetched = cursor_obj.fetchall()
    if cursor_obj.rowcount == 0:
        print("No such item found...")
    else:
        i = 0
        while i<len(fetched):
            print("--> "*10,"Name: {}".format(fetched[i][0].strip()), "Album: {}".format(fetched[i][1].strip()), "Path: {}".format(fetched[i][-2].strip()),sep='\n')
            i+=1
        print('--> '*10)
        
        while True:
            playlist = input("Do you wish to export them as playlist[Y/N]: ").strip().lower()
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
            
            with open(p_title+'.m3u', 'w') as f:
                f.write("#EXTM3U\n")
                if cover == 'y':
                    f.write("#EXTIMG: front cover\n{}\n".format(cover_loc))
                for file in fetched:
                    f.write("#EXTINF: {0}, {1}\n{2}\n".format(file[-1], file[2]+' - '+file[0], file[-2]))
            print("created...")
                
            
#Function to check presence of data
def check_data(file, file_type, path, album):
    if file_type == "L":
        q = "select l_name from lrcdata where l_name = \'{}\' and l_path = \'{}\'".format(file, path)
    else:
        q = "select song_name from musicdata where song_name = \'{}\' and s_album = \'{}\'".format(file, album)
    cursor_obj.execute(q)
    cursor_obj.fetchall()
    return cursor_obj.rowcount

#Function to maintain LRC Data
def lrc_database(lrc_name, path):
    if check_data(lrc_name, "L", path, "None") == 0:
        try:
            lrc_query = "INSERT INTO LRCDATA VALUES('{0}', '{1}')".format(lrc_name, path)
            cursor_obj.execute(lrc_query)
            conn.commit()
        except:
            print("Skipped: {}".format(path))
            print("Query:",lrc_query)
    else:
        pass


# Function to maintain database related to music data
def music_database(song_name, song_album, song_artist, al_artist, bit_rate, lrc_stat, lyrics, year, path, dur):
    if check_data(song_name, 'M', path, song_album) == 0:
        try:
            song_query = "INSERT INTO MUSICDATA VALUES('{0}', '{1}', '{2}','{3}','{4}', '{5}', '{6}', '{7}', '{8}',{9})".format(song_name, song_album, song_artist, al_artist, bit_rate, lrc_stat, lyrics, year, path, dur)
            cursor_obj.execute(song_query)
            conn.commit()
        except:
            print('Skipped: {}'.format(path))
            print('Query:',song_query)
    else:
        # song_query = "UPDATE MUSICDATA SET LRC_STAT =  \'{0}\',LYRICS= \'{1}\' WHERE SONG_NAME = \'{2}\'".format(lrc_stat, lyrics, song_name)
        # cursor_obj.execute(song_query)
        # conn.commit()
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
        cursor_obj.execute("CREATE TABLE MUSICDATA(SONG_NAME TEXT, S_ALBUM TEXT, S_ARTISTS TEXT, AL_ARTIST TEXT, B_RATE TEXT,LRC_STAT VARCHAR(10), LYRICS VARCHAR(10), YEAR VARCHAR(10), PATH TEXT, Duration INT)")
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
    conn.commit()
    cursor_obj.close()
    conn.close()

# P R O G R A M     E N D S #
