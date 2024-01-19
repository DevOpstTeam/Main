import pymysql
import os

def connectToDatabase():
    database = None
    try:
        database = pymysql.connect(
            host=os.environ.get('MYSQL_HOST'),
            port=int(os.environ.get('MYSQL_PORT')),
            db=os.environ.get('MYSQL_DB'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        print(f'Unable to connect to database{e}')
    finally:
        return database
    
def getData(sqlQuery):
    result = None
    connection = connectToDatabase()

    try:
        cursor = connection.cursor()
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
    except Exception as e:
        print(f'Unable to fetch data using query:\n\t \'{sqlQuery}\' {e}')
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
        print('Record inserted')
    except:
        print(f'Unable to insert data into meldingen: \n\t{abp}\n\t{priority}\n\t{date}\n\t{time}\n\t{postcode}')
    finally:
        try:
            connection.close()
        except:
            print("Unable to close connection to database")
