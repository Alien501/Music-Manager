#Importing needed modules
import os,shutil
from tinytag import TinyTag as tt

def MusicMove(old_path,new_path,year,album,fileName):
    if year not in years:
        os.makedirs(music_dir+'\\'+year)
        years.add(year)
    if album not in album_created:
        try:
            os.makedirs(new_path)
        except:
            return None
        try:
            shutil.move(old_path,new_path)
        except:
            print('Skipped : ',fileName)
            return None
        album_created[album] = new_path
        song_moved[fileName] = new_path
    else:
        required_path = album_created[album]
        try:
            shutil.move(old_path,required_path)
        except:
            print('Skipped : ',fileName)
            return None
        song_moved[fileName] = required_path

def LrcOrg(filename,oldpath):
    if filename in song_moved:
        newFilepath = song_moved[filename]
        shutil.move(oldpath,newFilepath)
    else:
        pass

def start():
    global years, album_created, song_moved, music_dir
    
    music_dir = input('Enter your current directory: ')
    os.chdir(music_dir)
    os.makedirs(music_dir+'\\'+'lrc')
    default_lrc_path = music_dir+'\\'+'lrc'
    years = set()
    album_created = {}
    song_moved = {}
    contents = os.listdir(music_dir)
    for file in contents:
        if file[-4:].lower() == '.ini':
            continue
        elif file[-4:].lower() == '.lrc':
            file_name = file[0:-4]
            file_path = music_dir+'\\'+file
            shutil.move(file_path,default_lrc_path)
        else:
            file_name = file[0:-4]
            try:
                song_tag = tt.get(file)
            except:
                continue
            albumName = song_tag.album
            new_al = ''
            if albumName is None:
                continue
            for nm in albumName:
                if nm in '\/*?"<>:|':
                    continue
                else:
                    new_al+=nm
            albumYear = song_tag.year
            if albumYear == None:
                albumYear = 'Unknown'
            oldFilePath = music_dir+'\\'+file
            newFilePath = music_dir+'\\'+albumYear+'\\'+new_al
            MusicMove(oldFilePath,newFilePath,albumYear,new_al,file_name)
    
    print('Finished arranging music files...')
    print('Arranging lrc files...')
    
    lrc_content = os.listdir(default_lrc_path)
    for lrc_file in lrc_content:
        file_name = lrc_file[0:-4]
        oldpath = default_lrc_path+'\\'+lrc_file
        LrcOrg(file_name,oldpath)