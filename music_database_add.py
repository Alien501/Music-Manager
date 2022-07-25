# importing required modules
import os
try:
    from tinytag import TinyTag as TT
except:
    print("Missing module: TinyTag")
    print("Program Ends. . .")
import tables as db

# #Function to get contents of a folder
# def folder_open(path):
#     folder_contents = os.listdir(path)
#     return folder_contents

def escape_remover(path):
    try:
        if "\'" in path:
            path = path.split("\'")
            path = "\\'".join(path)
            return path
        else:
            return path
    except:
        pass

#Function to check LRC
def check_lrc(path,file):
    lrc_path = path+'\\'+file
    lrc_path = lrc_path.split('\\')
    lrc_path = escape_remover('\\\\'.join(lrc_path))
    lrc_title = escape_remover(file[:-4])
    db.lrc_database(lrc_title, lrc_path)

#Function to process music's meta-data
def music_data(path,sibilings, file):
    s_path = path+'\\'+file
    s_tag = TT.get(s_path)
    s_path = s_path.split('\\')
    s_path = escape_remover('\\\\'.join(s_path))
    s_title = escape_remover(s_tag.title)
    s_album = escape_remover(s_tag.album)
    s_artist = escape_remover(s_tag.artist)
    s_alart = escape_remover(s_tag.albumartist)
    s_bitrate = s_tag.bitrate
    s_duration = int(s_tag.duration)
    
    if file[:-4]+'.lrc' in sibilings or file[-5:] in sibilings:
        s_lrc = "A"
    else:
        s_lrc = "NA"
    
    # if len(s_tag.extra)>0:
    #     s_lyrics = "A"
    # else:
    #     s_lyrics = "NA"
    try:
        if len(s_tag.extra['lyrics'].strip()) > 0:
            s_lyrics = "A"
        else:
            s_lyrics = 'NA'
    except KeyError:
        s_lyrics = 'NA'
    
    if s_tag.year == None:
        s_year = "NA"
    else:
        s_year = s_tag.year

    if s_duration == None:
        s_duration = 000
    db.music_database(s_title, s_album, s_artist, s_alart,s_bitrate, s_lrc, s_lyrics, s_year, s_path, s_duration)

#Function to determine file or folder
# {1: Music File, 2: Unwanted, 3: Lrc, 4: Folder}
def datatype(file):
    if file[-4:].lower() in [".mp3", ".wav", ".ogg", ".wma", ".mp4", ".m4a", ".m4b", ".aiff-c"] or file[-5:].lower() in [".opus", ".flac", ".aiff"]:
        return 1
    elif file[-4:].lower() in ['.ini','.com','.com','.txt']:
        return 2
    elif file[-4:].lower() in [".lrc"]:
        return 3
    else:
        return 4


#Function to start the program
def main():
    while True:
        master_path = input("Enter Root Directory: ").strip()
        if len(master_path)==0:                                 # Checks whether empty space is input
            print("Enter a Valid Directory (or) 1 to goto Main Menu. . .")
            continue
        elif master_path == '1':
            return
        else:
            break
    try:
        walked_data = os.walk(master_path)
    except:
        print("Invalid directory...")
        return None
    print("Please wait a while. . .")
    print("Working with database. . .")
    print("Output: ")
    for i in walked_data:
        walking_path = i[0]
        walking_contents = [j for k in i[1:] if len(k)>0 for j in k]
        for file in walking_contents:
            file_datatype = datatype(file)
            if file_datatype == 4:
                continue
            elif file_datatype == 3:
                check_lrc(walking_path, file)
            elif file_datatype == 2:
                continue
            else:
                music_data(walking_path, walking_contents, file)
    print('Database updated. . .')
    db.close()
                
def key():
    db.conn_main()
    if db.conn.is_connected():
        main()
    else:
        print("Something went wrong with database connection...")
        db.close()
