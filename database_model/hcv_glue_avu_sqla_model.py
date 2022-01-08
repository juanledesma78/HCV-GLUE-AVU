from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey,  Index, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT, BIT, LONGBLOB, DATE 
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql.schema import ForeignKeyConstraint

""" ESTABLISH CONNECTION TO THE DATABASE AND CREATING THE SESSION TO HANDLE IT"""

engine = create_engine('mysql+pymysql://gluetools:glue12345@localhost/GLUE_TOOLS', echo=True, future=True)  
Session = sessionmaker(bind=engine)
session = Session() 

""" DECLARATIVE MAPPING"""

Base = declarative_base()

class AlignedSegment(Base): 
    __tablename__='hcv_glue_avu_aligned_segment'
    __table_args__ = (
        Index('source_name','source_name', 'sequence_id', 'alignment_name'), 
        ForeignKeyConstraint(['source_name','sequence_id','alignment_name'],
        ['hcv_glue_avu_alignment_member.source_name', 'hcv_glue_avu_alignment_member.sequence_id','hcv_glue_avu_alignment_member.alignment_name'])
        ,)

    alignment_name = Column(String(50), nullable=False, primary_key=True)
    member_end = Column(Integer, nullable=False, primary_key=True)
    member_start = Column(Integer, nullable=False, primary_key=True)
    ref_end = Column(Integer, nullable=False, primary_key=True)
    ref_start = Column(Integer, nullable=False, primary_key=True)
    sequence_id = Column(String(50), nullable=False, primary_key=True)  
    source_name = Column(String(50), nullable=False, primary_key=True)
    alignment_member = relationship('AlignmentMember', back_populates='aligned_segments')


class Alignment(Base):
    __tablename__='hcv_glue_avu_alignment'
    __table_args_ = (Index('parent_name', 'parent_name'),Index('ref_seq_name', 'ref_seq_name') ) 

    description = Column(String(1000), nullable=True)
    display_name = Column(String(100), nullable=True)
    name = Column(String(50), nullable=False, primary_key=True)
    parent_name = Column(String(50), ForeignKey('hcv_glue_avu_alignment.name'), nullable=True)
    ref_seq_name = Column(String(50), ForeignKey('hcv_glue_avu_reference_sequence.name'), nullable=True)
    phylogeny = Column(String(10000), nullable=True)
    alignment = relationship("Alignment") # Adjacent
    alignment_members = relationship("AlignmentMember", back_populates="alignment")
    reference_sequence = relationship("ReferenceSequence", back_populates="alignments")
    var_almt_notes = relationship("VarAlmtNote", back_populates="alignment")


class AlignmentMember(Base): 
    __tablename__='hcv_glue_avu_alignment_member'
    __table_args__ = (
        ForeignKeyConstraint(['alignment_name'], ['hcv_glue_avu_alignment.name'] ), 
        Index('source_name', 'source_name', 'sequence_id'),
        ForeignKeyConstraint(['source_name', 'sequence_id'],
        ['hcv_glue_avu_sequence.source_name', 'hcv_glue_avu_sequence.sequence_id'])
                    ,)

    alignment_name = Column(String(50), nullable=False, primary_key=True) 
    reference_member = Column(BIT, nullable=False)
    sequence_id = Column(String(50), nullable=False, primary_key=True)   
    source_name = Column(String(50), nullable=False, primary_key=True) 
    alignment = relationship("Alignment", back_populates="alignment_members")
    aligned_segments = relationship('AlignedSegment', back_populates='alignment_member')
    sequence = relationship("Sequence", back_populates="alignment_members")
    

class Feature(Base):
    __tablename__='hcv_glue_avu_feature'
    __table_args__ =(Index('parent_name', 'parent_name'),) 

    description = Column(String(1000), nullable=True)
    display_name = Column(String(100), nullable=True)
    name = Column(String(50), nullable=False, primary_key=True)
    parent_name = Column(String(50), ForeignKey('hcv_glue_avu_feature.name'), nullable=True)
    features = relationship("Feature")
    feature_locations = relationship("FeatureLocation", back_populates="feature")
    feature_metatags = relationship("FeatureMetatag", back_populates="feature") 


