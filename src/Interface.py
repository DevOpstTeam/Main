import pymysql
import json

menuWidth = 35

mainMenu = ['P2000 bericht', 'Selecteer filters', 'Exit']
filterMenu = ['Postcode', 'Tijd', 'Prioriteit', 'Exit']

databaseConfig = json.load(open('src/dbConfig.json'))

# == Interface Methods =================== #

def showMainMenu():
    return showMenu('Hoofdmenu', mainMenu)

def showFilterMenu():
    return showMenu('Filters', filterMenu)

def showMenu(title, menuItems):
    print('')   # Print a new line
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
    print('')   # Print a new line
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
        # TODO: show menu for every filter
        print(f'Gekozen filter: {filterOption}')

    menuOption = showMainMenu()