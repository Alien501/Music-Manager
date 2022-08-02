import tables
from tinytag import TinyTag as tt

# Function to retrive lyrics from songs Metadata

def lyrics():
    while True:
        s_name = input('Enter song name: ').strip()
        if len(s_name) == 0:
            print("Enter a valid name. . .")
            continue
        else:
            break
    op = tables.dis_lyrics(s_name)

    if op != None:
        print(' - '*30)
        if op[1] == 'A':
            tag = tt.get(op[2])
            for i in tag.extra['lyrics'].split('\n'):
                print(i.strip())
        else:
            print("Lyrics not found. . .")
        print(' - '*30)
        
    while True:
        cont = input("[Y/N] Continue: ").strip().lower()
        if cont not in ['y', 'n']:
            print("Wrong input...")
            continue
        break
    if cont == 'y':
        lyrics()
    else:
        return
    
# Function to port playlist from pc to android
def port_play():
    while True:
        play_loc = input('Enter playlist path: ').strip()
        if '\\' not in play_loc or play_loc[-4:].lower() != '.m3u' or len(play_loc) == 0:
            print('Enter a valid path. . .')
            continue
        break
    try:
        with open(play_loc, 'r') as f:
            data = f.readlines()
            print('Sample location from playlist file:', data[2], sep='\n')
    except:
        print(f'File {play_loc} not found. . .')
        return

    while True:
        rep  = input('Enter common path from above: ').strip()
        if '\\' not in rep or len(rep) == 0:
            print("Enter a valid path. . .")
            continue
        else:
            while True:
                tex = input('Enter common path in new device: ').strip()
                if '\\' not in tex or len(tex) == 0:
                    print("Enter a valid path. . .")
                    continue
                break
            break
    play_loc = play_loc[:-4]+' NEW '+play_loc[-4:]

    with open(play_loc, 'w') as f:
        for i in data:
            if rep in i:
                i = i.replace(rep, tex)
                i = i.split('\\\\')
                i = '/'.join(i)
                f.write(i)
            else:
                f.write(i)
    print('Replaced. . .')

