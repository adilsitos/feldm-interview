import sqlite3

class DBConnector:
    def __init__(self, dbname: str):
        self.dbname = dbname
        self.connection = sqlite3.connect(dbname)
    
    def executeQuery(self, query: str):
        self.connection.execute(query)
        self.connection.commit()

    def executeSelectQuery(self, query: str):
        cur = self.connection.cursor()
        rows = cur.execute(query).fetchall()
        return rows

    def executeUpdateQuery(self, query: str):
        self.connection.execute(query)
        self.connection.commit()

    def executeQueryWithParams(self, query: str, params: str):
        cur = self.connection.cursor()
        rows = cur.execute(query, params).fetchall()
        return rows

    def executeQueryAndGetColumns(self, query: str):
        cur = self.connection.cursor()
        rows = cur.execute(query).fetchall()
        columns = list(map(lambda x: x[0], cur.description))
        return rows, columns
    
    def populateTable(self, query: str, values: list):
        try:
            self.connection.executemany(query, values)
            self.connection.commit()
        except Exception as err:
            print(err)

    def createAndPopulateNewTable(self, createTable:str, populateTable: str, rows:str):
        try:
            self.connection.execute(createTable) 
            self.connection.executemany(populateTable, rows)
            self.connection.commit()

        except Exception as err:
            print(err)
    