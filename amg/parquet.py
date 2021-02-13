import pandas as pd
import pyarrow  

filename = r'data/hashed.xlsx'
index_column = 'hashed_id'

data_frame = pd.read_excel(filename, index_col='hashed_id')

data_frame = data_frame.sort_index()

