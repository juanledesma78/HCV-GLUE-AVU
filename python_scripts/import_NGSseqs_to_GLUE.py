import os, re, sys
import pandas as pd 
import subprocess
path_to_NGS_run  = sys.argv[1] #ngs run, "z:/Antiviral Unit/Sequencing - HCV WGS/"+ NGSrun +"/FASTAs/"
path_to_sources = sys.argv[2]
NGS = re.search(r'NGS[0-9]*.*', path_to_NGS_run) 
NGS_fastas = NGS.group() # NGS91/FASTAs/
ngsRun = re.search(r'^NGS[0-9]*.*[^/FASTAs]', NGS_fastas ) # keep the original name
runName = ngsRun.group() 
runName = runName.replace(' ','_') # to allow the glue commands, error if spaces
NGSid = re.search(r'^NGS[0-9]*', runName ) # use only RUN name 
runID = NGSid.group()

if path_to_sources[-1]!= "/":
    path_to_sources=path_to_sources+"/"
if path_to_NGS_run[-1]!='/':
    path_to_NGS_run= path_to_NGS_run +"/"

path_to_tabular = path_to_sources.replace("sources", "tabular/table_sequence")

#sources_folder = os.mkdir(path_to_sources + str(runName))
os.mkdir(path_to_sources + str(runName))

NGS_directory = os.listdir(path_to_NGS_run) # list the files in the directory

sequenceID =[]
molis_id = []
Pipeline = []
Version = []
for sequence in NGS_directory:
    fasta_file= path_to_NGS_run + sequence
    with open(fasta_file,'r') as fasta:
        fasta_name=re.sub(r'^[0-9]*_',"",sequence) # remove first digits from the header
        fasta_name=fasta_name.replace(".fas", "_" + runID ) # replace .fas with NGS run
        file_name = fasta_name + ".fas"
        renamed_fasta_file = open(path_to_sources + runName +"/"+ file_name,'wt') # fasta_name + ".fas"
        renamed_sequence =""
        for line in fasta:
            
            if ">" in line: 
                pass
            else:
                renamed_sequence += ">"+ fasta_name +"\n" +line
                renamed_fasta_file.write(renamed_sequence)
                renamed_fasta_file.close()
    
        if "PC" not in fasta_name: #fasta_name H210360998-1_NGS91....
            sequenceID.append(fasta_name)
            molis = re.search(r'(^(H|RS)[0-9]*)',  fasta_name)
            molisID = molis.group()
            molis_id.append(molisID)
            if "genomancer" in fasta_name:
                Pipeline.append("Genomacer")
                Version.append("v.1")
            else:
                Pipeline.append("PHE HCV bioinformatics pipeline")
                Version.append("version 1.0")

# create info on pipeline and molis to update on sequence table
run = {"sequenceID" : sequenceID, "MOLIS" : molis_id, "Pipeline": Pipeline, "Version": Version}
ngs_run = pd.DataFrame(data=run)
ngs_run.to_csv(path_to_tabular +"metadata_table_SEQUENCE_"+ runID +".csv", index=False)

#CALLING GLUE TO IMPORT NEW FASTA SEQUENCES
Glue_commands = """\ 
project hcv_glue_avu
import source sources/RUNID
Q
exit\
"""
#project hcv_glue_avu\nimport source sources/NGS93\nQ\nexit\n'
Glue_commands = Glue_commands.replace("RUNID", runName) 
p1 = subprocess.run("gluetools.sh" , text=True, input=Glue_commands)

