import simplejson as json
import pymysql

databaseConfig = json.load(open('.config/databaseConfig.json'))

def connectToDatabase():
    database = None
    try:
        database = pymysql.connect(
            host=databaseConfig['host'],
            user=databaseConfig['username'],
            port=databaseConfig['port'],
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
    result = None
    connection = connectToDatabase()

    try:
        cursor = connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
    except:
        print(f'Unable to fetch data using query:\n\t \'{sqlQuery}\'')
    finally:
        try:
            connection.close()
        except:
            print('Unable to close connection to database')
        return result