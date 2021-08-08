import subprocess
import pandas as pd

# GLUE command to retrieve information from glue (subprocess)
commands = """
project hcv_glue_avu
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/test_query_1_NGS91_SEQUENCE.csv
list sequence --whereClause "source.name like 'NGS91%' and sequenceID not like 'PC%'" sequenceID source.name genotype subtype hcv_wg_pipeline pipeline_version sample.id sample.reception_date sample.initial_genotype  sample.hospital.hospital_name sample.patient.id 
Q
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/test_query_2_NGS91_PATIENT.csv
list sequence --whereClause "source.name like 'NGS91%' and sequenceID not like 'PC%'" sequenceID sample.patient.id sample.patient.city_of_residence sample.patient.country_of_birth sample.patient.date_of_birth sample.patient.diagnosis_date sample.patient.ethnicity sample.patient.gender sample.patient.hiv_infection
Q
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/test_query_3_NGS91_TREATMENT.csv
list custom-table-row treatment id patient.id regime treatment_date  drug.id drug.manufacturer
Q 
exit
quit
\\\
"""
query = subprocess.run("gluetools.sh" , text=True, input=commands)
if query.returncode == 0:
    print("\nGLUE commands succesfully passed through subprocess module\n")
else:
    print("Something went wrong")


''' Merge tables using pandas'''

seqSample = pd.read_csv("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/tmp/test_query_1_NGS91_SEQUENCE.csv")
seqSample.rename(columns={'sequenceID':'sequence id','source.name':'run', 'sample.id':'sample id', 'sample.reception_date':'sample date',
       'sample.initial_genotype':'initial genotype', 'sample.hospital.hospital_name' :'hospital'}, inplace=True) 
       #,'sample.patient.id' :'patient id' remove so the final fields will be sample.patient.id and patient id instead of patient id_x and _y
       #left_on= 'sample.patient.id_x', right_on='patient.id'
seqPatient = pd.read_csv("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/tmp/test_query_2_NGS91_PATIENT.csv")
seqPatient.rename(columns={'sequenceID':'sequence id','sample.patient.id' :'patient id', 'sample.patient.city_of_residence':'city',
       'sample.patient.country_of_birth':'country of birth', 'sample.patient.date_of_birth':'date of birth',
       'sample.patient.diagnosis_date':'diagnosis date', 'sample.patient.ethnicity':'ethnicity',
       'sample.patient.gender':'gender', 'sample.patient.hiv_infection':'hiv status'}, inplace=True) 
treatment = pd.read_csv("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/tmp/test_query_3_NGS91_TREATMENT.csv")
treatment.rename(columns={'id':'treatment id', 'patient.id':'patient id', 'treatment_date':'treatment date', 'drug.id':'drug id',
       'drug.manufacturer':'drug manufacturer'},inplace=True)

info = pd.merge(left = seqSample, right = seqPatient, how = "left" , left_on= 'sequence id', right_on='sequence id')
# just for testing, delete when finished
info.to_csv("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/SAMPLE_PATIENT_TEST_NGS91.csv",index=False) # just for testing, delete when finished
# ########################################

info = pd.merge(left = info, right = treatment, how = "left" , left_on= 'patient id', right_on='patient id')
info[['sequence id', 'run', 'hcv_wg_pipeline','pipeline_version','sample id', 'sample date','initial genotype','genotype', 'subtype','patient id', 'treatment id', 'regime', 'treatment date','drug id', 'drug manufacturer', 'city','country of birth', 'date of birth', 'diagnosis date', 'ethnicity','gender', 'hiv status']].to_csv("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/ALL_TABLES_TEST_NGS91.csv",index=False)

