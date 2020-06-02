# Database validation automation

Python script to automate the database validation using sql query.

## How to run?

- Add configuration details in *parameters.py*

```python
# Source details
sql_server = <SERVER NAME>
database = <DATABASE NAME>
user_name = <USER NAME>
password = <PASSWORD>

# Input file
input_file = 'config/input.csv'
```
- Paste sql file in data folder (or some other location, mention that location in input.csv file)

- Add test cases in *input.csv* under config folder

```csv

TEST_CASE					SQL_FILE_PATH	SQL_FILE_NAME	INCLUDE
Employee age check			data/			employee		N
Invoice date check			data/			invoice.sql		Y
Order amount check			data/			orders			Y
```

- Execute ***db_validation.py***

## Details

- Added some dummy sql files, input file and output file

- In Input file, you can add 'N' to exclude the test case in INCLUDE column 

- Python script flag zero records in query result set as 'PASS' (Negative scenario)

- Output file will be stored in output folder with timestamp

