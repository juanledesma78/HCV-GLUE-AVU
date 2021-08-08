import subprocess
import pandas as pd

# GLUE command to retrieve information from glue (subprocess)
# os to get the path and inserted in the patrh to queries? potential error depends of the path where the script is run
commands = """
project hcv_glue_avu
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/test_query_1_NGS92_SEQUENCE.csv
list sequence --whereClause "source.name like 'NGS92%' and sequenceID not like 'PC%'" sequenceID source.name genotype subtype hcv_wg_pipeline pipeline_version sample.id sample.reception_date sample.initial_genotype  sample.hospital.hospital_name sample.patient.id 
Q
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/test_query_2_NGS92_PATIENT.csv
list sequence --whereClause "source.name like 'NGS92%' and sequenceID not like 'PC%'" sequenceID sample.patient.id sample.patient.city_of_residence sample.patient.country_of_birth sample.patient.date_of_birth sample.patient.diagnosis_date sample.patient.ethnicity sample.patient.gender sample.patient.hiv_infection
Q
exit
quit
\
"""
query1 = subprocess.run("gluetools.sh" , text=True, input=commands)
if query1.returncode == 0:
    print("\nFirst query has been successfully passed in GLUE\n")
else:
    print("\nSomething went wrong")


''' Merge tables sequence, sample and patient using pandas'''

seqSample = pd.read_csv("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/tmp/test_query_1_NGS92_SEQUENCE.csv")
seqSample.rename(columns={'sequenceID':'sequence id','source.name':'run', 'sample.id':'sample id', 'sample.reception_date':'sample date',
       'sample.initial_genotype':'initial genotype', 'sample.hospital.hospital_name' :'hospital'}, inplace=True) 
       #,'sample.patient.id' :'patient id' remove so the final fields will be sample.patient.id and patient id instead of patient id_x and _y
       #left_on= 'sample.patient.id_x', right_on='patient.id'
seqPatient = pd.read_csv("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/tmp/test_query_2_NGS92_PATIENT.csv")
seqPatient.rename(columns={'sequenceID':'sequence id','sample.patient.id' :'patient id', 'sample.patient.city_of_residence':'city',
       'sample.patient.country_of_birth':'country of birth', 'sample.patient.date_of_birth':'date of birth',
       'sample.patient.diagnosis_date':'diagnosis date', 'sample.patient.ethnicity':'ethnicity',
       'sample.patient.gender':'gender', 'sample.patient.hiv_infection':'hiv status'}, inplace=True) 


seqSamplePatient = pd.merge(left = seqSample, right = seqPatient, how = "left" , left_on= 'sequence id', right_on='sequence id')
# just for testing, delete when finished
#seqSamplePatient.to_csv("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/SAMPLE_PATIENT_TEST_NGS91.csv",index=False) # just for testing, delete when finished
# ########################################


''' generate a list with patient Ids to make a second query in GLUE '''
patients = seqSamplePatient.drop_duplicates(subset=['patient id']) # remove duplicates
patient_list =[] # create a list which include the number (string) between '' to be used in sql commands
for patient in patients['patient id']:
       patient_list.append("'"+ str(patient) +"'" )
Patientwhereclause =""
for i in range(len(patient_list)):
       if len(patient_list) == 0:
              break # this will affect the second subprocess and merging the info!
       else:
              pid = patient_list[i]
              if Patientwhereclause =="":
                     Patientwhereclause += "(" + pid
              else:
                     Patientwhereclause += "," + pid
              
Patientwhereclause += ")" # ('1','2','3','5'...'37','38','39')

''' second subprocess'''
new_command = """
project hcv_glue_avu
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/test_query_3_NGS92_TREATMENT.csv
list custom-table-row treatment --whereClause "patient in PatientList" id patient.id regime treatment_date  drug.id drug.manufacturer drug.therapy_class
Q
exit
quit 
\
"""
new_command = new_command.replace('PatientList', Patientwhereclause)
query2 = subprocess.run("gluetools.sh" , text=True, input=new_command)
if query2.returncode == 0:
    print("\nSecond query has been successfully passed in GLUE")
    print("""\n--------------------------------------
             \nQueries successfully submitted to GLUE
             \n--------------------------------------""")
else:
    print("\nSomething went wrong")

''' getting treatment table from GLUE'''
treatment = pd.read_csv("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/tmp/test_query_3_NGS92_TREATMENT.csv")
treatment.rename(columns={'id':'treatment id', 'patient.id':'patient id', 'treatment_date':'treatment date', 'drug.id':'drug id',
       'drug.manufacturer':'drug manufacturer', 'drug.therapy_class': 'therapy class'},inplace=True)


'''final table'''
info = pd.merge(left = seqSamplePatient, right = treatment, how = "left" , left_on= 'patient id', right_on='patient id')
info.sort_values(by=['patient id','sample date', 'treatment date'], inplace = True)
info[['sequence id', 'run', 'hcv_wg_pipeline','pipeline_version','sample id', 'sample date','initial genotype','genotype', 'subtype','patient id', 'treatment id', 'regime', 'treatment date','drug id', 'drug manufacturer', 'therapy class', 'city','country of birth', 'date of birth', 'diagnosis date', 'ethnicity','gender', 'hiv status']].to_csv("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/query_TEST_NGS92.csv",index=False)
