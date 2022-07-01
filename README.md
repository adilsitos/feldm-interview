# Feld M Tech Interview 

My submission for the tasks presented by feld m, which is a collection of python scripts that perform operations in a dummy database      

## Setup 

This project uses two external libraries: Pandas and Psycopg, both can be installed by running:
`
    pip install pandas
    pip install psycopg2
`

## Project structure

This project has the following files/structure:


| File              | Description     |
| --------------    | --------------- |
| `main.py`         | Main script that runs the first 4 proposed Tasks. |
| `dbunit.py`  | Definition of the `DBConnector` class which is used to perform operation in sqlite3  |
| `xmlutils.py`     | Definition of the `XMLUtils` class, which parses the provided `.xml` file.    |
| `tasks.py`        | Contains the function definitions for each of the first four Tasks.   |
| `utils.py`        | Contains helper functions, eg. create a csv, check an array, insert values in a new table, etc |
| `createbackup.py` | Read the Devices and Transactions table to create a csv as backup; 
| `setuppostgres.py` | Connect to a postgresql and perform task1 and task2 operations
| `docker-compose.yml` | Used to create a postgresql instance 
| `01-init.sh` | Script used when the container is created, creates table Devices and Transactions
| `transactions.db`        | SQLite database file.  |
| `eurofxref-hist-90d.xml`        | File containing provided currency exchange data.  |


For a better organization the task 5 is apart from the others

## How to run?

You just need to run the main file:

```
python main.py
```

This file will run the 4 first taks

## Task 5 

To execute task 5 is necessary to have docker installed in your computer. To create a postgres instance is just necessary to run:

```
docker-compose up
```

ps: A common problem is to already have a postgres instance running on port 5432, so it's probably necessary to kill its process

The file `createbackup.py` takes a snapshot from the original sqlite database `transactions.db`, and it is used to populate the postgres database.

```
python createbackup.py
```

To perform some operations on the postgres database just run the following command inside the folder `task5`:

```
python task5.py
```
