import os
import re
import argparse
import subprocess
from pathlib import Path

program_specs = argparse.ArgumentParser(
    prog='import_fasta_seqs_to_GLUE.py',
    usage='%(prog)s -input <path to the directory where the raw FASTA files are (i.e zDrive/NGS91/FASTAs)>',
    description='Import NGS sequences from a specified directory to directory sources/ and then transfer them to GLUE')
program_specs.add_argument('-input','-i', help='path to the directory where the FASTQ files ares',required=True)
args = program_specs.parse_args()


path_to_ngs_run = args.input

NGS = re.search(r'NGS[0-9]*.*', path_to_ngs_run) 
ngs_fastas = NGS.group() # NGS91/FASTAs/
ngs_run = re.search(r'^NGS[0-9]*.*[^/FASTAs]', ngs_fastas ) # keep the original name
run_name = ngs_run.group() 
run_name = run_name.replace(' ','_') # to allow the glue commands, it returns an error if spaces are kept
ngs_id = re.search(r'^NGS[0-9]*', run_name ) # use only RUN name 
run_id = ngs_id.group()

path_to_fasta = os.path.join(os.getcwd(),path_to_ngs_run) #/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/zDrive/NGS91/FASTAs/
path_to_hcv_glue_avu = (str(Path(path_to_fasta).parents[2])) #/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/
path_to_sources = os.path.join(path_to_hcv_glue_avu, "sources")

try:
    sources_directory = os.path.join(path_to_sources, f"{run_name}")
    os.mkdir(sources_directory)
    ngs_directory = os.listdir(path_to_ngs_run) # list the files in the directory

    for sequence in ngs_directory:
        fasta_file = os.path.join(path_to_ngs_run,sequence)
        with open(fasta_file,'r') as fasta:
            fasta_name=re.sub(r'^[0-9]*_',"",sequence) # remove first digits from the header
            fasta_name=fasta_name.replace(".fas", "_" + run_id ) 
            final_name=fasta_name.replace(".", "-") # H211900006.2_NGS99 and H211140566.1_NGS96 contained . rather than - (manual modification?)
            file_name = final_name + ".fas"
            source_fasta_file = os.path.join(sources_directory, file_name)
            renamed_fasta_file = open(source_fasta_file,'wt')
            renamed_sequence =""
            for line in fasta:
                if ">" in line: 
                    pass
                else:
                    renamed_sequence += ">"+ final_name +"\n" +line
                    renamed_fasta_file.write(renamed_sequence)
                    renamed_fasta_file.close()
    

    """ CALLING GLUE TO IMPORT NEW FASTA SEQUENCES"""

    glue_commands = f"""
        project hcv_glue_avu
        import source sources/{run_name}
        Q
        exit
        quit
        \
        """
    #project hcv_glue_avu\nimport source sources/NGS93\nQ\nexit\n' in glue console
    p1 = subprocess.run("gluetools.sh" , text=True, input=glue_commands, capture_output=True)

    log_name = os.path.join(path_to_hcv_glue_avu, f'logs/fasta/{run_name}_FASTA_population_log.txt')
    with open( log_name,'w') as log:
        log.write(p1.stdout)
    if p1.returncode == 0:
        print(f"Process successfully performed.\nCheck the report {log_name} for additional information about the sequences imported in GLUE.")
        print(f"The fasta sequences transferred to the hcv_glu_avu project were also stored on {sources_directory}.")
    else:
        print("Something went wrong")


except FileExistsError as err:
    print(err)
    print(f"The subdirectory {run_id} in sources already exists (Check on {path_to_sources}). The fasta sequences belonging to this run may have been imported in the GLUE database previously.")
