import sys, os, re, subprocess
import pandas as pd
#from openpyxl import load_workbook
#once I know the fixed paths to the data, update this. 
molis_file = sys.argv[1] #c:/Users/juan.ledesma/Desktop/HCV_GLUE_AVU/tabular/made-up_MolisData_test.csv 
sources_run = sys.argv[2] #"c:/Users/juan.ledesma/Desktop/HCV_GLUE_AVU/sources/NGS91

SourcesNGSid = re.search(r'NGS[0-9]*.*[^/]',sources_run)
SourcesNGSid = SourcesNGSid.group() # this for calling GLUE NGS94_(repeat_Miseq_NGS93) 
NGSid = re.search(r'NGS[0-9]*',SourcesNGSid)
NGSid = NGSid.group() # this for csv NGS94

path_to_tabular = re.sub(r'sources/NGS.*','tabular/',sources_run) # create .../HCV_GLUE_AVU/tabular

NGSsequences = os.listdir(sources_run)
sequences = []
molis_id = []
for seq in NGSsequences:
    seq = seq.replace(".fas","")
    mol = re.sub(r'-[0-9].*',"", seq)
    sequences.append(seq)
    molis_id.append(mol)
run = {"sequenceID" : sequences, "MOLIS" : molis_id}
ngs_run = pd.DataFrame(data=run) # table with sequenceID and molis to check 

molis_data = pd.read_csv(molis_file) #print(molis_data.dtypes[molis_data.dtypes == "datetime64[ns]"]) before was datatime now is object
molis_data["SAMPLE_DT"]= pd.to_datetime(molis_data["SAMPLE_DT"])
molis_data["RECEPT_DT"]= pd.to_datetime(molis_data["RECEPT_DT"])
molis_data["ORDPATBIRTHDT"]= pd.to_datetime(molis_data["ORDPATBIRTHDT"])
#molis_data["RECEPT_DT"] = molis_data["RECEPT_DT"].dt.strftime('%d-%b-%Y')
datatypes = molis_data.dtypes.to_dict() # create a dictionary, colnames are the keys and datatype the value
#SAMPLE_DT        datetime64[ns]
#change data format to fit GLUE
for col, typ in datatypes.items():
    if (typ == "datetime64[ns]"):
        molis_data[col] = molis_data[col].dt.strftime('%d-%b-%Y') 


molis_data["ORDPATSX"] = molis_data["ORDPATSX"].replace({'F': 'Female', 'M': 'Male', 'O': 'Other', 'U': 'Unknown'})

# consolidate LPERIOD, ORDNB, MOLIS to give molis number
molis_data["LPERIOD"] = molis_data["LPERIOD"].apply('{:0>4}'.format) # 4 digit code
molis_data["ORDNB"] = molis_data["ORDNB"].apply('{:0>4}'.format) # 4 digit code
molis_data["MOLIS"] = molis_data["LID"].astype(str) + molis_data["LPERIOD"].astype(str) + molis_data["ORDNB"].astype(str)

# match the sequence name (molis numbers) with the molis number from the initial table to filter the run info
for seqid in ngs_run["sequenceID"]:
    for m in molis_data["MOLIS"]:
        if m in seqid:
            sequenceId_molis_info = pd.merge(ngs_run, molis_data, on="MOLIS")

# fill empty fields to avoid problems with GLUE

sample_list= path_to_tabular + "/table_sample/" + "metadata_table_SAMPLE_" + NGSid + ".csv"
patient_list= path_to_tabular + "/table_patient/" +  "metadata_table_PATIENT_" + NGSid + ".csv"

sequenceId_molis_info[["MOLIS","LID","LPERIOD","ORDNB","HCVGEN","SAMPLE_DT","RECEPT_DT","pid","NHS", "REFEXT"]].drop_duplicates("MOLIS").to_csv(sample_list, index=False)
sequenceId_molis_info[["pid","NHS", "ORDPATBIRTHDT","ORDPATSX"]].drop_duplicates("pid").to_csv(patient_list, index=False)




