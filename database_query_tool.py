import query_engine as query
import argparse
import  os

specs = argparse.ArgumentParser(
    prog='database_query_tool.py', 
    usage='%(prog)s \t --patient/-p <patientID>\n\
                    \t\t --run/-r <NGSrun>\n\
                    \t\t --drug/-dr <drug>\n\
                    \t\t --sampledate/-d <YYYY-MM-DD>', 
    description='<<< SCRIPT IN DEVELOPMENT >>> This script generates queries for the GLUE database based on 4 different selection (patient ids, run ids, drugs or sample dates).\
                At the moment each query is independent and MUST be used individually. All the queries will return information on samples, patients,\
                genotyping results and treatments of sequences obtained from the specified selection. The results will be saved in a CSV file in logs/queries/.')
specs.add_argument('--patient', '-p', required=False, nargs='*', help='Enter the PATIENT ID(s) of interest separated by space')
specs.add_argument('--run', '-r', required=False, nargs='*', help='Enter the path to the NGS run(s) in sources separated by space (i.e. sources/NGS91 sources/NGS92).')
specs.add_argument('--drug', '-dr', required=False, nargs='*', help='Enter the DRUG(s) of interest separated by space (i.e. simeprevir sofosbuvir). Use the following list as reference:\
                                                                    simeprevir  sofosbuvir  ledipasvir  ombitasvir  paritaprevir\
                                                                   ritonavir   dasabuvir   velpatasvir voxilaprevir    glecaprevir\
                                                                   pibrentasvir    ribavarin   peginterferon alfa  grazoprevir\
                                                                    elbasvir    daclastavir asunaprevir beclabuvir')
specs.add_argument('--sampledate', '-sd', required=False, nargs='*', help='Enter the SAMPLE DATES of interest using YYYY-MM-DD format and separated by space (i.e. 2020-01-1 2020-03-1)')
parameters = specs.parse_args() #Namespace(date=None, drug=None, patient=None, run=None)


#patients = ["90","1","24","10"] 
if parameters.patient != None:
    patient_list = parameters.patient 
    query.information_by_patient(patient_list)

#run = ['NGS91', 'NGS99']
if parameters.run != None:
    run_list = []
    for run in parameters.run:
        path_to_sources = os.path.join(os.getcwd(), run)
        run_id = os.path.basename(os.path.normpath(path_to_sources))
        run_list.append(run_id)
    query.information_by_ngs_run(run_list)

# drugs = ["asunaprevir", "sofosbuvir"]
if parameters.drug != None:
    drug_list = []
    for drug in parameters.drug:
        drug_list.append(drug.lower())
    query.information_by_drug(drug_list)

# dates = ["2020-01-1","2020-03-1"]
if parameters.sampledate != None:
    dates = parameters.sampledate
    query.information_by_dates(dates) 

