import sys 
sys.path.insert(0, "..")
from io import StringIO
from csv import writer, reader
import pandas as pd
from util.xmlutils import *
import util.dbunit as dbunit

def checkForJustOneValue(arr: list):
    if len(arr) == 1:
        return 
    raise Exception("The array must have just one value!")

def createCSV(filename: str, column_name:list, values: list):
    output = StringIO()
    csv_writer = writer(output)

    for row in values:
        csv_writer.writerow(row)
    output.seek(0)
    df = pd.read_csv(output, header=None)
    df.columns = column_name 
    
    df.to_csv(filename, index=False)

def getCurrencyList():    
    currencyXML = XMLUtils("./eurofxref-hist-90d.xml")
    currency_conversion = currencyXML.getConversionRates("USD")
    
    currency_list = []
    for key, value in currency_conversion.items():
        currency_list.append((key, value))
    
    return currency_list

def createCurrencyTable(dbConnector: dbunit.DBConnector, values: list):

    try:
        sqlCreateCurrencyTable = '''
            CREATE TABLE IF NOT EXISTS Currency (
                id integer PRIMARY KEY AUTOINCREMENT,
                currency_type TEXT,
                datetime INTEGER,
                conversion_rate REAL
            )
        '''
        
        sqlInsertIntoCurrencies = '''
            INSERT INTO Currency (currency_type, datetime, conversion_rate) VALUES ('USD', ?, ?)
        '''

        dbConnector.createAndPopulateNewTable(sqlCreateCurrencyTable, sqlInsertIntoCurrencies, values)
    except Exception as err: 
        print(err)

def createDatabaseBackup(dbConnector: dbunit.DBConnector):
    sqlGetAllDevices = '''
        SELECT * FROM Devices
    '''

    sqlGetAllTransactions = '''
        SELECT * FROM Transactions
    '''

    all_devices, device_columns = dbConnector.executeQueryAndGetColumns(sqlGetAllDevices)
    all_transactions, transactions_columns =  dbConnector.executeQueryAndGetColumns(sqlGetAllTransactions)
    
    createCSV('./backup_devices.csv', device_columns, all_devices)
    createCSV('./backup_transactions.csv', transactions_columns, all_transactions)

def restoreDatabase(dbConnector: dbunit.DBConnector):
    """
    This function is used to restore the database to its initial values, 
    since they were changed in task4  
    """
    sqlDropTransactions = '''
        DROP TABLE Transactions;
    '''

    sqlDropDevices = '''
        DROP TABLE Devices;
    '''

    sqlDropCurrency = '''
        DROP TABLE Currency;
    '''

    dbConnector.executeQuery(sqlDropTransactions)
    dbConnector.executeQuery(sqlDropDevices)
    dbConnector.executeQuery(sqlDropCurrency)

    sqlCreateDevices = '''
        CREATE TABLE Devices(
            id INTEGER,
            device_name TEXT,
            PRIMARY KEY (id)
        ); 
    '''
    
    sqlCreateTransactions = '''
        CREATE TABLE Transactions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime INTEGER,
                visitor_id INTEGER,
                device_type INTEGER,
                revenue REAL,
                tax REAL,

                FOREIGN KEY(device_type) REFERENCES Devices(id)
            );
    '''

    dbConnector.executeQuery(sqlCreateDevices)
    dbConnector.executeQuery(sqlCreateTransactions)

    with open('./data/backup_devices.csv') as device_file:
        values = reader(device_file, delimiter=',', quotechar='|')
        sqlCreateDevices = '''
            INSERT INTO Devices(id, device_name) VALUES (?, ?); 
        '''
        list_values = list(values)
        dbConnector.populateTable(sqlCreateDevices, list_values[1:])
    
    with open('./data/backup_transactions.csv') as device_file:
        values = reader(device_file, delimiter=',', quotechar='|')
        sqlCreateDevices = '''
            INSERT INTO Transactions(id, datetime, visitor_id, device_type, revenue, tax) VALUES (?, ?, ?, ?, ?, ?); 
        '''
        list_values = list(values)
        dbConnector.populateTable(sqlCreateDevices, list_values[1:])







