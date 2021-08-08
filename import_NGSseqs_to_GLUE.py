import os, re, sys
import pandas as pd 
import subprocess
path_to_NGS_run  = sys.argv[1] #select the NGS run to import "/FASTAs/"
path_to_sources = "/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/sources/"
NGS = re.search(r'NGS[0-9]*.*', path_to_NGS_run) 
NGS_fastas = NGS.group() # NGS91/FASTAs/
ngsRun = re.search(r'^NGS[0-9]*.*[^/FASTAs]', NGS_fastas ) # keep the original name
runName = ngsRun.group() 
runName = runName.replace(' ','_') # to allow the glue commands, error if spaces
NGSid = re.search(r'^NGS[0-9]*', runName ) # use only RUN name 
runID = NGSid.group()

if path_to_NGS_run[-1]!='/':
    path_to_NGS_run= path_to_NGS_run +"/"

os.mkdir(path_to_sources + str(runName)) #sources_folder = os.mkdir(path_to_sources + str(runName)), not needed to assign a variable

NGS_directory = os.listdir(path_to_NGS_run) # list the files in the directory

for sequence in NGS_directory:
    fasta_file= path_to_NGS_run + sequence
    with open(fasta_file,'r') as fasta:
        fasta_name=re.sub(r'^[0-9]*_',"",sequence) # remove first digits from the header
        fasta_name=fasta_name.replace(".fas", "_" + runID ) # replace .fas with NGS run
        final_name=fasta_name.replace(".", "-") # H211900006.2_NGS99 and H211140566.1_NGS96it contained . rather than - (manual modification?)
        file_name = final_name + ".fas"
        renamed_fasta_file = open(path_to_sources + runName +"/"+ file_name,'wt') # final_name + ".fas"
        renamed_sequence =""
        for line in fasta:
            if ">" in line: 
                pass
            else:
                renamed_sequence += ">"+ final_name +"\n" +line
                renamed_fasta_file.write(renamed_sequence)
                renamed_fasta_file.close()
    

#CALLING GLUE TO IMPORT NEW FASTA SEQUENCES python 3.8
Glue_commands = """
project hcv_glue_avu
import source sources/RUNID
Q
exit
quit
\
"""
#project hcv_glue_avu\nimport source sources/NGS93\nQ\nexit\n'
Glue_commands = Glue_commands.replace("RUNID", runName) 
p1 = subprocess.run("gluetools.sh" , text=True, input=Glue_commands)

if p1.returncode == 0:
    print("\nSequences successfully imported in GLUE\n")
else:
    print("\nSomething went wrong")
