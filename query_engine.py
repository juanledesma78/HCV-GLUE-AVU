from sqlalchemy import create_engine
from sqlalchemy import select 
from sqlalchemy.orm import declarative_base, sessionmaker
from database_model.hcv_glue_avu_sqla_model import Sequence, Sample, Patient, Hospital, Drug, Treatment
import os
import csv # instead of pandas

""" ACCESS TO GLUE MYSQL DATABASE"""

engine = create_engine('mysql+pymysql://gluetools:glue12345@localhost/GLUE_TOOLS', echo=True, future=True)  
Session = sessionmaker(bind=engine)
session = Session() 
Base = declarative_base()
# Base.metadata.create_all(engine)

path_to_query_results = os.path.join(os.getcwd(), "logs/queries") 

def information_by_ngs_run(ngs_run):
    """ It returns information on samples, patients, genotyping results and treatments of sequences obtained from a selection of NGS runs"""    
    
    query_id = '_'.join([run for run in ngs_run])
    file_name = os.path.join(path_to_query_results, f"Selection_RUN_{query_id}_query_result.csv")
    
    with open(file_name, 'w') as results:
        out_file = csv.writer(results)
        out_file.writerow(['Patient ID', 'Sample ID', 'RUN', 'Sample Date', 'Reception date',
                            'Gender', 'Date of Birth', 'Diagnosis date', 'Country', 'Nationality', 
                            'Ethnicity', 'City of resisdence', 'NHS number', 'HIV infection', 
                            'Pipeline', 'Hospital Name', 'Initial Genotype', 'Genotype', 'Subtype',
                            'Genotyping CORE', 'Genotyping E1',	'Genotyping E2','Genotyping P7', 
                            'Genotyping NS2', 'Genotyping NS3','Genotyping NS4A', 'Genotyping NS4B', 
                            'Genotyping NS5A',' Genotyping NS5B',
                            'Drug', 'Manufacturer', 'Therapy Class', 'Regime', 'Treatment date'])
            
        for row  in session.execute(select(Sample, Sequence, Patient, Hospital, Drug, Treatment).\
                                                                        order_by(Patient.id).\
                                                                        join(Sequence, Sample.sequences).\
                                                                        join(Patient, Sample.patient).\
                                                                        join(Hospital, Sample.hospital).\
                                                                        outerjoin(Treatment, Patient.treatments).\
                                                                        outerjoin(Drug,Treatment.drug).\
                                                                        filter(Sequence.source_name.in_(ngs_run))).all():
            if row.Treatment and row.Drug:
                out_file.writerow([row.Patient.id, row.Sample.id, row.Sequence.source_name, row.Sample.sample_date, row.Sample.reception_date,
                                    row.Patient.gender , row.Patient.date_of_birth , row.Patient.diagnosis_date , row.Patient.country_of_birth , row.Patient.nationality ,
                                    row.Patient.ethnicity , row.Patient.city_of_residence , row.Patient.nhs , row.Patient.hiv_infection ,
                                    row.Sequence.hcv_wg_pipeline, row.Hospital.name, row.Sample.initial_genotype, row.Sequence.genotype,row.Sequence.subtype,
                                    row.Sequence.genotyping_core, row.Sequence.genotyping_e1, row.Sequence.genotyping_e2, row.Sequence.genotyping_p7,
                                    row.Sequence.genotyping_ns2, row.Sequence.genotyping_ns3, row.Sequence.genotyping_ns4a, row.Sequence.genotyping_ns4b,
                                    row.Sequence.genotyping_ns5a,row.Sequence.genotyping_ns5b, 
                                    row.Drug.id, row.Drug.manufacturer, row.Drug.therapy_class, 
                                    row.Treatment.regime, row.Treatment.treatment_date ])
            
            else:
                out_file.writerow([row.Patient.id, row.Sample.id, row.Sequence.source_name, row.Sample.sample_date, row.Sample.reception_date,
                                    row.Patient.gender , row.Patient.date_of_birth , row.Patient.diagnosis_date , row.Patient.country_of_birth , row.Patient.nationality ,
                                    row.Patient.ethnicity , row.Patient.city_of_residence , row.Patient.nhs , row.Patient.hiv_infection ,
                                    row.Sequence.hcv_wg_pipeline, row.Hospital.name, row.Sample.initial_genotype, row.Sequence.genotype, row.Sequence.subtype,
                                    row.Sequence.genotyping_core, row.Sequence.genotyping_e1, row.Sequence.genotyping_e2, row.Sequence.genotyping_p7,
                                    row.Sequence.genotyping_ns2, row.Sequence.genotyping_ns3, row.Sequence.genotyping_ns4a, row.Sequence.genotyping_ns4b,
                                    row.Sequence.genotyping_ns5a,row.Sequence.genotyping_ns5b])
    print(f"Check report on {file_name} for details")



