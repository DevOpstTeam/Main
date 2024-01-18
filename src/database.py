import pymysql
import yaml

databaseConfig = yaml.safe_load(open(".config/dbConfig.yaml"))

def connectToDatabase():
    database = None
    try:
        database = pymysql.connect(
            host=databaseConfig['host'],
            port=databaseConfig['port'],
            db=databaseConfig['dbName'],
            user=databaseConfig['username'],
            password=databaseConfig['password'],
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
    
def insertData(abp, priority, date, time, postcode):
    connection = connectToDatabase()
    
    try:
        cursor = connection.cursor()

        sql = f'INSERT INTO meldingen (ABP, Prioriteit, Datum, Tijd, Postcode) VALUES (%s, %s, %s, %s, %s);'
        val = (abp, priority, date, time, postcode)
        cursor.execute(sql, val)

        connection.commit()
        print(f'{cursor.rowcount} records inserted')
    except:
        print(f'Unable to insert data into meldingen: \n\t{abp}\n\t{priority}\n\t{date}\n\t{time}\n\t{postcode}')
    finally:
        try:
            connection.close()
        except:
            print("Unable to close connection to database")