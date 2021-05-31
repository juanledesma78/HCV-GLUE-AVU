import sys, os, re
import pandas as pd
from openpyxl import load_workbook
#once I know the fixed paths to the data, update this. 
molis_file = sys.argv[1] #c:/Users/juan.ledesma/Desktop/HCV_GLUE_AVU/tabular/made-up_MolisData_test.xlsx 
seq_files = sys.argv[2] #"c:/Users/juan.ledesma/Desktop/HCV_GLUE_AVU/sources/NGS91
NGSrun = os.listdir(seq_files)
sequences = []
molis_id = []
for seq in NGSrun:
    seq = seq.replace(".fas","")
    mol = re.sub(r'-[0-9].*',"", seq)
    sequences.append(seq)
    molis_id.append(mol)
run = {"sequenceID" : sequences, "MOLIS" : molis_id}
ngs_run = pd.DataFrame(data=run)

molis_data = pd.read_excel(molis_file) #print(molis_data.dtypes[molis_data.dtypes == "datetime64[ns]"])
datatypes = molis_data.dtypes.to_dict() # create a dictionary, colnames are the keys and datatype the value
#SAMPLE_DT        datetime64[ns]
#change data format to fit GLUE
for col, typ in datatypes.items():
    if (typ == "datetime64[ns]"):
        molis_data[col] = molis_data[col].dt.strftime('%d-%b-%Y') 

# consolidate LPERIOD, ORDNB, MOLIS to give molis number
molis_data["LPERIOD"]=molis_data["LPERIOD"].apply('{:0>4}'.format) # 4 digit code
molis_data["ORDNB"]=molis_data["ORDNB"].apply('{:0>4}'.format) # 4 digit code
molis_data["MOLIS"]=molis_data["LID"].astype(str) + molis_data["LPERIOD"].astype(str) + molis_data["ORDNB"].astype(str)

# match the sequence name (molis numbers) with the molis number in the samplesheet excel to filter the run info
for seqid in ngs_run["sequenceID"]:
    for m in molis_data["MOLIS"]:
        if m in seqid:
            sequenceId_molis_info = pd.merge(ngs_run, molis_data, on="MOLIS")

seq_files = re.sub(r'/',"",seq_files)
metadata_name = re.sub(r'.*sources',"",seq_files)
molis_list= molis_file.replace(".xlsx","_MOLIS_" + metadata_name + ".csv")
sample_list= molis_file.replace(".xlsx","_SAMPLES_" + metadata_name + ".csv")
patient_list= molis_file.replace(".xlsx","_PATIENTS_" + metadata_name + ".csv")
#hospital_list= molis_file.replace(".xlsx","_HospitalList_" + metadata_name + ".csv")
#sequenceId_molis_info[["sequenceID","MOLIS","LID","LPERIOD","ORDNB","HCVGEN","SAMPLE_DT","RECEPT_DT","CORORDNB","ORDPATBIRTHDT","ORDPATSX"]].to_csv(output_name, index=False)
sequenceId_molis_info[["sequenceID","MOLIS","NHS","CORORDNB"]].to_csv(molis_list, index=False)
sequenceId_molis_info[["MOLIS","LID","LPERIOD","ORDNB","HCVGEN","SAMPLE_DT","RECEPT_DT","NHS", "REFEXT"]].drop_duplicates("MOLIS").to_csv(sample_list, index=False)
sequenceId_molis_info[["NHS", "ORDPATBIRTHDT","ORDPATSX"]].drop_duplicates("NHS").to_csv(patient_list, index=False)
#sequenceId_molis_info[["CORORDNB","NHS","REFEXT" ]].drop_duplicates("CORORDNB").to_csv(hospital_list, index=False) # list of hospital shoudl be fixed
#sequenceId_molis_info[["REFEXT","CORORDNB", ]].drop_duplicates("CORORDNB").to_csv(hospital_list, index=False)

