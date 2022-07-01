import sys 
sys.path.insert(0, "..")
import psycopg2
import csv
import sys

from util.utils import *

class PostgresConnector:
    def __init__(self, host: str, port:str, dbname: str, user: str, password: str):
        self.cursor = self.databaseConnection(host, port, dbname, user, password) 
    
    def databaseConnection(self, host: str, port:str, dbname: str, user: str, password: str):
        conn = psycopg2.connect(f'host={host} port={port} dbname={dbname} user={user} password={password}')
        conn.autocommit = True
        return conn.cursor()

    def executeQuery(self, query: str):
        self.cursor.execute(query) 
        result = self.cursor.fetchall()
        return result
    
    def executeQueryWithParams(self, query: str, params: list):
        self.cursor.execute(query, params)

    def executeMany(self, query: str, values: list):
        self.cursor.executemany(query, values)


def importFromCSV(dbConnector: PostgresConnector, filename: str, insertQuery: str):
    with open(filename) as csvfile:
        values = csv.reader(csvfile, delimiter=',', quotechar='|')

        list_values = list(values)
        dbConnector.executeMany(insertQuery, list_values[1:])

def selectVisitorWithMostRevenue(dbConnector: PostgresConnector):
    try:
        sql = '''
            SELECT visitor_id, MAX(sum_revenue) as max_revenue 
            FROM (
                SELECT visitor_id, SUM(revenue) as sum_revenue
                FROM Transactions as t
                GROUP BY visitor_id         
            ) AS visitorRevenue
            GROUP BY visitor_id ORDER BY max_revenue DESC;
        '''

        result = dbConnector.executeQuery(sql)
        visitor_id, revenue = result[0][0], result[0][1]

        print(f'The user: {visitor_id} has the most revenue ${revenue}')
    except Exception as err:
        print(err)

def selectDayWithMostRevenueForMobilePhone(dbConnector: PostgresConnector):
    try:
        sql = '''
            SELECT datetime, MAX(sum_revenue) as max_revenue
            FROM (
                SELECT datetime, SUM(revenue) as sum_revenue
                FROM Transactions AS t
                INNER JOIN Devices AS d ON d.id = t.device_type
                WHERE d.device_name = 'Mobile Phone' GROUP BY datetime
            ) AS datetimeRevenue
            GROUP BY datetime ORDER BY max_revenue DESC;
        '''

        result = dbConnector.executeQuery(sql)

        datetime, max_revenue = result[0][0], result[0][1]
      
        print(f'The date {datetime} has the most revenue ${max_revenue} for mobile phones')

    except Exception as err:
        print(err)

def main():

    postgresConnector = PostgresConnector('127.0.0.1', '5432', 'docker', 'root', 'password')
    sqlInsertDevices = '''
        INSERT INTO Devices (id, device_name) VALUES (%s, %s)
    '''
    sqlInsertTransactions = '''
        INSERT INTO Transactions (id, datetime, visitor_id, device_type, revenue, tax) VALUES (%s, %s, %s, %s, %s, %s)
    '''
    
    #importFromCSV(postgresConnector, './backup_devices.csv', sqlInsertDevices)
    #importFromCSV(postgresConnector, './backup_transactions.csv', sqlInsertTransactions)

    selectVisitorWithMostRevenue(postgresConnector)
    selectDayWithMostRevenueForMobilePhone(postgresConnector)


if __name__ == "__main__":
    main()
