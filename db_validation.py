#!/usr/bin/env python
# coding: utf-8

# Import the libraries

import pandas as pd
import datetime
import pyodbc
import parameters as p

# Library version

# print(f'Pandas version - {pd.__version__}')

# display options

pd.options.display.float_format = '{:.3f}'.format
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# Constant

DRIVER_NAME = 'ODBC Driver 17 for SQL Server'

# Functions


def db_conn(server, db, user, pwd):
    ''' Returns the ODBC connection.

        Input arguments:
            server = MS SQL Server
            db = Database Name
            user = User Name
            pwd = password
        Output:
            ODBC connection'''
    try:
        conn = pyodbc.connect(f''' DRIVER={{{DRIVER_NAME}}};
                                   SERVER={server};DATABASE={db};
                                   UID={user};PWD={pwd}''')
                                   
        print(f'Database - ({db}) on Server - ({server}) is connected with the user - ({user}) successfully.')
        return conn
    except Exception as e:
        print(f'Database connection is not successful due to {e}')


def sql_execution(file_path, conn):
    ''' Returns query result set row count.

        Input arguments:
            file path = SQL file path
            conn = ODBC connection.
        Output:
            Row count (int)'''
    try:
        with open(file_path, 'r') as f:
            sql_query = f.read().lower()
            print(f'SQL file - {file_path} read successfully.')
            sql_result_df = pd.read_sql(sql_query, conn)
            return sql_result_df.shape[0]
    except Exception as e:
        print(e)
        return (e)


def db_conn_close(conn):
    ''' Close the existing ODBC connection. '''
    try:
        conn.close()
        print('Database connection is closed')
    except Exception as e:
        print(f'Connection is already closed - {e}')


# Create the connection

s_conn = db_conn(p.sql_server, p.database, p.user_name, p.password)

# Read input file, Get the result, Write to output file

if s_conn is not None:
    try:
        input_df = pd.read_csv(p.input_file)
        test_case_df = input_df[input_df['INCLUDE'].str.lower() == 'y'].copy()
        test_case_df['SQL_FILE_NAME'] = test_case_df['SQL_FILE_NAME'].apply(
                                        lambda x: f'{x}.sql' if '.sql' not in x else x)
        test_case_df['SQL_FILE'] = test_case_df['SQL_FILE_PATH'] + test_case_df['SQL_FILE_NAME']
        test_case_df['SQL_RESULT_ROW_COUNT'] = test_case_df['SQL_FILE'].apply(sql_execution, args=(s_conn,))
        test_case_df['TEST_RESULT'] = test_case_df['SQL_RESULT_ROW_COUNT'].apply(lambda x: 'PASS' if x == 0 else 'FAIL')
        output_file_name = f'output/DB_Validation_Test_Result_{datetime.datetime.now().strftime("%d%m%Y_%H%M%S")}.csv'

        test_case_df.to_csv(output_file_name, index=False)
        print(f'Test results are stored in - {output_file_name}')
    except Exception as e:
        print(f'Test case script execution is failed, Due to - {e}')

db_conn_close(s_conn)
