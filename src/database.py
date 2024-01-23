import pymysql
import os

def connectToDatabase():
    try:
        # TODO SSL Settings
        return pymysql.connect(
            host=os.environ.get('MYSQL_HOST'),
            port=int(os.environ.get('MYSQL_PORT')),
            database=os.environ.get('MYSQL_DB'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            ssl_ca=os.environ.get('MYSQL_SSLCERT'),
            ssl_verify_cert=True,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        print(f'Unable to connect to database:\n\t{e}')
    
def getData(sqlQuery):
    connection = connectToDatabase()

    try:
        cursor = connection.cursor()
        cursor.execute(sqlQuery)
        return cursor.fetchall()
    except Exception as e:
        print(f'Unable to fetch data using query:\n\t \'{sqlQuery}\' \n\t{e}')
    finally:
        try:
            connection.close()
        except:
            print('Unable to close connection to database')
    
def insertData(abp, priority, date, time, capcode, region):
    connection = connectToDatabase()
    
    try:
        cursor = connection.cursor()

        sql = f'INSERT INTO site_meldingen (ABP, Prioriteit, Datum, Tijd, Capcode, Regio) VALUES (%s, %s, %s, %s, %s, %s);'
        val = (abp, priority, date, time, capcode, region)
        cursor.execute(sql, val)

        connection.commit()
        print('Record inserted')
    except:
        print(f'Unable to insert data into site_meldingen: \n\t{abp}\n\t{priority}\n\t{date}\n\t{time}\n\t{capcode}\n\t{region}')
    finally:
        try:
            connection.close()
        except:
            print("Unable to close connection to database")