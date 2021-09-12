import os
import re
import argparse
import pandas as pd 
import subprocess

program_specs = argparse.ArgumentParser(
    prog='import_NGSseqs_to_GLUE.py',
    usage='%(prog)s -input path-to-raw-NGSrun',
    description='Import NGS sequences from a specified directory to sources directory and then transfer them to GLUE')
program_specs.add_argument('-input','-i', help='path to the directory where the FASTQ files ares',required=True)
args = program_specs.parse_args()


path_to_ngs_run = args.input
print(path_to_ngs_run)

#path_to_NGS_run  = sys.argv[1] #select the NGS run to import "/FASTAs/"
path_to_sources = "/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/sources/"
NGS = re.search(r'NGS[0-9]*.*', path_to_ngs_run) 
ngs_fastas = NGS.group() # NGS91/FASTAs/
ngs_run = re.search(r'^NGS[0-9]*.*[^/FASTAs]', ngs_fastas ) # keep the original name
run_name = ngs_run.group() 
run_name = run_name.replace(' ','_') # to allow the glue commands, error if spaces
ngs_id = re.search(r'^NGS[0-9]*', run_name ) # use only RUN name 
run_id = ngs_id.group()

#if path_to_NGS_run[-1]!='/':
#    path_to_NGS_run= path_to_NGS_run +"/"
#os.mkdir(path_to_sources + str(runName)) #sources_folder = os.mkdir(path_to_sources + str(runName)), not needed to assign a variable

#this substitute the code above
sources_directory = os.path.join(path_to_sources,run_name)
os.mkdir(sources_directory) #os.mkdir(os.path.join(path_to_sources,runName))

ngs_directory = os.listdir(path_to_ngs_run) # list the files in the directory


for sequence in ngs_directory:
    fasta_file = os.path.join(path_to_ngs_run,sequence)
    with open(fasta_file,'r') as fasta:
        fasta_name=re.sub(r'^[0-9]*_',"",sequence) # remove first digits from the header
        fasta_name=fasta_name.replace(".fas", "_" + run_id ) 
        final_name=fasta_name.replace(".", "-") # H211900006.2_NGS99 and H211140566.1_NGS96it contained . rather than - (manual modification?)
        file_name = final_name + ".fas"
        #renamed_fasta_file = open(path_to_sources + runName +"/"+ file_name,'wt') # final_name + ".fas"
        source_fasta_file = os.path.join(path_to_sources,run_name, file_name)
        renamed_fasta_file = open(source_fasta_file,'wt')
        renamed_sequence =""
        for line in fasta:
            if ">" in line: 
                pass
            else:
                renamed_sequence += ">"+ final_name +"\n" +line
                renamed_fasta_file.write(renamed_sequence)
                renamed_fasta_file.close()
    

#CALLING GLUE TO IMPORT NEW FASTA SEQUENCES python 3.8
glue_commands = """
    project hcv_glue_avu
    import source sources/RUNID
    Q
    exit
    quit
    \
    """
#project hcv_glue_avu\nimport source sources/NGS93\nQ\nexit\n'
glue_commands = glue_commands.replace("RUNID", run_name) 
p1 = subprocess.run("gluetools.sh" , text=True, input=glue_commands)

if p1.returncode == 0:
    print("\nSequences successfully imported in GLUE\n")
else:
    print("\nSomething went wrong")