class FeatureLocation(Base):
    __tablename__='hcv_glue_avu_feature_location'
    
    feature_name = Column(String(50), ForeignKey('hcv_glue_avu_feature.name'), nullable=False, primary_key=True)
    ref_seq_name = Column(String(50), ForeignKey('hcv_glue_avu_reference_sequence.name'), nullable=False, primary_key=True)
    feature = relationship("Feature", back_populates="feature_locations")
    reference_sequence = relationship("ReferenceSequence", back_populates="feature_locations")
    feature_segments = relationship("FeatureSegment", back_populates="feature_location") 
    member_floc_notes = relationship("MemberFlocNote", back_populates="feature_location") 
    variations = relationship("Variation", back_populates="feature_location") 
    

class FeatureMetatag(Base):
    __tablename__='hcv_glue_avu_feature_metatag'
    
    feature_name = Column(String(50), ForeignKey('hcv_glue_avu_feature.name'), nullable=False, primary_key=True)
    name = Column(String(50), nullable=False, primary_key=True)
    value =  Column(String(50), nullable=True)
    feature = relationship("Feature", back_populates="feature_metatags")


class FeatureSegment(Base): 
    __tablename__='hcv_glue_avu_feature_segment'
    __table_args__ = (
        Index('ref_seq_name' , 'ref_seq_name', 'feature_name'),
        ForeignKeyConstraint(['ref_seq_name', 'feature_name'],
        ['hcv_glue_avu_feature_location.ref_seq_name', 'hcv_glue_avu_feature_location.feature_name'])
        ,)

    feature_name = Column(String(50), nullable=False, primary_key=True) 
    ref_end = Column(Integer, nullable=False, primary_key=True)
    ref_seq_name = Column(String(50), nullable=False, primary_key=True) 
    ref_start = Column(Integer, nullable=False, primary_key=True)
    splice_index = Column(Integer, nullable=False)
    transcription_index = Column(Integer, nullable=False)
    translation_modifier_name = Column(String(100), nullable=True)
    feature_location = relationship("FeatureLocation", back_populates= "feature_segments")
    

class MemberFlocNote(Base): 
    __tablename__='hcv_glue_avu_member_floc_note'
    __table_args__= (
        Index('ref_seq_name','ref_seq_name', 'feature_name'), 
        ForeignKeyConstraint(['ref_seq_name', 'feature_name'],
        ['hcv_glue_avu_feature_location.ref_seq_name', 'hcv_glue_avu_feature_location.feature_name' ])
        ,) 

    alignment_name = Column(String(50), nullable=False, primary_key=True)
    feature_name = Column(String(50), nullable=False, primary_key=True)
    ref_seq_name = Column(String(50), nullable=False, primary_key=True)
    sequence_id = Column(String(50), nullable=False, primary_key=True)
    source_name = Column(String(50), nullable=False, primary_key=True)
    feature_location = relationship("FeatureLocation", back_populates="member_floc_notes")


class Module(Base):
    __tablename__='hcv_glue_avu_module'

    config = Column(LONGBLOB , nullable=False) 
    description = Column(String(1000), nullable=True)
    name = Column(String(50), nullable=False, primary_key=True)
    module_resources = relationship("ModuleResource",back_populates="module")


class ModuleResource(Base):
    __tablename__='hcv_glue_avu_module_resource'

    content = Column(LONGBLOB , nullable=True) 
    module_name = Column(String(50), ForeignKey('hcv_glue_avu_module.name'), nullable=False, primary_key=True)
    name = Column(String(200), nullable=False, primary_key=True)
    module = relationship("Module", back_populates="module_resources")


class ProjectSetting(Base):
    __tablename__='hcv_glue_avu_project_setting'

    name = Column(String(50), nullable=False, primary_key=True)
    value = Column(String(200), nullable=True)


