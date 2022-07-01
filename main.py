from util.dbunit import DBConnector
from tasks import *

def main():
    dbConnector = DBConnector("./data/transactions.db")
    print("-------TASK1-------")
    task1(dbConnector)    
    print("-------TASK2-------")
    task2(dbConnector)
    print("-------TASK3-------")
    task3(dbConnector)
    task4(dbConnector)
    
    usr_input = input("Press enter to restore database...")
    print("Restoring the database ...")
    restoreDatabase(dbConnector)

if __name__ == "__main__":
    main()