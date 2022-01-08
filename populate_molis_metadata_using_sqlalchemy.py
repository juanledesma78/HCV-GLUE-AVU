import sqlite3
import os
import re
import argparse
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import update
from sqlalchemy.orm import declarative_base, sessionmaker
from database_model.hcv_glue_avu_sqla_model import Hospital, Patient, Sample, Sequence


specs = argparse.ArgumentParser(
    prog='populate_metadata_from_molis.py', 
    usage='%(prog)s --sources/-s <path to the specific NGS run in directory sources>', 
    description='populate information from MOLIS database to glue project')
specs.add_argument('--sources','-s', required=True, help=' path to the folder in sources/ that contains the fasta sequences which data is going to be transferred')
sources_run =specs.parse_args() # Namespace(sources='../sources/NGS91')
ngs_id = re.search(r'NGS[0-9]*',sources_run.sources)
ngs_id = ngs_id.group() # this used for the report/csv/txt


""" ACCESS TO TESTING MOLIS DATABASE"""
path_to_project = os.getcwd() #/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu
path_to_testing_molis_db = os.path.join(path_to_project,"tabular/molis.db")

conn = sqlite3.connect(path_to_testing_molis_db)
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


""" MODIFICATIONS FOR DATA TO WORK ON MYSQL AND CREATION OF DATAFRANES FOR THE DATA POPULATION """

molis_data["SAMPLE_DT"]= pd.to_datetime(molis_data["SAMPLE_DT"]).dt.strftime('%Y-%m-%d')
molis_data["RECEPT_DT"]= pd.to_datetime(molis_data["RECEPT_DT"]).dt.strftime('%Y-%m-%d')
molis_data["ORDPATBIRTHDT"]= pd.to_datetime(molis_data["ORDPATBIRTHDT"]).dt.strftime('%Y-%m-%d')
molis_data["ORDPATSX"] = molis_data["ORDPATSX"].replace({'F': 'Female', 'M': 'Male', 'O': 'Other', 'U': 'Unknown'})

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

current_run = {"sequenceID" : sequences, "sample_id" : molis_id, "Pipeline": pipeline, "Version": version}
sequence_df = pd.DataFrame(data=current_run) 
combined_sequence_molis_df = sequence_df.merge(molis_data, how='left', left_on='sample_id', right_on='MOLIS') # matching the sequenceID with the molis number 
combined_sequence_molis_df = combined_sequence_molis_df.dropna(subset = ["MOLIS"]) # dropping PC
sample_df = combined_sequence_molis_df[["MOLIS","LID","LPERIOD","ORDNB","HCVGEN",
                                        "SAMPLE_DT","RECEPT_DT","ORDPATIDNB", "CORORDNB","REFEXT"]].drop_duplicates("MOLIS")
patient_df = combined_sequence_molis_df[["ORDPATIDNB", "ORDPATBIRTHDT","ORDPATSX"]].drop_duplicates("ORDPATIDNB")

""" ACCESS TO GLUE MYSQL DATABASE"""

engine = create_engine('mysql+pymysql://gluetools:glue12345@localhost/GLUE_TOOLS', echo=True, future=True)  
Session = sessionmaker(bind=engine)
session = Session() 
Base = declarative_base()


""" DATA POPULATION. The population must start using the parent tables before populating the children tables 
as the latter are dependent on the formers becuase of the constraints. Otherwise this error is returned:
sqlalchemy.exc.IntegrityError: (pymysql.err.IntegrityError) (1452, 'Cannot add or update a child row: a foreign key constraint fails"""

""" HOSPITAL DATA POPULATION"""

glue_hospital_codes = [hospital.id for hospital in session.query(Hospital)]
hospital_df = pd.read_csv(os.path.join(path_to_project,'tabular/hospital_list.csv')) # Hospital list is fixed
hospital_df = hospital_df.replace({np.nan: None }) # to fix sqlalchemy.exc.ProgrammingError: (pymysql.err.ProgrammingError) nan can not be used with MySQL

duplicated_hospital_records= ""
new_hospital_records= ""
for hidx in hospital_df.iloc:
    if hidx.CORNB in glue_hospital_codes:
        duplicated_hospital_records +=  str(hidx.CORNB_FULLNAME) + '\n'
    else:
        session.add(Hospital(id = hidx.CORNB, name = hidx.CORNB_FULLNAME))
        new_hospital_records += str(hidx.CORNB_FULLNAME) + '\n' 


""" PATIENT DATA POPULATION"""

patient_list = [patient.id for patient in session.query(Patient)]
patient_df = patient_df.replace({np.nan: None })

duplicated_patients= ""
new_patients= ""
for pidx in patient_df.iloc:
    if pidx.ORDPATIDNB in patient_list:
        duplicated_patients += str(pidx.ORDPATIDNB) + '\n' 
    else:
        session.add(Patient(id = pidx.ORDPATIDNB, date_of_birth = pidx.ORDPATBIRTHDT, gender = pidx.ORDPATSX))
        new_patients += str(pidx.ORDPATIDNB) + '\n' 

""" SAMPLE DATA POPULATION"""

sample_list = [sample.id for sample in session.query(Sample)]
sample_df = sample_df.replace({np.nan: None })

duplicated_samples= ""
new_samples= ""
for saidx in sample_df.iloc:
    if saidx.MOLIS in sample_list:
        duplicated_samples += str(saidx.MOLIS) + '\n' 
    else:
        session.add(Sample(id = saidx.MOLIS, sample_date = saidx.SAMPLE_DT, reception_date = saidx.RECEPT_DT,
                             initial_genotype = saidx.HCVGEN, patient_id = saidx.ORDPATIDNB,  hospital_id =saidx.CORORDNB ))
        new_samples += str(saidx.MOLIS) + '\n' 


""" SEQUENCE DATA POPULATION"""

new_sequence= ""
for sqidx in sequence_df.iloc:
    if "PC" in sqidx.sequenceID:
        session.execute(update(Sequence).where(Sequence.sequence_id == sqidx.sequenceID).
                                    values(hcv_wg_pipeline = sqidx.Pipeline, pipeline_version = sqidx.Version ))
        new_sequence +=  sqidx.sequenceID + '\n' 
    else:
        session.execute(update(Sequence).where(Sequence.sequence_id == sqidx.sequenceID).
                                    values(sample_id = sqidx.sample_id, hcv_wg_pipeline = sqidx.Pipeline, pipeline_version = sqidx.Version ))
        new_sequence +=  sqidx.sequenceID + '\n' 


session.commit()   
 

"""LOG GENERATION"""

log_name = os.path.join(path_to_project,f'logs/molis/{ngs_id}_MOLIS_data_population_log.txt')
with open(log_name, 'w') as log:
    report = f''' \
MOLIS DATA POPULATION LOG - {ngs_id}\n
The following HOSPITALS were added to the table hospital in the GLUE database:\n 
{new_hospital_records}
while the ones below already existed: \n
{duplicated_hospital_records}
The following PATIENT records were added to the table patient in the GLUE database: \n
{new_patients}
while the ones below already existed: \n
{duplicated_patients}
The following SAMPLES were added to the table sample in the GLUE database: \n
{new_samples}
while the ones below already existed: \n
{duplicated_samples}\n
Details for the following SEQUENCES were added to the table sequence in the GLUE database: \n 
{new_sequence}\n
    '''
    log.write(report)

             
print(f"Check the report {log_name} for details on the data population")
