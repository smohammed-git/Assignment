#import libraries to handle request to api
import requests
import json
import pandas as pd

# Display all rows and columns of dataframe
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

EXCEL_FILE_PATH = r'C:\temp\Exchange_Data.xlsx'

# base currency or reference currency
BASE="USD"
# required currencies
OUT_CURR=["AUD","CAD","CHF","CNH","EUR","GBP","HKD","JPY","NZD","USD"]
# exchange data from a date
START_DATE="2022-11-03"
# exchange data till a date
END_DATE="2022-11-03"
# api url for request 
URL = 'https://api.exchangerate.host/timeseries?base={0}&start_date={1}&end_date={2}'.format(BASE,START_DATE,END_DATE)

def ProcessDataFromApi():    
    response = requests.get(URL)

    # retrive response in json format
    data = response.json()

    df1 = pd.DataFrame(OUT_CURR)
    df1.columns=["Currency_To"]

    # extract rates from each item of dictionary and append to list
    rates=[]
    for i,j in data["rates"].items():
        for out in OUT_CURR:
            rates.append([j[out]])
    df2 = pd.DataFrame(rates)
    df2.columns=["Currency_To_Value"]

    horizontal_stack = pd.concat([df1, df2], axis=1)

    df2 = pd.DataFrame(OUT_CURR)
    df2.columns=["Currency_To"]
    df2['Rate Type'],df2['Date'],df2['Currency_From'],df2['Currency_From_Value'] = ['Spot rate',START_DATE,BASE,1]

    merged_inner = pd.merge(left=df2, right=horizontal_stack)
    merged_inner = merged_inner.reindex(['Rate Type', 'Date', 'Currency_From', 'Currency_From_Value', 'Currency_To', 'Currency_To_Value'], axis=1)

    #export to excel
    merged_inner.to_excel(EXCEL_FILE_PATH, index = False)

if __name__ == "__main__":
    ProcessDataFromApi()       

