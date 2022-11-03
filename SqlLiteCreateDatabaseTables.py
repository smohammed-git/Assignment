import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"C:\sqlite\db\ClaimDevelopment.db"

    sql_create_FactStatistical_table = """ CREATE TABLE IF NOT EXISTS FactStatistical (
                                        Id integer PRIMARY KEY,
                                        CompanyName text,
                                        LineOfBusiness text,
                                        Currency text,
                                        Year integer,
                                        LossIncurredRatio real,
                                        DevelopmentMonth integer,
                                        DWCreatedDate,
                                        DWCreatedBy
                                    ); """

    sql_create_FactData_table = """CREATE TABLE IF NOT EXISTS FactData (
                                    Id integer PRIMARY KEY,
                                    LineOfBusiness text,
                                    Year integer,
                                    GrossWrittenPremium integer,
                                    EarnedPremium integer,
                                    PaidLosses integer,
                                    CaseReserves integer,
                                    IBNR integer,
                                    UltimateLossRatio integer,
                                    DWCreatedDate text,
                                    DWCreatedBy text
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_FactStatistical_table)

        # create tasks table
        create_table(conn, sql_create_FactData_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
