import pyodbc
import pytest

def set_up_connection():
    """Fixture to establish connection before a test is run"""
    server = '172.17.0.1\\SQLEXPRESS'
    database = 'AdventureWorks2012'
    username = 'NewAdminName'
    password = 'ABCDEFG!!!!3'
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + '; Port=60126; DATABASE=' + database + ';' \
        'UID=' + username + ';PWD=' + password)
    cursor = connection.cursor()
    return cursor


@pytest.mark.DQcheck
def test_modifieddate_unitmeasure():
    """
    TC#1 Check that ModifiedDate values are less than the current date
    Test Steps:
    1. Connect to AdventureWorks2012 DB
    2. Execute query to select future date records from UnitMeasure table
    3. Verify that the query result is empty
    Expected result:
    1. The result of query is 0.
    """
    connection = set_up_connection()
    query = """SELECT count(*) as 'Row count' FROM AdventureWorks2012.Production.UnitMeasure
    WHERE ModifiedDate >= getdate();"""
    result = connection.execute(query).fetchall()
    count_duplicates = result[0][0]
    assert count_duplicates == 0


@pytest.mark.DQcheck
def test_upper_case_unitmeasure():
    """
    TC#2 Check that UnitMeasureCode column values have UPPER-case format
    Test Steps:
    1. Connect to AdventureWorks2012 DB
    2. Execute query to select records from UnitMeasure table that have lower symbol(s)
    3. Verify that the query result is empty
    Expected result:
    1. The result of query is 0.
    """
    connection = set_up_connection()
    query = """SELECT count(*) AS 'Row count' FROM AdventureWorks2012.Production.UnitMeasure
    WHERE UPPER(UnitMeasureCode) COLLATE Latin1_General_CS_AS <> UnitMeasureCode;"""
    result = connection.execute(query).fetchall()
    count_lower_case = result[0][0]
    assert count_lower_case == 0


@pytest.mark.DQcheck
def test_documentlevel_document():
    """
    TC#3 Check that DocumentLevel column contains only 0, 1, 2 values
    Test Steps:
    1. Connect to AdventureWorks2012 DB
    2. Execute query to select records from Document table that contain value not in 0, 1, 2
    3. Verify that the query result is empty
    Expected result:
    1. The result of query is 0.
    """
    connection = set_up_connection()
    query = """SELECT count(*) AS 'Row count'
    FROM (SELECT DocumentNode, DocumentLevel FROM AdventureWorks2012.Production.Document 
    WHERE DocumentLevel NOT IN ('0', '1', '2')) a;"""
    result = connection.execute(query).fetchall()
    count_error_level = result[0][0]
    assert count_error_level == 0


@pytest.mark.DQcheck
def test_file_extension_document():
    """
    TC#4 Check that FileExtension values provided only to Document
    Test Steps:
    1. Connect to AdventureWorks2012 DB
    2. Execute query to select all records with document level
    and except all records with filled FileExtension
    3. Verify that the query result is empty
    Expected result:
    1. The result of query is 0.
    """
    connection = set_up_connection()
    query = """SELECT count(DocumentNode) AS 'Row count' from (
    SELECT DocumentNode FROM AdventureWorks2012.Production.Document WHERE FolderFlag = '0'
    EXCEPT
    SELECT DocumentNode FROM AdventureWorks2012.Production.Document WHERE FileExtension != ''
    UNION ALL
    SELECT DocumentNode FROM AdventureWorks2012.Production.Document WHERE FileExtension != ''
    EXCEPT 
    SELECT DocumentNode FROM AdventureWorks2012.Production.Document WHERE FolderFlag = '0') a;"""
    result = connection.execute(query).fetchall()
    count_folder = result[0][0]
    assert count_folder == 0


@pytest.mark.DQcheck
def test_blank_addressline_address():
    """
    TC#6 Check that AddressLine column doesn't contain blank values
    Test Steps:
    1. Connect to AdventureWorks2012 DB
    2. Execute query to select blank value in AddressLine column from Address table
    3. Verify that the query result is empty
    Expected result:
    1. The result of query is 0.
    """
    connection = set_up_connection()
    query = """SELECT count(*) as 'AddressID count' FROM AdventureWorks2012.Person.Address
    WHERE AddressLine1 IS NULL or AddressLine1 = '';"""
    result = connection.execute(query).fetchall()
    count_blank_address = result[0][0]
    assert count_blank_address == 0