class ReferenceSequence(Base):
    __tablename__='hcv_glue_avu_reference_sequence'
    __table_args__= (
        Index('source_name', 'source_name', 'sequence_id'),
        ForeignKeyConstraint(['source_name', 'sequence_id'],
        ['hcv_glue_avu_sequence.source_name', 'hcv_glue_avu_sequence.sequence_id'])
        ,) 

    creation_time = Column(BIGINT, nullable=False)
    description = Column(String(1000), nullable=True)
    display_name = Column(String(100), nullable=True)
    name = Column(String(50), nullable=False, primary_key=True)
    sequence_id = Column(String(50), nullable=False)
    source_name = Column(String(50), nullable=False)
    alignments = relationship("Alignment", back_populates="reference_sequence")
    feature_locations = relationship("FeatureLocation", back_populates="reference_sequence")
    sequence = relationship("Sequence", back_populates="reference_sequences")


class SeqOriData(Base):
    __tablename__='hcv_glue_avu_seq_orig_data'
    __table_args__ = (
        Index('source_name', 'source_name', 'sequence_id'),
        ForeignKeyConstraint(['source_name', 'sequence_id'],
        ['hcv_glue_avu_sequence.source_name', 'hcv_glue_avu_sequence.sequence_id'])
            ,)

    packed_data = Column(LONGBLOB, nullable=False) 
    sequence_id = Column(String(50), nullable=False, primary_key=True)
    source_name = Column(String(50), nullable=False, primary_key=True)
    sequence = relationship("Sequence", back_populates="seqs_ori_data")


class Sequence(Base): 
    __tablename__='hcv_glue_avu_sequence'
    __table_args__ = (Index('source_name', 'source_name'), 
            Index('who_country_id', 'who_country_id'),
            Index('sample_id', 'sample_id') )

    format = Column(String(50), nullable=False)
    sequence_id = Column(String(50), nullable=False, primary_key=True)
    source_name = Column(String(50), ForeignKey('hcv_glue_avu_source.name'), nullable=False, primary_key=True)
    gb_gi_number = Column(String(50), nullable=True)
    gb_primary_accession = Column(String(50), nullable=True)
    gb_accession_version = Column(String(50), nullable=True)
    gb_locus = Column(String(50), nullable=True)
    gb_length = Column(Integer, nullable=True)
    gb_recombinant = Column(BIT, nullable=True) 
    gb_organism = Column(String(50), nullable=True)
    gb_isolate = Column(String(300), nullable=True)
    gb_taxonomy = Column(String(200), nullable=True)
    gb_host = Column(String(50), nullable=True)
    gb_pubmed_id = Column(String(50), nullable=True)
    gb_country = Column(String(50), nullable=True)
    gb_place_sampled = Column(String(200), nullable=True)
    gb_collection_year = Column(Integer, nullable=True)
    gb_collection_month = Column(String(50), nullable=True)
    gb_collection_month_day = Column(Integer, nullable=True)
    gb_create_date = Column(DATE, nullable=True) 
    gb_update_date = Column(DATE, nullable=True) 
    gb_genotype = Column(String(50), nullable=True)
    gb_subtype = Column(String(50), nullable=True)
    earliest_collection_year = Column(Integer, nullable=True)
    latest_collection_year = Column(Integer, nullable=True)
    genotype = Column(String(50), nullable=True)
    subtype = Column(String(50), nullable=True)
    genotyping_method = Column(String(200), nullable=True)
    reference_status = Column(String(20), nullable=True)
    gb_lab_construct = Column(BIT, nullable=True) 
    who_country_id = Column(String(50), ForeignKey('hcv_glue_avu_who_country.id'), nullable=True)
    hcv_wg_pipeline = Column(String(100), nullable=True)
    pipeline_version = Column(String(50), nullable=True)
    sample_id = Column(String(50), ForeignKey('hcv_glue_avu_sample.id'), nullable=True) 
    # genotyping using polyprotein and single genes
    genotyping_polyprotein = Column(String(50),nullable=True)
    genotyping_core = Column(String(50),nullable=True)
    genotyping_e1 = Column(String(50),nullable=True)
    genotyping_e2 = Column(String(50),nullable=True)
    genotyping_p7 = Column(String(50),nullable=True)
    genotyping_ns2 = Column(String(50),nullable=True)
    genotyping_ns3 = Column(String(50),nullable=True)
    genotyping_ns4a = Column(String(50),nullable=True)
    genotyping_ns4b = Column(String(50),nullable=True)
    genotyping_ns5a = Column(String(50),nullable=True)
    genotyping_ns5b = Column(String(50),nullable=True)
    alignment_members = relationship("AlignmentMember", back_populates="sequence")
    reference_sequences = relationship("ReferenceSequence", back_populates="sequence")
    seqs_ori_data = relationship("SeqOriData", back_populates="sequence")
    source = relationship("Source", back_populates="sequences")
    sample = relationship("Sample", back_populates="sequences")
    country = relationship("WhoCountry", back_populates="sequences")


