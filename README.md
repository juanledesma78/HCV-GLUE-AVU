# HCV GLUE AVU

Deployment of GLUE in the Antiviral Unit to integrate HCV whole genome sequencing and clinical data.

There are two ways for installing GLUE, which can be found on [http://glue-tools.cvr.gla.ac.uk/#/installation](http://glue-tools.cvr.gla.ac.uk/#/installation).

For details on how to use GLUE and get familiar with it visit the official [GLUE documentation](http://glue-tools.cvr.gla.ac.uk/#/home).

## Requirements
- Glue Version 1.1.107
- Java: openjdk version "1.8.0_282", OpenJDK Runtime Environment
- Mysql: Ver 8.0.23-0ubuntu0.20.04.1 for Linux on x86_64 (Ubuntu)
- Blast-2.2.31
- Mafft v7.475
- Raxml version 8.2.12
- Python 3.8

## Steps

1. **BUILDING THE PROJECT**.

    From the terminal run `gluetools.sh` within the main directory *hcv_glue_avu*.
    Once the glue console is displayed run following command line for building the project *hcv_glue_avu*.

    `run file avuHcvProject.glue`

    After completion, exit GLUE by typing in the console either `exit` or `quit` 

2. **ADD NGS SEQUENCES**. 

    From the terminal and within the main directory *hcv_glue_avu*, run the following command
    
    `python3 import_NGSseqs_to_GLUE.py -i <path-to-fasta-sequences-in-zDrive/>`
    
    The fasta sequences are stored in a subdirectory called *FASTAs* for each NGS experiment (i.e. zDrive/NGS91/FASTAs). It is recommended to use ***TAB key*** to complete the argument that takes the path to that folder.

3. **POPULATE METADATA FROM MOLIS**.

    From the terminal and within the main directory *hcv_glue_avu*, run the following command
    
    `python3 populate_metadata_from_molis.py -s <path-to-edited-fasta-sequences-in-sources/>`
    
    Specify the argument for the path to the NGS experiment in *sources/*.


4. **POPULATE METADATA FROM EPI DATABASES**.

    From the terminal and within the main directory *hcv_glue_avu*, run the following command
    
    `python3 add_Epidata_to_Patient_and_Treatment.py`
    
    The script will prompt for the specific NGS experiment to use to retrieve the information.

5. **PERFORM GENOTYPING USING MAXIMUM LIKELIHOOD CLADE ASSIGNMENT**.

    From the terminal and within the main directory *hcv_glue_avu*, run the following command
    
    `python3 genotyping_of_NGS_sequences.py`
    
    The script will prompt for the specific NGS experiment to use perform the analysis.

6. **QUERY GLUE FOR DATA OF A SPECIFIC NGS EXPERIMENT**.

    From the terminal and within the main directory *hcv_glue_avu*, run the following command
    
    `python3 query_sequences_NGS_run.py`
    
    Specify the NGS experiment to query when the prompt is displayed.
    After completion, chek results stored csv files in subdirectory *queries*