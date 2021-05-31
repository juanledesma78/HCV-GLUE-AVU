import sys, os, re
import pandas as pd
from openpyxl import load_workbook
#once I know the fixed paths to the data, update this. 
molis_file = sys.argv[1] #c:/Users/juan.ledesma/Desktop/HCV_GLUE_AVU/tabular/made-up_MolisData_test.xlsx 
seq_files = sys.argv[2] #"c:/Users/juan.ledesma/Desktop/HCV_GLUE_AVU/sources/NGS91
NGSrun = os.listdir(seq_files)

df = {"HCVGEN",	"SAMPLE_DT"	RECEPT_DT	CORORDNB	ORDPATBIRTHDT}
sequences = []
for seq in NGSrun:
    seq=seq.replace(".fas","")
    sequences.append(seq)
print(sequences)

df = {}

molis_data = pd.read_excel(molis_file)
#print(molis_data.dtypes[molis_data.dtypes == "datetime64[ns]"])
datatypes = molis_data.dtypes.to_dict() # create a dictionary, col names are the keys and datatype the value
#SAMPLE_DT        datetime64[ns]
#rename the date to fit in GLUE 
for col, typ in datatypes.items():
    if (typ == "datetime64[ns]"):
        molis_data[col] = molis_data[col].dt.strftime('%d-%b-%Y') 

molis_data["LPERIOD"]=molis_data["LPERIOD"].apply('{:0>4}'.format) # 4 digit code
molis_data["ORDNB"]=molis_data["ORDNB"].apply('{:0>4}'.format) # 4 digit code

molis_data["MOLIS"]=molis_data["LID"].astype(str) + molis_data["LPERIOD"].astype(str) + molis_data["ORDNB"].astype(str)
#molis_data["sequenceID"]=""
#print(molis_data)

#GlueMolis=molis_data[["MOLIS","LID","LPERIOD","ORDNB","HCVGEN","SAMPLE_DT","RECEPT_DT","CORORDNB","ORDPATBIRTHDT","ORDPATSX"]]

#output_name= input_file.replace(".xlsx",".csv")
#GlueMolis.to_csv(output_name, index=False)
for seqid in sequences:
    for m in molis_data["MOLIS"]:
        if m in seqid:
            molis_data.loc[molis_data["MOLIS"]==str(m), "sequenceID"] = seqid
            
        
    #print(m, seqid)
molis_data = molis_data.dropna(subset = ["sequenceID"])
print(molis_data)

#df.loc[df['c1'] == 'Value', 'c2'] = 10
# It doesnt work for repeats 