class Source(Base):
    __tablename__='hcv_glue_avu_source'

    name = Column(String(50), nullable=False, primary_key=True)
    sequences = relationship("Sequence", back_populates="source")


class VarAlmtNote(Base):
    __tablename__='hcv_glue_avu_var_almt_note'
    __table_args__ = (
        Index('ref_seq_name', 'ref_seq_name','feature_name' , 'variation_name'),
        ForeignKeyConstraint(['alignment_name'],['hcv_glue_avu_alignment.name']),
        ForeignKeyConstraint(['ref_seq_name','feature_name' , 'variation_name'], 
        ['hcv_glue_avu_variation.ref_seq_name','hcv_glue_avu_variation.feature_name','hcv_glue_avu_variation.name'])
        ,)

    alignment_name = Column(String(50), nullable=False, primary_key=True)   
    feature_name = Column(String(50), nullable=False, primary_key=True)     
    ref_seq_name = Column(String(50), nullable=False, primary_key=True)     
    variation_name = Column(String(50), nullable=False, primary_key=True)   
    alignment = relationship("Alignment", back_populates="var_almt_notes")
    variation = relationship("Variation", back_populates="var_almt_notes")

class Variation(Base):
    __tablename__='hcv_glue_avu_variation'
    __table_args__=(
        Index('ref_seq_name', 'ref_seq_name', 'feature_name'),
        ForeignKeyConstraint(['ref_seq_name', 'feature_name'],
        ['hcv_glue_avu_feature_location.ref_seq_name', 'hcv_glue_avu_feature_location.feature_name' ])
        ,)

    description = Column(String(1000), nullable=True)
    display_name = Column(String(100), nullable=True)
    feature_name = Column(String(50), nullable=False, primary_key=True)
    name = Column(String(50), nullable=False, primary_key=True)
    ref_end = Column(Integer, nullable=True)
    ref_seq_name = Column(String(50), nullable=False, primary_key=True)
    ref_start = Column(Integer, nullable=True)
    type = Column(String(50), nullable=False)
    var_almt_notes = relationship("VarAlmtNote", back_populates="variation")
    feature_location = relationship("FeatureLocation", back_populates="variations")


class VariationMetatag(Base):
    __tablename__='hcv_glue_avu_variation_metatag'

    feature_name = Column(String(50), nullable=False, primary_key=True)
    metatag_name = Column(String(50), nullable=False, primary_key=True)
    metatag_value = Column(String(50), nullable=True)
    ref_seq_name = Column(String(50), nullable=False, primary_key=True)
    variation_name = Column(String(50), nullable=False, primary_key=True)

# CUSTOM TABLES

class WhoCountry(Base):
    __tablename__='hcv_glue_avu_who_country'
    
    id = Column(String(50), nullable=False, primary_key=True)
    m49_code = Column(Integer, nullable=True)
    display_name = Column(String(100), nullable=True)
    full_name = Column(String(100), nullable=True)
    is_ldc = Column(BIT, nullable=True) # bit
    is_lldc = Column(BIT, nullable=True) # bit
    is_sids = Column(BIT, nullable=True) # bit
    development_status = Column(String(20), nullable=True)
    who_region_id = Column(String(50), ForeignKey('hcv_glue_avu_who_region.id'), nullable=True)
    who_sub_region_id = Column(String(50), ForeignKey('hcv_glue_avu_who_sub_region.id'),nullable=True)
    who_intermediate_region_id = Column(String(50), ForeignKey('hcv_glue_avu_who_intermediate_region.id'), nullable=True)
    sequences = relationship("Sequence", back_populates="country")
    region = relationship("WhoRegion", back_populates="countries")
    sub_region = relationship("WhoSubRegion", back_populates="countries")
    intermediate_region = relationship("WhoIntermediateRegion", back_populates="countries")


