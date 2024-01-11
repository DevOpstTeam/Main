import pymysql
import json

mainMenu = ['P2000 bericht', 'Selecteer filters', 'Exit']
filterMenu = ['Postcode', 'Tijd', 'Prioriteit', 'Exit']

config = json.load(open('src/Config.json'))
databaseConfig = config["dbConfig"]

menuWidth = config["consoleMenuWidth"]

# == Interface Methods =================== #

def showMainMenu():
    return showMenu('Hoofdmenu', mainMenu)

def showFilterMenu(filterOption = 0):
    if filterOption == 0:
        return showMenu('Filters', filterMenu)
    elif filterOption == 1:
        postCode = showFilterPostcode()
        # TODO Set filter option to this postcode
        print(postCode)
    elif filterOption == 2:
        timeStart, timeEnd = showFilterTime()
        # TODO Set filter option to this timeframe
        print(timeStart, timeEnd)
    elif filterOption == 3:
        priority = showFilterPriority()
        # TODO Set filter option to this priority
        print(priority)

def showMenu(title, menuItems):
    print('')   # Start with a new line
    printTitle(title)
    # Print all the menu items
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
    print('')   # End with a new line
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

# Filter menu option postcode
def showFilterPostcode():
    printTitle('Postcode')
    postCode = input('| Selecteer een postcode [0000XX]: ')
    while not postCode[:4].isnumeric() or not postCode[4:].isalnum():
        postCode = input('| Selecteer een postcode [0000XX]: ')
    printBar()
    return postCode

# Filter menu option priority
def showFilterPriority():
    printTitle('Prioriteit')
    priority = int(input('| Selecteer een prioriteit [1-3]: '))
    while priority < 1 or priority > 3:
        priority = int(input('| Selecteer een prioriteit [1-3]: '))
    printBar()
    return priority

# Filter menu option time
def showFilterTime():
    printTitle('Tijd')
    startTime = input('| Selecteer een start datum []: ')
    endTime = input('| Selecteer een eind datum []: ')
    printBar()
    return startTime, endTime

# == Database Methods ==================== #

def connectToDatabase():
    database = None
    try:
        database = pymysql.connect(
            host=databaseConfig['host'],
            user=databaseConfig['username'],
            password=databaseConfig['password'],
            db=databaseConfig['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except:
        db = databaseConfig['database']
        host = databaseConfig['host']
        print(f'Unable to connect to database \'{db}\' on \'{host}\'')
    finally:
        return database
    
def getData(sqlQuery):
    latestMessage = 'No messages available'
    connection = connectToDatabase()

    try:
        cursor = connection.cursor()
        cursor.execute(sqlQuery)

        rows = cursor().fetchall()

        latestMessage = ''
        for row in rows:
            latestMessage += row + '\n'

    except:
        print(f'Unable to fetch data using query:\n\t \'{sqlQuery}\'')
    finally:
        try:
            connection.close()
        except:
            print('Unable to close connection to database')
        return latestMessage

# == Script ============================== #

menuOption = showMainMenu()
while menuOption != len(mainMenu):
    if menuOption == 1:
        # P2000 bericht
        query = "SELECT * FROM `users`"
        msg = getData(query)
        print(msg)
    if menuOption == 2:
        # Filter selectie
        filterOption = showFilterMenu()
        if filterOption != len(filterMenu):
            showFilterMenu(filterOption)

    menuOption = showMainMenu()