import util.dbunit as dbunit 
from util.utils import *

def task1(dbConnector: dbunit.DBConnector):
    try:
        selectMostRevenueCustomer = '''
        SELECT visitor_id, MAX(revenue_sum) as max_revenue 
        FROM (
            SELECT visitor_id, SUM(revenue) as revenue_sum
                FROM
                Transactions GROUP BY visitor_id
            )
        '''
        result = dbConnector.executeQuery(selectMostRevenueCustomer)
        checkForJustOneValue(result) 

        visitor_id, revenue = result[0][0], result[0][1]
        print(f'The user: {visitor_id} has the most revenue ${revenue}')
   
    except Exception as err:
        print(err)

def task2(dbConnector: dbunit.DBConnector):
    try:
        selectDateWithMostRevenueForMobilePhones = '''
            SELECT datetime, MAX(revenue_sum) as max_revenue
            FROM (
                SELECT datetime, SUM(revenue) as revenue_sum 
                    FROM
                Transactions as t
                INNER JOIN Devices as d ON t.device_type = d.id 
                WHERE d.device_name = 'Mobile Phone' GROUP BY datetime
            )
        '''

        result = dbConnector.executeQuery(
            selectDateWithMostRevenueForMobilePhones)
        checkForJustOneValue(result)

        datetime, max_revenue = result[0][0], result[0][1]
      
        print(f'The date:{datetime} has the most revenue ${max_revenue} for mobile phones')
        
    except Exception as err:
        print(err)
    
def task3(dbConnector: dbunit.DBConnector, fileName: str = "./devicesjointransactions.csv"):
    try:
        joinTransactionsAndDevices = '''
            SELECT 
                t.id,
                t.datetime,
                t.visitor_id,
                t.revenue,
                t.device_type,
                d.device_name
            FROM Transactions as t
            INNER JOIN Devices as d 
            ON t.device_type = d.id
        '''
        result, column_names = dbConnector.executeQueryAndGetColumns(joinTransactionsAndDevices)
        
        createCSV(fileName, column_names, result)
        print(f'TASK 3: Created new file {fileName}')

    except Exception as err:
        print(err)


def task4(dbConnector: dbunit.DBConnector):
    try:
        currencies = getCurrencyList()  
        createCurrencyTable(dbConnector, currencies)  

        sqlUpdateDatesNotInCurrency = '''
            UPDATE Transactions as t
            SET revenue = revenue / (SELECT SUM(conversion_rate)/COUNT(*) FROM Currency)
            WHERE t.datetime NOT IN (
                SELECT t.datetime
                FROM Transactions AS t 
                INNER JOIN Currency AS c ON 
                c.datetime = t.datetime
            )
        '''
        dbConnector.executeUpdateQuery(sqlUpdateDatesNotInCurrency)

        sqlUpdateDatesInCurrency = '''
            UPDATE Transactions as t 
            SET revenue = (
                SELECT t.revenue / c.conversion_rate 
                FROM Currency as c 
                WHERE t.datetime = c.datetime
            )
            WHERE t.datetime = (
                SELECT t.datetime
                FROM Transactions AS t 
                INNER JOIN Currency AS c ON 
                c.datetime = t.datetime 
            )
        '''
        dbConnector.executeUpdateQuery(sqlUpdateDatesInCurrency)        

    except Exception as err:
        print(err)