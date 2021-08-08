import sqlite3
import sys, os, re, subprocess
import pandas as pd

conn = sqlite3.connect("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/tabular/molis.db")

molis_data = pd.read_sql_query('''
SELECT STAT_ORD.LID || printf('%04d',STAT_ORD.LPERIOD) || printf('%04d',STAT_ORD.ORDNB)  AS MOLIS, STAT_ORD.LID, STAT_ORD.LPERIOD, STAT_ORD.ORDNB,
IIF(MC='HCVGEN',RES_TXT,'') AS HCVGEN,
--IIF(MC='MAT',RES_TXT,'') AS XX,
STAT_ORD.SAMPLE_DT, STAT_ORD.RECEPT_DT, STAT_ORD.CORORDNB, STAT_ORD.HOSP_FL, 
STAT_ORD.ORDPATNAME, STAT_ORD.ORDPATBIRTHDT, STAT_ORD.ORDPATSX, STAT_ORD.ORDPATIDNB, 
STAT_ORD.CORORDSUBNB, STAT_ORD.REFEXT, STAT_ORD.EXTPATIDNB, STAT_ORD.REC_SITE_NB 

FROM 
(
(STAT_ORD INNER JOIN STAT_ORDANAEL ON (STAT_ORD.ORDNB = STAT_ORDANAEL.ORDNB) AND (STAT_ORD.LPERIOD = STAT_ORDANAEL.LPERIOD) AND (STAT_ORD.LID = STAT_ORDANAEL.LID))
INNER JOIN STAT_COR ON STAT_ORD.CORORDNB = STAT_COR.CORNB)

INNER JOIN STAT_SAMPLEPOS_CONT_V ON (STAT_ORDANAEL.ORDNB = STAT_SAMPLEPOS_CONT_V.ORDNB) 
AND (STAT_ORDANAEL.LPERIOD = STAT_SAMPLEPOS_CONT_V.LPERIOD) AND (STAT_ORDANAEL.LID = STAT_SAMPLEPOS_CONT_V.LID) 

GROUP BY STAT_ORDANAEL.LID, STAT_ORDANAEL.LPERIOD, STAT_ORDANAEL.ORDNB, STAT_ORD.LID || printf('%04d',STAT_ORD.LPERIOD) || printf('%04d',STAT_ORD.ORDNB), 
STAT_ORD.SAMPLE_DT, STAT_ORD.RECEPT_DT, STAT_ORD.CORORDNB, STAT_ORD.HOSP_FL, STAT_ORD.ORDPATNAME, STAT_ORD.ORDPATBIRTHDT, 
STAT_ORD.ORDPATSX, STAT_ORD.ORDPATIDNB, STAT_ORD.CORORDSUBNB, STAT_ORD.REFEXT, STAT_ORD.EXTPATIDNB, STAT_ORD.REC_SITE_NB

HAVING STAT_ORD.REC_SITE_NB IN ("SHC", "SHE")
;
''', conn)

sources_run = sys.argv[1] #"..sources/NGS91 ...

SourcesNGSid = re.search(r'NGS[0-9]*.*[^/]',sources_run)
SourcesNGSid = SourcesNGSid.group() # this for calling GLUE NGS94_(repeat_Miseq_NGS93) 
NGSid = re.search(r'NGS[0-9]*',SourcesNGSid)
NGSid = NGSid.group() # this for csv NGS94

""" Create a table with sequenceID and molis to check against synthetic_molis.db """
NGSsequences = os.listdir(sources_run)
sequences = []
molis_id = []
Pipeline = []
Version = []
for seq in NGSsequences:
    seq = seq.replace(".fas","")
    mol = re.sub(r'-[0-9].*',"", seq)
    sequences.append(seq)
    molis_id.append(mol)

    if "genomancer" in seq:
        Pipeline.append("Genomacer")
        Version.append("v.1")
    else:
        Pipeline.append("PHE HCV bioinformatics pipeline")
        Version.append("version 1.0")

