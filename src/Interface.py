import pymysql

menuWidth = 35

mainMenu = ['P2000 bericht', 'Selecteer filters', 'Exit']
filterMenu = ['Postcode', 'Tijd', 'Prioriteit', 'Exit']

dbHost = 'localhost'
dbUser = 'root'
dbPass = 'password'
dbDatabase = 'mydatabase'

# = Interface Methods =================== #

def showMainMenu():
    return showMenu('Hoofdmenu', mainMenu)

def showFilterMenu():
    return showMenu('Filters', filterMenu)

def showMenu(title, menuItems):
    printTitle(title)
    for option, currentMenuItem in enumerate(menuItems):
        menuItem = f'| [{option + 1}] {currentMenuItem}'
        tail = (menuWidth - len(menuItem) - 1) * ' '
        print(menuItem + tail + '|')
    printBar()

    return getMenuOption(f'Kies een optie (1-{len(menuItems)}): ', len(menuItems))

def getMenuOption(question, maxMenuOption):
    option = input(question)
    while not option.isnumeric() or (int(option) > maxMenuOption or int(option) < 1):
        option = input(question)
    return int(option)

def printTitle(title):
    bars = ((menuWidth - len(title) - 4) // 2) * '='
    titleText = '|' + bars + ' ' + title + ' ' + bars
    if len(title) % 2 == 1 and menuWidth % 2 == 0:
        titleText += '='
    print(titleText + '|')

def printBar():
    bar = (menuWidth - 2) * '='
    print(f'|{bar}|')

# = Database Methods ==================== #

def connectToDatabase():
    database = None
    try:
        database = pymysql.connect(
            host=dbHost,
            user=dbUser,
            password=dbPass,
            db=dbDatabase,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except:
        print(f'Unable to connect to database \'{dbDatabase}\' on \'{dbHost}\'')
    finally:
        return database
    
def getLastMessage():
    latestMessage = 'No messages available'
    connection = connectToDatabase()

    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM `users`"
        cursor.execute(sql)

        rows = cursor().fetchall()

        for row in rows:
            print(row)

        connection.close()
    except:
        return latestMessage
    else:
        connection.close()
        return latestMessage

# = Script ============================== #

menuOption = showMainMenu()
while menuOption != len(mainMenu):
    if menuOption == 1:
        # P2000 bericht
        msg = getLastMessage()
        print(msg)
    if menuOption == 2:
        # Filter selectie
        filterOption = showFilterMenu()
        # TODO: show menu for every filter
        print(f'Gekozen filter: {filterOption}')

    menuOption = showMainMenu()