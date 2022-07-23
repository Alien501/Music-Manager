import os, shutil
from tinytag import TinyTag as TT

# Function to modify path 
def path_changer(path_in):
    path_in = path_in.split('\\')
    path_in = '\\\\'.join(path_in)
    return path_in

# Function to move song
def s_move(ol_path, ne_path):
    try:
        os.makedirs(ne_path)
    except:
        pass
    try:
        shutil.move(ol_path, ne_path)
    except:
        print("Skipped: ", ol_path)
    

# Function to get song data
def s_data(file_path, sortOption):
    s_tag = TT.get(file_path)
    if sortOption == 1:
        year = s_tag.year
        if year == '0000' or year == None:
            year = 'NA'
        return year
    elif sortOption == 2:
        n_al = ''
        for i in str(s_tag.album):
            if i not in '\/*?"<>:|':
                n_al += i
        return n_al
    else:
        n_alart = ''
        for i in str(s_tag.albumartist):
            if i not in '\/*?"<>:|':
                n_alart+=i
        return n_alart
        

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

def main():
    global s_dict           # Dictionary to hold song:path pair for lrc

    s_dict = {}
    d_sort_op = {1: "Year",2: "Album", 3:"Album Artist"}

    master_dir = input("Enter music directory: ").strip()

    for i in d_sort_op:
        print(i,':',d_sort_op[i] )
    sort_option = int(input("Enter option: "))

    os.chdir(master_dir)            # Changing current directory
    master_contents = os.walk(master_dir)
    master_dir= path_changer(master_dir)
    try:
        os.makedirs(master_dir+'\\lrc')
    except:
        pass
    for in_cont in master_contents:
        path = in_cont[0]
        in_files = [j for k in in_cont[1:] if len(k)>0 for j in k]
        for file in in_files:
            file_path = path_changer(path+'\\'+file)
            file_type = datatype(file_path)
            if file_type == 1:
                if sort_option == 1:
                    data = s_data(file_path, 1)
                elif sort_option == 2:
                    data = s_data(file_path, 2)
                else:
                    data = s_data(file_path, 3)

                destination = path_changer(master_dir+'\\Sorted\\'+data+'\\')
                s_move(file_path, destination)
                if file[-4:].lower() in [".mp3", ".wav", ".ogg", ".wma", ".mp4", ".m4a", ".m4b", ".aiff-c"]:
                    s_dict[file[:-4]] = destination
                else:
                    s_dict[file[:-5]] = destination
            elif file_type == 3:
                try:            # Moving LRC file to common lrc file for later use
                    shutil.move(file_path, master_dir+'\\lrc\\')
                except:
                    pass
    
    a = input("Enter any key to continue: ")
        
    print("Arranging lrc. . .")
    if len(s_dict)>0:
        all_lrc = os.listdir(master_dir+'\\lrc\\')
        for lrc in all_lrc:
            if lrc[:-4] in s_dict:
                destination = s_dict[lrc[:-4]]
                s_move(master_dir+'\\lrc\\'+lrc, destination)
    else:
        print('No LRC Found...')

    try:
        os.close(master_dir)
    except:
        print('Skipped')
        
    print("All set...")