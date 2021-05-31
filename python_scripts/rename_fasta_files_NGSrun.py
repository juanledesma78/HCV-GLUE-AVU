import os, re, sys 
origin_path  = sys.argv[1] #ngs run
destination_path = sys.argv[2] #ngs run
origin_folder = re.search(r'NGS[0-9]*.*', origin_path)
destination_folder = origin_folder.group()
destination_directory = os.mkdir(destination_path+"/"+str(destination_folder))
ngsRun = re.search(r'^NGS[0-9]*', destination_folder )
runName = ngsRun.group()

#+ NGSrun +"/"
# NGSrun=input("Specify the run name: ")
# at the moment, the fasta files are in the Z drive and the folder sources of GLUE in Desktop
#origin_path = "z:/Antiviral Unit/Sequencing - HCV WGS/"+ NGSrun +"/FASTAs/"
origin_directory = os.listdir(origin_path)
#include something to double check the folder already exists
for sequence in origin_directory:
    if "PC" not in sequence:
        fasta_file= origin_path +"/" +sequence
        with open(fasta_file,'r') as fasta:
            #name=re.sub(r'^[0-9]*_',"",re.sub(r'-[0-9]',"",sequence))
            fasta_name=re.sub(r'^[0-9]*_',"",sequence)
            fasta_name=fasta_name.replace(".fas", "_"+runName)
            file_name = "/"+ fasta_name + ".fas"
            renamed_fasta_file = open(destination_path+"/"+destination_folder +"/"+ file_name,'wt')
            renamed_sequence =""
            
            for line in fasta:
                if ">" in line:
                    pass
                else:
                    
                    renamed_sequence += ">"+ fasta_name +"\n" +line
                    renamed_fasta_file.write(renamed_sequence)
                    renamed_fasta_file.close()








