import sqlite3

class DBConnector:
    def __init__(self, dbname):
        self.dbname = dbname
        self.connection = sqlite3.connect(dbname)
    
    def executeQuery(self, query):
        cur = self.connection.cursor()
        rows = cur.execute(query).fetchall()
        return rows

    def executeUpdateQuery(self, query):
        self.connection.execute(query)
        self.connection.commit()


    def executeQueryWithParams(self, query, params):
        cur = self.connection.cursor()
        rows = cur.execute(query, params).fetchall()
        return rows

    def executeQueryAndGetColumns(self, query):
        cur = self.connection.cursor()
        rows = cur.execute(query).fetchall()
        columns = list(map(lambda x: x[0], cur.description))
        return rows, columns


    def createAndPopulateNewTable(self, createTable, populateTable, rows):
        try:
            self.connection.execute(createTable) 
            self.connection.executemany(populateTable, rows)
            self.connection.commit()

        except Exception as err:
            print(err)
    