import sys 
sys.path.insert(0, "..")
from util.dbunit import *
from util.utils import *

def main():
    dbConnector = DBConnector("../data/transactions.db")
    createDatabaseBackup(dbConnector)

if __name__ == "__main__":
    main()