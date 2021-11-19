import pandas as pd 




def features():
    data = pd.read_csv('final_data.csv')
    cols = list(data.columns)
    cols= cols[2:]
    return cols

