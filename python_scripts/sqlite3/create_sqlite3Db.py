import sqlite3
import pandas as pd
conn = sqlite3.connect("/home/juan/gluetools/projects/HCV-GLUE-AVU/python_scripts/sqlite3/molis.db") # create the database

#create a cursor https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor
# to execute different things in the database
cur = conn.cursor()

#create table
cur.execute(''' CREATE TABLE STAT_ORD 
                    (LID TEXT NOT NULL, 
                    LPERIOD TEXT  NOT NULL, 
                    ORDNB INTEGER  NOT NULL, 
                    SAMPLE_DT TEXT,  
                    RECEPT_DT TEXT, 
                    CORORDNB TEXT, 
                    HOSP_FL, 
                    ORDPATNAME TEXT, 
                    ORDPATBIRTHDT TEXT, 
                    ORDPATSX TEXT, 
                    ORDPATIDNB TEXT, 
                    CORORDSUBNB, 
                    REFEXT TEXT, 
                    EXTPATIDNB TEXT, 
                    REC_SITE_NB TEXT,
                    UNIQUE (LID, LPERIOD, ORDNB),
                    FOREIGN KEY(LID, LPERIOD, ORDNB) REFERENCES STAT_ORDANAEL(LID, LPERIOD, ORDNB)
                    FOREIGN KEY(CORORDNB) REFERENCES STAT_COR(CORNB)                  
                      --for composite primary keys  
                      ) 
                    ''')

cur.execute(''' CREATE TABLE STAT_ORDANAEL
                     (LID TEXT NOT NULL, 
                     LPERIOD TEXT  NOT NULL, 
                     ORDNB INTEGER  NOT NULL, 
                     MC TEXT,
                     RES_NUM,
                     RES_TXT,
                     SPSEQ INTEGER, 
                     NBINT INTEGER,
                     --UNIQUE (LID, LPERIOD, ORDNB),
                     PRIMARY KEY (LID, LPERIOD, ORDNB, NBINT),
                     FOREIGN KEY(LID, LPERIOD, ORDNB) REFERENCES STAT_SAMPLEPOS_CONT_V(LID, LPERIOD, ORDNB) 
                        ) ''')

cur.execute(''' CREATE TABLE STAT_SAMPLEPOS_CONT_V
                     (LID TEXT NOT NULL, 
                     LPERIOD TEXT  NOT NULL, 
                     ORDNB INTEGER  NOT NULL, 
                     CONTMC TEXT,
                     CONTMCSEQ INTEGER,
                     POS INTEGER,
                     BCSEQ INTEGER,
                     BC TEXT,
                     UNIQUE (LID, LPERIOD, ORDNB)
                     ) ''')

cur.execute(''' CREATE TABLE STAT_COR
                     (CORNB TEXT NOT NULL, 
                     CORNB_FULLNAME TEXT  
                     ) ''')

STAT_ORD_csv = pd.read_csv('/home/juan/gluetools/projects/HCV-GLUE-AVU/python_scripts/sqlite3/STAT_ORD.csv')
STAT_ORD_csv.to_sql('STAT_ORD', conn, if_exists='append', index = False)

STAT_ORDANAEL_csv = pd.read_csv('/home/juan/gluetools/projects/HCV-GLUE-AVU/python_scripts/sqlite3/STAT_ORDANAEL.csv')
STAT_ORDANAEL_csv.to_sql('STAT_ORDANAEL', conn, if_exists='append', index = False)

STAT_SAMPLEPOS_CONT_V_csv = pd.read_csv('/home/juan/gluetools/projects/HCV-GLUE-AVU/python_scripts/sqlite3/STAT_SAMPLEPOS_CONT_V.csv')
STAT_SAMPLEPOS_CONT_V_csv.to_sql('STAT_SAMPLEPOS_CONT_V', conn, if_exists='append', index = False)

STAT_COR_csv = pd.read_csv('/home/juan/gluetools/projects/HCV-GLUE-AVU/python_scripts/sqlite3/STAT_COR.csv')
STAT_COR_csv.to_sql('STAT_COR', conn, if_exists='append', index = False)



# save changes in the database
conn.commit()

# close the connections
conn.close() 
