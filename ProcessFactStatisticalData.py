import pandas as pd
import sqlite3
from datetime import datetime

# Display all rows and columns of dataframe
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Setup variables
DB_FILE_PATH = r'C:\sqlite\db\ClaimDevelopment.db'
CSV_FILE_PATH = r'C:\Howden_CompanyXYZ_2021_Data.xlsx'


def connect_to_db(db_file):
    """
    Connect to an SQlite database
    :param db_file: absolute or relative path of db file
    :return: sqlite3 connection
    """
    sqlite3_conn = None

    try:
        sqlite3_conn = sqlite3.connect(db_file)
        return sqlite3_conn

    except Error as err:
        print(err)

        if sqlite3_conn is not None:
            sqlite3_conn.close()


def procss_data():
    # Read first sheet data
    df1 = pd.read_excel(CSV_FILE_PATH,
                       sheet_name='GL-np',
                       skiprows = 4,
                       usecols = "A:N",
                       engine='openpyxl')

    #Read second sheet data
    df2 = pd.read_excel(CSV_FILE_PATH,
                       sheet_name='MA-np',
                       skiprows = 4,
                       usecols = "A:N",
                       engine='openpyxl')    

    df_GL = df1.iloc[0:12]
    df_GL = df_GL.assign(LineOfBusiness = 'GL-np')
    df_MA = df2.iloc[0:12]
    df_MA = df_MA.assign(LineOfBusiness = 'MA-np')  
    df_merged = df_GL.append(df_MA, ignore_index=True)

    df_merged = pd.melt(df_merged,['U/W year','Gross written premium','LineOfBusiness'],var_name='DevelopmentMonth',value_name='LossIncurredRatio')
    df_merged = df_merged.rename(columns={'U/W year': 'Year'})
    df_merged.drop('Gross written premium', axis=1, inplace=True)
    df_merged['CompanyName'], df_merged['Currency'], df_merged['DWCreatedDate'], df_merged['DWCreatedBy'] = ['Howden', 'EUR', datetime.today().strftime('%Y-%m-%d'), 'admin']

    print(df_merged)

    #Initialise the connection
    conn = connect_to_db(DB_FILE_PATH)
    if conn is not None:
        df_merged.to_sql('FactStatistical', conn, if_exists='append', index=False)
        conn.close()
    else:
        print('Connection to database failed')

if __name__ == "__main__":
    procss_data()    
