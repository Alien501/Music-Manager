import music_database_add as md
import tables as dbm
import arrange as arrange
import other_features as ot


#function to deal with search
def search():
    dbm.conn_main()
    search_options = {
        1: "Title",
        2: "Album",
        3: "Artist",
        4: "Album Artist",
        5: "Year",
        6: "Admin Commands",
        7: "Main Menu"
    }
    
    print("Search based on: ")
    for options in search_options:
        print(options,':',search_options[options])
    
    print("-_"*30)
    while True:
        try:
            search_choice = int(input("Enter no. of option you wish to perform: "))
            if search_choice not in [1, 2, 3, 4, 5, 6, 7]:         #Can be replaced with range()
                print("Wrong Input, Only input No. within range...")
                continue
            else:
                break
        except:
            print("Only enter numeric character within given range...")
            continue
    print("-_"*30)
    
    if search_choice in range(1,6):
        while True:
            search_query = input(f"Enter {search_options[search_choice]} You are looking for: ").strip()
            if len(search_query) == 0:                                         #Checks whether empty space is input
                print("Invalid Input..., Try again...")
                continue
            else:
                break
        print("-_"*30)
        dbm.db_search(search_query, search_choice)
        search()
    elif search_choice == 6:
        print("/ # \\"*10)
        print("NOTE:\n1. ADMIN CMD ACCEPTS ONLY DIRECT SQL QUERIES")
        print("2. You will be working with raw data and orginal database")
        print("3. Execute command at your own risk")
        print("If you wish to quit enter 4, 1 to continue")
        print("/ # \\"*10)
        print("-_"*30)
        choice = input("Enter your wish: ").strip()    
        print("-_"*30)                         #Still not designated to get only input as integer(1/4)
        if int(choice) == 4:
            return None
        else:
            print("Key: ")
            dbm.query("DESC MUSICDATA")
        while True:
            print('[]'*30)
            user_query = input("Enter your: query: ").strip()
            dbm.query(user_query)
            while True:
                cont = input("[Y/N] Continue: ").strip().lower()
                if cont not in ['y', 'n']:
                    print("Wrong input...")
                    continue
                else:
                    break
            if cont == 'y':
                continue
            else:
                print('[]'*30)
                return None
    else:
        return None
    try:
        dbm.close()
    except:
        pass
        

#Function to deal main menu
def menu():
    choice_list = {
        1: "Update Music Database",
        2: "Search Database",
        3: "Arrange Music Folder",
        4: "Display Lyrics",
        5: "Quit"       #Last option will be always quit
        }        #List to keep track of features
    
    print("~-"*30)
    for i in choice_list:
        print(i,":",choice_list[i])
    print("~-"*30)
    
    while True:
        try:
            user_input = int(input("Enter no. of option you wish to perform: "))
            if user_input not in [1, 2, 3, 4, 5]:              #Can be replaced with range()
                print("Wrong Input, Only input No. within range...")
                continue
            else:
                break
        except:
            print("Only enter numeric character within given range...")
            continue
    
    if user_input == 1:
        md.key()
    elif user_input == 2:
        search()
    elif user_input == 3:
        # print("/ # \\"*10)            #FIXED
        # print("NOTE:")
        # print('1. For now it cant move flac files.')
        # print("/ # \\"*10)
        arrange.main()
    elif user_input == 4:
        dbm.conn_main()
        print("X ! . Song should be in database . ! X")
        ot.lyrics()
        dbm.close()
    else:
        print("- Coded By Alien 👽 -")
        return None
    menu()

menu()    