import sys
input_file = sys.argv[1] #excel

import pandas as pd
from openpyxl import load_workbook
molis_data = pd.read_excel(input_file)
#print(molis_data.dtypes[molis_data.dtypes == "datetime64[ns]"])
datatypes = molis_data.dtypes.to_dict() # create a dictionary, col names are the keys and datatype the value
#SAMPLE_DT        datetime64[ns]
#rename the date to fit in GLUE 
for col, typ in datatypes.items():
    if (typ == "datetime64[ns]"):
        molis_data[col] = molis_data[col].dt.strftime('%d-%b-%Y') 

molis_data["LPERIOD"]=molis_data["LPERIOD"].apply('{:0>4}'.format) # 4 digit code
molis_data["ORDNB"]=molis_data["ORDNB"].apply('{:0>4}'.format) # 4 digit code

molis_data["MOLIS"]=molis_data["LID"].astype(str)+molis_data["LPERIOD"].astype(str)+molis_data["ORDNB"].astype(str)

GlueMolis=molis_data[["MOLIS","LID","LPERIOD","ORDNB","HCVGEN","SAMPLE_DT","RECEPT_DT","CORORDNB","ORDPATBIRTHDT","ORDPATSX"]]

output_name= input_file.replace(".xlsx",".csv")
GlueMolis.to_csv(output_name, index=False)