def information_by_patient(list_of_patients):
    """ It returns information on samples, patients, genotyping results and treatments of sequences obtained from a selection of PATIENTS"""    
    
    query_id = '_'.join([patient for patient in list_of_patients])
    file_name = os.path.join(path_to_query_results, f"Selection_PATIENT_{query_id}_query_result.csv")
    
    
    with open(file_name, 'w') as results:
        out_file = csv.writer(results)
        out_file.writerow(['Patient ID', 'Sample ID', 'RUN', 'Sample Date', 'Reception date',
                            'Gender', 'Date of Birth', 'Diagnosis date', 'Country', 'Nationality', 
                            'Ethnicity', 'City of resisdence', 'NHS number', 'HIV infection', 
                            'Pipeline', 'Hospital Name', 'Initial Genotype', 'Genotype', 'Subtype',
                            'Genotyping CORE', 'Genotyping E1',	'Genotyping E2','Genotyping P7', 
                            'Genotyping NS2', 'Genotyping NS3','Genotyping NS4A', 'Genotyping NS4B', 
                            'Genotyping NS5A',' Genotyping NS5B',
                            'Drug', 'Manufacturer', 'Therapy Class', 'Regime', 'Treatment date'])
            
        for row  in session.execute(select(Sample, Sequence, Patient, Hospital, Drug, Treatment).\
                                                                        order_by(Patient.id).\
                                                                        join(Sequence, Sample.sequences).\
                                                                        join(Patient, Sample.patient).\
                                                                        join(Hospital, Sample.hospital).\
                                                                        outerjoin(Treatment, Patient.treatments).\
                                                                        outerjoin(Drug,Treatment.drug).\
                                                                        filter(Patient.id.in_(list_of_patients))).all():
            if row.Treatment and row.Drug:
                out_file.writerow([row.Patient.id, row.Sample.id, row.Sequence.source_name, row.Sample.sample_date, row.Sample.reception_date,
                                    row.Patient.gender , row.Patient.date_of_birth , row.Patient.diagnosis_date , row.Patient.country_of_birth , row.Patient.nationality ,
                                    row.Patient.ethnicity , row.Patient.city_of_residence , row.Patient.nhs , row.Patient.hiv_infection ,
                                    row.Sequence.hcv_wg_pipeline, row.Hospital.name, row.Sample.initial_genotype, row.Sequence.genotype,row.Sequence.subtype,
                                    row.Sequence.genotyping_core, row.Sequence.genotyping_e1, row.Sequence.genotyping_e2, row.Sequence.genotyping_p7,
                                    row.Sequence.genotyping_ns2, row.Sequence.genotyping_ns3, row.Sequence.genotyping_ns4a, row.Sequence.genotyping_ns4b,
                                    row.Sequence.genotyping_ns5a,row.Sequence.genotyping_ns5b, 
                                    row.Drug.id, row.Drug.manufacturer, row.Drug.therapy_class, 
                                    row.Treatment.regime, row.Treatment.treatment_date ])
            
            else:
                out_file.writerow([row.Patient.id, row.Sample.id, row.Sequence.source_name, row.Sample.sample_date, row.Sample.reception_date,
                                    row.Patient.gender , row.Patient.date_of_birth , row.Patient.diagnosis_date , row.Patient.country_of_birth , row.Patient.nationality ,
                                    row.Patient.ethnicity , row.Patient.city_of_residence , row.Patient.nhs , row.Patient.hiv_infection ,
                                    row.Sequence.hcv_wg_pipeline, row.Hospital.name, row.Sample.initial_genotype, row.Sequence.genotype, row.Sequence.subtype,
                                    row.Sequence.genotyping_core, row.Sequence.genotyping_e1, row.Sequence.genotyping_e2, row.Sequence.genotyping_p7,
                                    row.Sequence.genotyping_ns2, row.Sequence.genotyping_ns3, row.Sequence.genotyping_ns4a, row.Sequence.genotyping_ns4b,
                                    row.Sequence.genotyping_ns5a,row.Sequence.genotyping_ns5b])
    print(f"Check report on {file_name} for details")



