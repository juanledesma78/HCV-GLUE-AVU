import subprocess
import pandas as pd
ngs_id = input("Please specify the NGS of interest by typing NGS and number for the experiment (i.e. NGS1978)\n").upper()

# GLUE command to retrieve information from glue (subprocess)
# os to get the path and inserted in the patrh to queries? potential error depends of the path where the script is run
first_query = """
project hcv_glue_avu
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/query_1_[NGSid]_SEQUENCE.csv
list sequence --whereClause "source.name like '[NGSid]%' and sequenceID not like 'PC%'" sequenceID source.name genotype subtype hcv_wg_pipeline pipeline_version sample.id sample.sample_date sample.reception_date sample.initial_genotype  sample.hospital.hospital_name sample.patient.id 
Q
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/query_2_[NGSid]_PATIENT.csv
list sequence --whereClause "source.name like '[NGSid]%' and sequenceID not like 'PC%'" sequenceID sample.patient.id sample.patient.city_of_residence sample.patient.country_of_birth sample.patient.date_of_birth sample.patient.diagnosis_date sample.patient.ethnicity sample.patient.nationality sample.patient.gender sample.patient.hiv_infection
Q
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/query_3_[NGSid]_GENOTYPING.csv
list sequence -w "source.name like'[NGSid]%'" sequenceID  genotyping_core genotyping_e1 genotyping_e2 genotyping_p7 genotyping_ns2 genotyping_ns3 genotyping_ns4a genotyping_ns4b genotyping_ns5a genotyping_ns5b
Q
exit
quit
\
"""
updated_first_query = first_query.replace("[NGSid]", ngs_id)

query1 = subprocess.run("gluetools.sh" , text=True, input=updated_first_query)
if query1.returncode == 0:
    print("\nFirst query has been successfully passed in GLUE\n")
else:
    print("\nSomething went wrong")


''' Merge tables sequence, sample and patient using pandas'''

path_to_seq_sample = "/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/tmp/query_1_" + ngs_id + "_SEQUENCE.csv"
path_to_seq_patient = "/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/tmp/query_2_" + ngs_id + "_PATIENT.csv"
path_to_seq_genotyping = "/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/tmp/query_3_" + ngs_id + "_GENOTYPING.csv"

seq_sample = pd.read_csv(path_to_seq_sample)
seq_patient = pd.read_csv(path_to_seq_patient)
seq_genotyping = pd.read_csv(path_to_seq_genotyping)

seq_sample.rename(columns={'sequenceID':'sequence id','source.name':'run', 'sample.id':'sample id', 
                            'sample.reception_date':'sample reception date', 'sample.sample_date':'sample date',
                            'sample.initial_genotype':'initial genotype', 'sample.hospital.hospital_name' :'hospital'}, inplace=True) 

seq_patient.rename(columns={'sequenceID':'sequence id','sample.patient.id' :'patient id', 'sample.patient.city_of_residence':'city',
                            'sample.patient.country_of_birth':'country of birth', 'sample.patient.date_of_birth':'date of birth',
                            'sample.patient.diagnosis_date':'diagnosis date', 'sample.patient.ethnicity':'ethnicity', 
                            'sample.patient.nationality' : 'nationality', 'sample.patient.gender':'gender', 
                            'sample.patient.hiv_infection':'hiv status'}, inplace=True) 

seq_genotyping.rename(columns={'sequenceID':'sequence id', 'genotyping_core':'Genotyping CORE','genotyping_e1':'Genotyping E1',
                            'genotyping_e2':'Genotyping E2','genotyping_p7':'Genotyping P7','genotyping_ns2':'Genotyping NS2',
                            'genotyping_ns3':'Genotyping NS3','genotyping_ns4a':'Genotyping NS4A','genotyping_ns4b':'Genotyping NS4B',
                            'genotyping_ns5a':'Genotyping NS5A','genotyping_ns5b':'Genotyping NS5B'}, inplace=True)



seq_sample_patient = pd.merge(left= seq_sample, right= seq_patient, how= "left" , left_on= 'sequence id', right_on='sequence id')  
                                                                                  #left_on= 'sample.patient.id_x', right_on='patient.id'
seq_sample_patient_genotypes = pd.merge(left= seq_sample_patient, right= seq_genotyping, how = "left" , left_on= 'sequence id', right_on='sequence id')


''' generate a list with patient Ids to make a second query in GLUE '''
patients = seq_sample_patient.drop_duplicates(subset=['patient id']) 
patient_list =[] # create a list which include the number (string) between '' to be used in sql commands
for patient in patients['patient id']:
       patient_list.append("'"+ str(patient) +"'" )
patient_whereclause =""
for i in range(len(patient_list)):
       if len(patient_list) == 0:
              break # this will affect the second subprocess and merging the info!
       else:
              pid = patient_list[i]
              if patient_whereclause =="":
                     patient_whereclause += "(" + pid
              else:
                     patient_whereclause += "," + pid
              
patient_whereclause += ")" # ('1','2','3','5'...'37','38','39')

''' second subprocess'''
second_query = """
project hcv_glue_avu
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/query_4_[NGSid]_TREATMENT.csv
list custom-table-row treatment --whereClause "patient in PatientList" id patient.id regime treatment_date drug.id drug.manufacturer drug.therapy_class
Q
exit
quit 
\
"""
updated_second_query = second_query.replace("[NGSid]", ngs_id)
updated_second_query = updated_second_query.replace('PatientList', patient_whereclause)
query2 = subprocess.run("gluetools.sh" , text=True, input=updated_second_query)

if query2.returncode == 0:
    print("\nSecond query has been successfully passed in GLUE")
    print("""\n--------------------------------------
             \nQueries successfully submitted to GLUE
             \n--------------------------------------""")
else:
    print("\nSomething went wrong")

''' getting treatment table from GLUE'''
path_to_treatment = "/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/tmp/query_4_" + ngs_id+ "_TREATMENT.csv"
treatment = pd.read_csv(path_to_treatment)
treatment.rename(columns={'id':'treatment id', 'patient.id':'patient id', 'treatment_date':'treatment date', 'drug.id':'drug id',
       'drug.manufacturer':'drug manufacturer', 'drug.therapy_class': 'therapy class'},inplace=True)


'''final table'''
info = pd.merge(left= seq_sample_patient_genotypes, right= treatment, how= "left" , left_on= 'patient id', right_on='patient id')
info.sort_values(by=['patient id','sample date', 'treatment date'], inplace = True)

file_name = "/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/query_"+ ngs_id +".csv"
info[['sequence id', 'run', 'hcv_wg_pipeline','pipeline_version','sample id', 'sample date','initial genotype',
       'genotype', 'subtype','Genotyping CORE', 'Genotyping E1','Genotyping E2','Genotyping P7','Genotyping NS2',
       'Genotyping NS3','Genotyping NS4A','Genotyping NS4B','Genotyping NS5A','Genotyping NS5B' ,'patient id', 
       'treatment id', 'regime', 'treatment date','drug id', 'drug manufacturer', 'therapy class', 'city',
       'country of birth', 'date of birth', 'diagnosis date', 'ethnicity','nationality','gender', 
       'hiv status']].to_csv(file_name,index=False)

