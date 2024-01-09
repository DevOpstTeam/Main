menuWidth = 35

mainMenu = ['P2000 bericht', 'Selecteer filters', 'Exit']
filterMenu = ['Postcode', 'Tijd', 'Prioriteit', 'Exit']

# ============================= #

def showMainMenu():
    return showMenu('Hoofdmenu', mainMenu)

def showFilters():
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

def getLastMessage():
    # TODO: get latest message from database using the API
    print('Latest message')

# ============================= #

menuOption = showMainMenu()
while menuOption != len(mainMenu):
    if menuOption == 1:
        # P2000 bericht
        getLastMessage()
    if menuOption == 2:
        # Filter selectie
        filterOption = showFilters()
        # TODO: show menu for every filter
        print(f'Gekozen filter: {filterOption}')

    menuOption = showMainMenu()