class WhoIntermediateRegion(Base):
    __tablename__='hcv_glue_avu_who_intermediate_region'
    
    id = Column(String(50), nullable=False, primary_key=True)
    m49_code = Column(Integer, nullable=True)
    display_name = Column(String(100), nullable=True)
    who_sub_region_id = Column(String(50), nullable=True)
    countries = relationship("WhoCountry", back_populates="intermediate_region")


class WhoRegion(Base):
    __tablename__='hcv_glue_avu_who_region'

    id = Column(String(50), nullable=False, primary_key=True)
    m49_code = Column(Integer, nullable=True)
    display_name = Column(String(100), nullable=True)
    countries = relationship("WhoCountry", back_populates="region")
    


class WhoSubRegion(Base):
    __tablename__='hcv_glue_avu_who_sub_region'

    id = Column(String(50), nullable=False, primary_key=True)
    m49_code = Column(Integer, nullable=True)
    display_name = Column(String(100), nullable=True)
    who_region_id = Column(String(50), nullable=True)
    countries = relationship("WhoCountry", back_populates="sub_region")


# AVU TABLES 

class Sample(Base):
    __tablename__='hcv_glue_avu_sample'
    
    id = Column(String(50), nullable=False, primary_key=True)
    sample_date = Column(DATE, nullable=True) 
    reception_date = Column(DATE, nullable=True) 
    initial_genotype = Column(String(50), nullable=True)
    patient_id = Column(String(50), ForeignKey('hcv_glue_avu_patient.id'),  nullable=False)
    hospital_id = Column(String(50), ForeignKey('hcv_glue_avu_hospital.id'),nullable=False )
    patient = relationship("Patient", back_populates="samples")
    sequences = relationship("Sequence", back_populates="sample")
    hospital = relationship("Hospital", back_populates="samples")


class Patient(Base):
    __tablename__='hcv_glue_avu_patient'

    id = Column(String(50), nullable=False, primary_key=True) # number or string? dependns of final decision
    date_of_birth = Column(DATE, nullable=True) 
    diagnosis_date = Column(DATE, nullable=True) 
    country_of_birth = Column(String(50), nullable=True)
    nationality = Column(String(50), nullable=True)
    ethnicity = Column(String(50), nullable=True)
    city_of_residence = Column(String(50), nullable=True)
    nhs = Column(Integer, nullable=True) # it was integer but pandas changes to float when NaN 
    gender = Column(String(50), nullable=True)
    hiv_infection = Column(String(50), nullable=True)
    samples = relationship("Sample", back_populates="patient")
    treatments =relationship("Treatment", back_populates="patient") 

class Hospital(Base):
    __tablename__='hcv_glue_avu_hospital'
    
    id = Column(String(50), nullable=False, primary_key=True)
    name = Column(String(50), nullable=True)
    samples = relationship("Sample", back_populates="hospital")


class Treatment(Base):
    __tablename__='hcv_glue_avu_treatment' # association table, many to many with patient
    __table_args__=(UniqueConstraint('patient_id', 'drug_id', 'regime','treatment_date' ),)
    
    id = Column(Integer, nullable=False, primary_key=True) # autoincrement by default
    patient_id = Column(String(50), ForeignKey('hcv_glue_avu_patient.id'),  nullable=False )
    drug_id = Column(String(50), ForeignKey('hcv_glue_avu_drug.id'),  nullable=False )
    regime = Column(String(100),nullable=True)
    treatment_date = Column(DATE,nullable=True)
    patient =relationship("Patient", back_populates="treatments") 
    drug =relationship("Drug", back_populates="treatments") 


class Drug(Base):
    __tablename__='hcv_glue_avu_drug'

    id = Column(String(50), nullable=False, primary_key=True)
    manufacturer = Column(String(50), nullable=True)
    therapy_class = Column(String(50), nullable=True)
    treatments = relationship("Treatment", back_populates='drug')


Base.metadata.create_all(engine)

