import os, sys, re
folder =sys.argv[1]
destination =sys.argv[2]
sources = os.listdir(folder)

if folder[-1] != "/" and destination[-1] != "/":
    folder += '/'
    destination +='/'

for sequence in sources:
    if "PC" not in sequence:
        fasta_file= folder + sequence
        with open(fasta_file,'r') as fasta:
            name=re.sub(r'^[0-9]*_',"",re.sub(r'-[0-9]',"",sequence))

            file_name = destination + name 
            #file_name = folder+'/'+ name 
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