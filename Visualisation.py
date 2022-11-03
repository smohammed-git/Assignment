import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Display all rows and columns of dataframe
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Setup variables
CSV_FILE_PATH = r'C:\Howden_CompanyXYZ_2021_Data.xlsx'

def procss_data():
    # Read first sheet data
    df1 = pd.read_excel(CSV_FILE_PATH,
                       sheet_name='GL-np',
                       skiprows = 4,
                       usecols = "A:S",
                       engine='openpyxl')

    # drop unwanted columns
    df_GL = df1.drop(df1.iloc[:, 1:15],axis = 1).iloc[0:12]
    print(df_GL)

    x = df_GL['U/W year']
    y1 = df_GL['Paid losses']
    y2 = df_GL['Case reserves']
    y3 = df_GL['IBNR']
    y4 = df_GL['Earned premium']

    fig = create_plot(x, y1, y2, y3, y4)
    plt.show()

def create_plot(x, y1, y2, y3, y4):

    fig = plt.figure()
    ax1 = fig.gca()
    ax2 = ax1.twinx()

    plt.title("Ultimate loss ratio")

    bar1 = ax1.bar(x, y1, width=0.3, color='mediumblue', label = 'Paid losses')
    bar2 = ax1.bar(x, y2, bottom=y1, width=0.3, color='limegreen', label = 'Case reserves')
    bar3 = ax1.bar(x, y3, bottom=y1+y2, width=0.3, color='green', label = 'IBNR')
    line1 = ax2.plot(x, y4, marker='o', color='cornflowerblue', label = 'Earned premium')    

    ax1.set_xlabel('U/W year')
    ax1.set_ylabel('Ultimate loss ratio split')
    ax2.set_ylabel('Earned premium')


    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    ax1.set_ylim(0.0, 1.40)
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
    ax2.set_ylim(0, 1200)
    
    return fig

if __name__ == "__main__":
    procss_data()    
