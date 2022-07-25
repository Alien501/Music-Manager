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