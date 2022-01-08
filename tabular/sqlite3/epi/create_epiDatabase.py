import sqlite3
import pandas as pd
conn = sqlite3.connect("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/sqlite3/epi/epi_database.db") # create the database

cur = conn.cursor()

#create table
cur.execute(''' CREATE TABLE PATIENT 
                    (pid TEXT NOT NULL, 
                    NHS,
                      nationality TEXT,
                      country_of_birth,
                      ethnicity, 
                      diagnosis_date,
                      city, 
                      hiv_infection                      
                      ) ;
                    ''')

cur.execute(''' CREATE TABLE TREATMENT
                     (id PRIMARY KEY, 
                      pid TEXT NOT NULL, 
                     drug_id TEXT NOT NULL, 
                     regime TEXT,
                     treatment_date TEXT,
                     FOREIGN KEY(pid) REFERENCES PATIENT(pid)
                     FOREIGN KEY(drug_id) REFERENCES DRUG(drug_id) 
                        ) ;''')
"""
cur.execute(''' CREATE TABLE DRUG
                     (drug_id TEXT NOT NULL,
                     manufacturer, 
                     therapy_class  ,
                     ) ;''')"""


patients = pd.read_csv('/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/sqlite3/epi/patients.csv')
patients.to_sql('PATIENT', conn, if_exists='append', index = False)

treatment = pd.read_csv('/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/sqlite3/epi/treatment.csv')
treatment.to_sql('TREATMENT', conn, if_exists='append', index = False)

drugs = pd.read_csv('/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/sqlite3/epi/hcv_medication.csv')
drugs.to_sql('DRUG', conn, if_exists='append', index = False)




# save changes in the database
conn.commit()

# close the connections
conn.close() 
