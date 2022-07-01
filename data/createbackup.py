from util.dbunit import *
from util.utils import *

def main():
    dbConnector = DBConnector("./transactions.db")
    createDatabaseBackup(dbConnector)

if __name__ == "__main__":
    main()