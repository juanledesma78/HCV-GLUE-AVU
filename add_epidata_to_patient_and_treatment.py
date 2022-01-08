import sqlite3
import os
import re
import argparse
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import update
from sqlalchemy.orm import declarative_base,  sessionmaker
from database_model.hcv_glue_avu_sqla_model import Drug, Treatment, Patient, Sample, Sequence

specs = argparse.ArgumentParser(
    prog='add_epidata_to_patient_and_treatment.py', 
    usage='%(prog)s --sources/-s <path to the specific NGS run in directory sources>', 
    description='populate information from the EPI database to glue project')
specs.add_argument('--sources','-s', required=True, help=' path to the folder in sources/ that contains the fasta sequences which data is going to be transferred')
sources_run =specs.parse_args() 
ngs_id = re.search(r'NGS[0-9]*',sources_run.sources)
ngs_id = ngs_id.group() 


path_to_project = os.getcwd() #/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu
path_to_testing_epi_db = os.path.join(path_to_project,"tabular/epi_database.db")

conn = sqlite3.connect(path_to_testing_epi_db)
patient_epi_data = pd.read_sql_query('''select * FROM  patient ;''', conn)
treatment_data = pd.read_sql_query('''select * FROM  TREATMENT;''', conn)

""" MODIFICATIONS NEEDED FOR DATA TO WORK ON MYSQL """

patient_epi_data["diagnosis_date"]= pd.to_datetime(patient_epi_data["diagnosis_date"]).dt.strftime('%Y-%m-%d')
treatment_data["treatment_date"]= pd.to_datetime(treatment_data["treatment_date"]).dt.strftime('%Y-%m-%d')

""" ACCESS TO GLUE MYSQL DATABASE. ALL THE TABLES MUST BE INCLUDED"""

# establish connectivity to database and create Session
engine = create_engine('mysql+pymysql://gluetools:glue12345@localhost/GLUE_TOOLS', echo=True, future=True)  
Session = sessionmaker(bind=engine)
session = Session() 
Base = declarative_base()



""" DRUG DATA POPULATION"""

drug_list = [drug.id for drug in session.query(Drug)]
drug_df = pd.read_csv(os.path.join(path_to_project,'tabular/hcv_medication.csv')) 
drug_df = drug_df.replace({np.nan: None }) # nan can not be used with MySQL

duplicated_drug_records= ""
new_drug_records= ""
for didx in drug_df.iloc:
    if didx.id in drug_list:
        duplicated_drug_records +=  str(didx.id) + '\n' 
    else:
        session.add(Drug(id = didx.id, manufacturer = didx.manufacturer, therapy_class = didx.therapy_class))
        new_drug_records +=  str(didx.id) + '\n'

""" PATIENT DATA POPULATION"""

glue_patient_id = [patient.id for patient in session.query(Patient).
                                                    join(Sample, Patient.samples).
                                                    join(Sequence, Sample.sequences).
                                                    filter(Sequence.sequence_id.like(f'%{ngs_id}%'))]
run_patient_df = pd.DataFrame({'id': glue_patient_id})
epi_patient_df = pd.merge(left= patient_epi_data, right= run_patient_df, left_on= 'pid', right_on='id')
epi_patient_df = epi_patient_df.replace({np.nan: None })

extra_patient_info = ""
for epipatx in epi_patient_df.iloc:
    session.execute(update(Patient).where(Patient.id == epipatx.pid).
                                values(diagnosis_date = epipatx.diagnosis_date,
                                        country_of_birth = epipatx.country_of_birth,
                                        nationality = epipatx.nationality ,
                                        ethnicity = epipatx.ethnicity ,
                                        city_of_residence = epipatx.city ,
                                        nhs =  epipatx.NHS ,
                                        hiv_infection = epipatx.hiv_infection))
    extra_patient_info +=   str(epipatx.pid) + ' ' + \
                            str(epipatx.diagnosis_date) + ' ' + \
                            str(epipatx.country_of_birth) + ' ' + \
                            str(epipatx.nationality) + ' ' + \
                            str(epipatx.ethnicity) + ' ' + \
                            str(epipatx.city) + ' ' + \
                            str(epipatx.NHS) + ' ' + \
                            str(epipatx.hiv_infection) + ' ' + '\n'

""" TREATMENT DATA POPULATION """

glue_treatments =[]
for trt in session.query(Treatment):
    glue_treatments.append(str(trt.patient_id) + str(trt.drug_id) + str(trt.regime) + str(trt.treatment_date)) 
run_treatment_df = pd.merge(left= treatment_data, right= run_patient_df, left_on= 'pid', right_on='id')
run_treatment_df = run_treatment_df.replace({np.nan: None })

duplicated_treatment = ""
new_treatment_info = ""
for tidx in run_treatment_df.iloc:
    new_record = str(tidx.pid) + str(tidx.drug_id) + str(tidx.regime) + str(tidx.treatment_date)
    if new_record in glue_treatments:
        duplicated_treatment += str(tidx.pid) +' '+ \
                                str(tidx.drug_id) +' '+ \
                                str(tidx.regime) +' '+ \
                                str(tidx.treatment_date) + '\n'
    else:
        session.add(Treatment(patient_id = tidx.pid, drug_id = tidx.drug_id, regime = tidx.regime, treatment_date = tidx.treatment_date))
        new_treatment_info += str(tidx.pid) +' '+ \
                                str(tidx.drug_id) +' '+ \
                                str(tidx.regime) +' '+ \
                                str(tidx.treatment_date) + '\n'


session.commit() 

"""LOG GENERATION"""

log_name = os.path.join(path_to_project, f'logs/epi/{ngs_id}_EPI_data_population_log.txt')
with open(log_name, 'w') as log:
    report = f''' \
EPIDEMIOLOGICAL DATA POPULATION LOG - {ngs_id}\n
The following DRUGS were added to the table drug in the GLUE database:\n 
{new_drug_records}
while the ones below already existed: \n
{duplicated_drug_records}
The following records were updated in the table patient in the GLUE database: \n
{extra_patient_info}
The following TREATMENTS were added to the table treatment in the GLUE database: \n
{new_treatment_info}
while the ones below already existed: \n
{duplicated_treatment}\n
    '''
    log.write(report)
             
print(f"Check the report {log_name} for details on the EPI data population")