def information_by_drug(drugs):
    """ It returns information on samples, patients, genotyping results and treatments of sequences obtained from a selection of ANTIVIRALS"""    
    
    query_id = '_'.join([drug for drug in drugs])
    file_name = os.path.join(path_to_query_results, f"Selection_DRUG_{query_id}_query_result.csv")
    
    
    with open(file_name, 'w') as results:
        out_file = csv.writer(results)
        out_file.writerow(['Patient ID', 'Sample ID', 'RUN', 'Sample Date', 'Reception date',
                            'Gender', 'Date of Birth', 'Diagnosis date', 'Country', 'Nationality', 
                            'Ethnicity', 'City of resisdence', 'NHS number', 'HIV infection', 
                            'Pipeline', 'Hospital Name', 'Initial Genotype', 'Genotype', 'Subtype',
                            'Genotyping CORE', 'Genotyping E1',	'Genotyping E2','Genotyping P7', 
                            'Genotyping NS2', 'Genotyping NS3','Genotyping NS4A', 'Genotyping NS4B', 
                            'Genotyping NS5A',' Genotyping NS5B',
                            'Drug', 'Manufacturer', 'Therapy Class', 'Regime', 'Treatment date'])
            
        for row  in session.execute(select(Sample, Sequence, Patient, Hospital, Drug, Treatment).\
                                                                        order_by(Patient.id).\
                                                                        join(Sequence, Sample.sequences).\
                                                                        join(Patient, Sample.patient).\
                                                                        join(Hospital, Sample.hospital).\
                                                                        outerjoin(Treatment, Patient.treatments).\
                                                                        outerjoin(Drug,Treatment.drug).\
                                                                        filter(Drug.id.in_(drugs))).all():
            if row.Treatment and row.Drug:
                out_file.writerow([row.Patient.id, row.Sample.id, row.Sequence.source_name, row.Sample.sample_date, row.Sample.reception_date,
                                    row.Patient.gender , row.Patient.date_of_birth , row.Patient.diagnosis_date , row.Patient.country_of_birth , row.Patient.nationality ,
                                    row.Patient.ethnicity , row.Patient.city_of_residence , row.Patient.nhs , row.Patient.hiv_infection ,
                                    row.Sequence.hcv_wg_pipeline, row.Hospital.name, row.Sample.initial_genotype, row.Sequence.genotype,row.Sequence.subtype,
                                    row.Sequence.genotyping_core, row.Sequence.genotyping_e1, row.Sequence.genotyping_e2, row.Sequence.genotyping_p7,
                                    row.Sequence.genotyping_ns2, row.Sequence.genotyping_ns3, row.Sequence.genotyping_ns4a, row.Sequence.genotyping_ns4b,
                                    row.Sequence.genotyping_ns5a,row.Sequence.genotyping_ns5b, 
                                    row.Drug.id, row.Drug.manufacturer, row.Drug.therapy_class, 
                                    row.Treatment.regime, row.Treatment.treatment_date ])
            
            else:
                out_file.writerow([row.Patient.id, row.Sample.id, row.Sequence.source_name, row.Sample.sample_date, row.Sample.reception_date,
                                    row.Patient.gender , row.Patient.date_of_birth , row.Patient.diagnosis_date , row.Patient.country_of_birth , row.Patient.nationality ,
                                    row.Patient.ethnicity , row.Patient.city_of_residence , row.Patient.nhs , row.Patient.hiv_infection ,
                                    row.Sequence.hcv_wg_pipeline, row.Hospital.name, row.Sample.initial_genotype, row.Sequence.genotype, row.Sequence.subtype,
                                    row.Sequence.genotyping_core, row.Sequence.genotyping_e1, row.Sequence.genotyping_e2, row.Sequence.genotyping_p7,
                                    row.Sequence.genotyping_ns2, row.Sequence.genotyping_ns3, row.Sequence.genotyping_ns4a, row.Sequence.genotyping_ns4b,
                                    row.Sequence.genotyping_ns5a,row.Sequence.genotyping_ns5b])
    print(f"Check report on {file_name} for details")



