import pymysql
import os


def connectToDatabase():
    database = None
    try:
        database = pymysql.connect(
            host=os.environ.get('MYSQL_HOST'),
            port=os.environ.get('MYSQL_PORT'),
            db=os.environ.get('MYSQL_DB'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
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