run = {"sequenceID" : sequences, "MOLIS" : molis_id, "Pipeline": Pipeline, "Version": Version}
ngs_run = pd.DataFrame(data=run) 


""" Reformat data from molis according to GLUE: DD-MMM-YYYY, gender... """
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


"""match the sequenceID (or molis numbers) with the molis number from the database to filter the run info""" 
#sequenceId_molis_info = ngs_run.merge(molis_data, how='left', left_on='MOLIS', right_on='MOLIS')
sequenceId_molis_info = ngs_run.merge(molis_data, on='MOLIS')

path_to_tabular = "/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/tabular/"
sample_list= path_to_tabular + "table_sample/" + "metadata_table_SAMPLE_" + NGSid + ".csv"
patient_list= path_to_tabular + "table_patient/" +  "metadata_table_PATIENT_" + NGSid + ".csv"
sequence_list = path_to_tabular +"table_sequence/"+ "metadata_table_SEQUENCE_"+ NGSid +".csv"
#sequenceId_molis_info[["MOLIS","LID","LPERIOD","ORDNB","HCVGEN","SAMPLE_DT","RECEPT_DT","pid","NHS", "CORORDNB","REFEXT"]].drop_duplicates("MOLIS").to_csv(sample_list, index=False)
# the id for the patient can be NHS, patientid or anyother id according to what I was told. Molis Housekeeping
sequenceId_molis_info[["MOLIS","LID","LPERIOD","ORDNB","HCVGEN","SAMPLE_DT","RECEPT_DT","ORDPATIDNB", "CORORDNB","REFEXT"]].drop_duplicates("MOLIS").to_csv(sample_list, index=False)
sequenceId_molis_info[["ORDPATIDNB", "ORDPATBIRTHDT","ORDPATSX"]].drop_duplicates("ORDPATIDNB").to_csv(patient_list, index=False)
sequenceId_molis_info[["sequenceID","MOLIS","Pipeline","Version","ORDPATIDNB"]].to_csv(sequence_list, index=False) # ORDPATIDNB added here in case shcema needs to be changed 

# CALL GLUE TO IMPORT THIS TABLES AND SEQUENCE TABLE
# update the name run in javascripts to allow the data population

new_NGS_run_PATIENT = ""
with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/populatePatientTable.js",'r') as script:
        text = script.read()
        new_NGS_run_PATIENT = re.sub(r'metadata_table_PATIENT_[a-zA-Z0-9]*.csv','metadata_table_PATIENT_'+ NGSid + '.csv', text)
        script.close()
with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/populatePatientTable.js",'w') as script:
    script.write(new_NGS_run_PATIENT)
    script.close()

new_NGS_run_SAMPLE = ""
with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/populateSampleTable.js",'r') as script: # THIS IS NOT THE FINAL PATH AS IT DEPENDS ON WHERE GLUE IS GOING TO BE INSTALLED
        text = script.read()
        new_NGS_run_SAMPLE = re.sub(r'metadata_table_SAMPLE_[a-zA-Z0-9]*.csv','metadata_table_SAMPLE_'+ NGSid + '.csv', text)
        script.close()
with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/populateSampleTable.js",'w') as script:
    script.write(new_NGS_run_SAMPLE)
    script.close()


Glue_commands = """ 
project hcv_glue_avu
run script glue/populatePatientTable.js
run script glue/populateSampleTable.js
module NGSSequenceDataPopulator populate --whereClause "source.name='NGSsource'" --fileName tabular/table_sequence/metadata_table_SEQUENCE_RUNID.csv
Q
exit
quit
\
"""
#project hcv_glue_avu\nimport source sources/NGS93\nQ\nexit\n'
Glue_commands = Glue_commands.replace("NGSsource", SourcesNGSid) #NGSid)
Glue_commands = Glue_commands.replace("RUNID", NGSid) 
p1 = subprocess.run("gluetools.sh" , text=True, input=Glue_commands)
if p1.returncode == 0:
    print("\nMetadata successfully uploaded in GLUE\n")
else:
    print("\nSomething went wrong")
