import os, re
NGSrun=input("Specify the run name: ")
# at the moment, the fasta files are in the Z drive and the folder sources of GLUE in Desktop
origin_path = "z:/Antiviral Unit/Sequencing - HCV WGS/"+ NGSrun +"/FASTAs/"
origin_directory = os.listdir(origin_path)
#include something to double check the folder already exists
destination_path = "c:/Users/juan.ledesma/Desktop/HCV_GLUE_AVU/sources/"+ NGSrun +"/"
destination_directory = os.mkdir(destination_path)

for sequence in origin_directory:
    if "PC" not in sequence:
        fasta_file= origin_path + sequence
        with open(fasta_file,'r') as fasta:
            #name=re.sub(r'^[0-9]*_',"",re.sub(r'-[0-9]',"",sequence))
            name=re.sub(r'^[0-9]*_',"",sequence)
            file_name = destination_path + name 
            renamed_fasta_file = open(file_name,'wt')
            renamed_sequence =""
            
            for line in fasta:
                if ">" in line:
                    pass
                else:
                    header =name.replace(".fas", "")
                    renamed_sequence += ">"+ header +"\n" +line
                    renamed_fasta_file.write(renamed_sequence)
                    renamed_fasta_file.close()