def information_by_dates(dates):
    """ It returns information on samples, patients, genotyping results and treatments of sequences obtained from a selection of DATES"""    
    
    query_id = '_'.join([date for date in dates])
    file_name = os.path.join(path_to_query_results, f"Selection_DATES_{query_id}_query_result.csv")
    
    
    with open(file_name, 'w') as results:
        out_file = csv.writer(results)
        out_file.writerow(['Patient ID', 'Sample ID', 'RUN', 'Sample Date', 'Reception date',
                            'Gender', 'Date of Birth', 'Diagnosis date', 'Country', 'Nationality', 
                            'Ethnicity', 'City of resisdence', 'NHS number', 'HIV infection', 
                            'Pipeline', 'Hospital Name', 'Initial Genotype', 'Genotype', 'Subtype',
                            'Genotyping CORE', 'Genotyping E1',	'Genotyping E2','Genotyping P7', 
                            'Genotyping NS2', 'Genotyping NS3','Genotyping NS4A', 'Genotyping NS4B', 
                            'Genotyping NS5A',' Genotyping NS5B',
                            'Drug', 'Manufacturer', 'Therapy Class', 'Regime', 'Treatment date'])
            
        for row  in session.execute(select(Sample, Sequence, Patient, Hospital, Drug, Treatment).\
                                                                        order_by(Patient.id).\
                                                                        join(Sequence, Sample.sequences).\
                                                                        join(Patient, Sample.patient).\
                                                                        join(Hospital, Sample.hospital).\
                                                                        outerjoin(Treatment, Patient.treatments).\
                                                                        outerjoin(Drug,Treatment.drug).\
                                                                        filter(Sample.sample_date.between(dates[0],dates[1]))).all():
            if row.Treatment and row.Drug:
                out_file.writerow([row.Patient.id, row.Sample.id, row.Sequence.source_name, row.Sample.sample_date, row.Sample.reception_date,
                                    row.Patient.gender , row.Patient.date_of_birth , row.Patient.diagnosis_date , row.Patient.country_of_birth , row.Patient.nationality ,
                                    row.Patient.ethnicity , row.Patient.city_of_residence , row.Patient.nhs , row.Patient.hiv_infection ,
                                    row.Sequence.hcv_wg_pipeline, row.Hospital.name, row.Sample.initial_genotype, row.Sequence.genotype,row.Sequence.subtype,
                                    row.Sequence.genotyping_core, row.Sequence.genotyping_e1, row.Sequence.genotyping_e2, row.Sequence.genotyping_p7,
                                    row.Sequence.genotyping_ns2, row.Sequence.genotyping_ns3, row.Sequence.genotyping_ns4a, row.Sequence.genotyping_ns4b,
                                    row.Sequence.genotyping_ns5a,row.Sequence.genotyping_ns5b, 
                                    row.Drug.id, row.Drug.manufacturer, row.Drug.therapy_class, 
                                    row.Treatment.regime, row.Treatment.treatment_date ])
            
            else:
                out_file.writerow([row.Patient.id, row.Sample.id, row.Sequence.source_name, row.Sample.sample_date, row.Sample.reception_date,
                                    row.Patient.gender , row.Patient.date_of_birth , row.Patient.diagnosis_date , row.Patient.country_of_birth , row.Patient.nationality ,
                                    row.Patient.ethnicity , row.Patient.city_of_residence , row.Patient.nhs , row.Patient.hiv_infection ,
                                    row.Sequence.hcv_wg_pipeline, row.Hospital.name, row.Sample.initial_genotype, row.Sequence.genotype, row.Sequence.subtype,
                                    row.Sequence.genotyping_core, row.Sequence.genotyping_e1, row.Sequence.genotyping_e2, row.Sequence.genotyping_p7,
                                    row.Sequence.genotyping_ns2, row.Sequence.genotyping_ns3, row.Sequence.genotyping_ns4a, row.Sequence.genotyping_ns4b,
                                    row.Sequence.genotyping_ns5a,row.Sequence.genotyping_ns5b])
    print(f"Check report on {file_name} for details")