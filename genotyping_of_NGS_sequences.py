import subprocess
import re
import os
import argparse

program_specs = argparse.ArgumentParser(
    prog='genotyping_of_NGS_sequences.py',
    usage='%(prog)s -run <path to the specific NGS run in directory sources (i.e. sources/NGS91)>',
    description='The script %(prog)s calls GLUE to invoke a JavaScript program which perfoms the genotyping of all the sequences from a specific NGS run')
program_specs.add_argument('-run', help='path to the sepecific folder in sources/ where the fasta sequences to be genotyped are',required=True)
args = program_specs.parse_args()

path_to_hcv_glue_avu = os.getcwd()
path_to_sources = os.path.join(os.getcwd(), args.run)
ngs_run = os.path.basename(os.path.normpath(path_to_sources)) 


with open(os.path.join(path_to_hcv_glue_avu, 'glue/genotyping_by_genes.js'),'r') as program:
    default_lines = program.read()
    update = re.sub("source.name like '[A-Z0-9]*.*%'",f"source.name like '{ngs_run}%'",default_lines)
    program.close()

with open(os.path.join(path_to_hcv_glue_avu, 'glue/genotyping_by_genes.js'),'w') as program:
    program.write(update)
    program.close()

glue_commnads ="""
project hcv_glue_avu
run script glue/genotyping_by_genes.js
exit
quit
\
"""
print(f"""
Maximum likelihood clade assignment in process. 
The analysis can take a while depends on the number of sequences to genotype. 
Please wait until the analysis for the run {ngs_run} is completed.
""")
genotype_sequences = subprocess.run("gluetools.sh", text = True, input= glue_commnads, capture_output=True)

log_name = os.path.join(path_to_hcv_glue_avu, f'logs/genotyping/{ngs_run}_genotyping_MLCA_log.txt')
with open( log_name,'w') as log:
    log.write(genotype_sequences.stdout)
if genotype_sequences.returncode == 0:
    print(f"Process completed.\nCheck the report {log_name} for additional information about genotyping by maximum likelihood clade assignment (MLCA)")
else:
    print("Something went wrong")
  
