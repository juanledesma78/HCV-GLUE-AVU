import sqlite3
import os
import re
import subprocess
import argparse
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

#sources_run = sys.argv[1] #"..sources/NGS91 ...
specs = argparse.ArgumentParser(
    prog='populate_metadata_from_molis.py', 
    usage='%(prog)s --sources/-s path-to-sources-NGSrun', 
    description='populate information from molis database to glue porject')
specs.add_argument('--sources','-s', required=True, help=' path to the folder in sources/ that contains the fasta sequences which data is going to be transferred')
sources_run =specs.parse_args()
# Namespace(sources='../sources/NGS91')

sources_ngs_id = re.search(r'NGS[0-9]*.*[^/]',sources_run.sources)
sources_ngs_id = sources_ngs_id.group() # this for calling GLUE NGS94_(repeat_Miseq_NGS93) 
ngs_id = re.search(r'NGS[0-9]*',sources_ngs_id)
ngs_id = ngs_id.group() # this for csv NGS94

""" Create a table with sequenceID and molis to check against synthetic_molis.db """
ngs_sequences = os.listdir(sources_run.sources)
sequences = []
molis_id = []
pipeline = []
version = []
for seq in ngs_sequences:
    seq = seq.replace(".fas","")
    mol = re.sub(r'-[0-9].*',"", seq)
    sequences.append(seq)
    molis_id.append(mol)

    if "genomancer" in seq:
        pipeline.append("Genomacer")
        version.append("v.1")
    else:
        pipeline.append("PHE HCV bioinformatics pipeline")
        version.append("version 1.0")

run = {"sequenceID" : sequences, "MOLIS" : molis_id, "Pipeline": pipeline, "Version": version}
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
sequence_id_molis_info = ngs_run.merge(molis_data, on='MOLIS')

path_to_tabular = "/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/tabular/"
sample_list= os.path.join(path_to_tabular,"table_sample","metadata_table_SAMPLE_" + ngs_id + ".csv") # each comma add a slash /
patient_list= os.path.join(path_to_tabular ,"table_patient","metadata_table_PATIENT_" + ngs_id + ".csv")
sequence_list = os.path.join(path_to_tabular +"table_sequence", "metadata_table_SEQUENCE_"+ ngs_id +".csv")


#sequenceId_molis_info[["MOLIS","LID","LPERIOD","ORDNB","HCVGEN","SAMPLE_DT","RECEPT_DT","pid","NHS", "CORORDNB","REFEXT"]].drop_duplicates("MOLIS").to_csv(sample_list, index=False)
# the id for the patient can be NHS, patientid or anyother id according to what I was told. Molis Housekeeping
sequence_id_molis_info[["MOLIS","LID","LPERIOD","ORDNB","HCVGEN","SAMPLE_DT","RECEPT_DT","ORDPATIDNB", "CORORDNB","REFEXT"]].drop_duplicates("MOLIS").to_csv(sample_list, index=False)
sequence_id_molis_info[["ORDPATIDNB", "ORDPATBIRTHDT","ORDPATSX"]].drop_duplicates("ORDPATIDNB").to_csv(patient_list, index=False)
sequence_id_molis_info[["sequenceID","MOLIS","Pipeline","Version","ORDPATIDNB"]].to_csv(sequence_list, index=False) # ORDPATIDNB added here in case shcema needs to be changed 

# CALL GLUE TO IMPORT THIS TABLES AND SEQUENCE TABLE
# update the name run in javascripts to allow the data population

new_ngs_run_patient = ""
with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/populatePatientTable.js",'r') as script:
        text = script.read()
        new_ngs_run_patient = re.sub(r'metadata_table_PATIENT_[a-zA-Z0-9]*.csv','metadata_table_PATIENT_'+ ngs_id + '.csv', text)
        script.close()
with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/populatePatientTable.js",'w') as script:
    script.write(new_ngs_run_patient)
    script.close()

new_ngs_run_sample = ""
with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/populateSampleTable.js",'r') as script: 
        text = script.read()
        new_ngs_run_sample = re.sub(r'metadata_table_SAMPLE_[a-zA-Z0-9]*.csv','metadata_table_SAMPLE_'+ ngs_id + '.csv', text)
        script.close()
with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/populateSampleTable.js",'w') as script:
    script.write(new_ngs_run_sample)
    script.close()


glue_commands = """ 
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
glue_commands = glue_commands.replace("NGSsource", sources_ngs_id) #NGSid)
glue_commands = glue_commands.replace("RUNID", ngs_id) 
p1 = subprocess.run("gluetools.sh" , text=True, input=glue_commands)
if p1.returncode == 0:
    print("\nMetadata successfully uploaded in GLUE\n")
else:
    print("\nSomething went wrong")

