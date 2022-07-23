# Code to shift spotify playlist with offline songs

def keyPlay():
    while True:
        playlist = input("Enter playlist path: ").strip()
        if len(playlist) == 0 or playlist[-4:].lower() != '.m3u':
            print('! Not a valid Playlist path !')
            print('Enter 1 to goto Main Menu')
            continue
        elif playlist == '1':
            return
        else:
            break

    while True:
        old_text = input('Enter text to be replaced: ').strip()
        if len(old_text) == 0:
            print('Enter a valid text. . .')
            continue
        else:
            while True:
                new_text = input('Enter text to replace: ').strip()
                if len(new_text) == 0:
                    print('Enter a valid text. . .')
                    continue
                else:
                    break
            break
    



keyPlay() 