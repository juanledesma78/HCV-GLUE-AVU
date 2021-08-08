import sqlite3
import sys, os, re, subprocess
import pandas as pd
NGS=(input("Enter a NGS id (i.e. NGS1): \n")).upper()
conn = sqlite3.connect("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/tabular/epi_database.db")

extra_patient_data = pd.read_sql_query('''select * FROM  patient ;''', conn)
treatment_data = pd.read_sql_query('''select * FROM  TREATMENT;''', conn)

extra_patient_data["diagnosis_date"]= pd.to_datetime(extra_patient_data["diagnosis_date"])
extra_patient_data["diagnosis_date"] = extra_patient_data["diagnosis_date"].dt.strftime('%d-%b-%Y') 

treatment_data["treatment_date"]= pd.to_datetime(treatment_data["treatment_date"])
treatment_data["treatment_date"] = treatment_data["treatment_date"].dt.strftime('%d-%b-%Y') 

path_to_tabular = "/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/tabular/"
table_patient = pd.read_csv(path_to_tabular + "table_patient/metadata_table_PATIENT_" + NGS + ".csv") #ORDPATIDNB

# merge using two columns with different names
additional_info_patient = pd.merge(left=extra_patient_data, right= table_patient, left_on= 'pid', right_on='ORDPATIDNB')
treatment = pd.merge(left=treatment_data, right= table_patient, left_on= 'pid', right_on='ORDPATIDNB')

additional_info_patient[["pid","nationality","country_of_birth","ethnicity","diagnosis_date","hiv_infection","city","NHS"]].to_csv(path_to_tabular+ "epi_data/Epidata_table_PATIENT_" + NGS + ".csv", index= False ) 
treatment[["id","pid","drug_id","regime","treatment_date"]].to_csv(path_to_tabular + "epi_data/Treatment_" + NGS + ".csv", index= False ) 


"""populate data in GLUE """
# modify id of javascript according to NGS

epidata_patient_js = ""
with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/populateEpiDataPatient.js",'r') as script:
    text = script.read()
    epidata_patient_js = re.sub(r'Epidata_table_PATIENT_[a-zA-Z0-9]*.csv','Epidata_table_PATIENT_'+ NGS + '.csv', text)
    script.close()
with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/populateEpiDataPatient.js",'w') as script:
    script.write(epidata_patient_js)
    script.close()

treatment_js = ""
with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/populateTreatmentTable.js",'r') as script:
    text = script.read()
    treatment_js = re.sub(r'Treatment_[a-zA-Z0-9]*.csv','Treatment_'+ NGS + '.csv', text)
    script.close()
with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/populateTreatmentTable.js",'w') as script:
    script.write(treatment_js)
    script.close()


Glue_commands = """ 
project hcv_glue_avu
run script glue/populateEpiDataPatient.js
run script glue/populateTreatmentTable.js
exit
quit 
\
"""

p1 = subprocess.run("gluetools.sh" , text=True, input=Glue_commands)
if p1.returncode == 0:
    print("\nEpidemiological data successfully imported in GLUE\n")
else:
    print("\nSomething went wrong")




