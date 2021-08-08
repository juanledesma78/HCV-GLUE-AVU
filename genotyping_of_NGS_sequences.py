import subprocess,re 
NGSId = input("This program will take a batch of sequences from a NGS experiment and will perform a genetic classifciation using Maximum Likelihood Clade Assignment method developed in GLUE.\nPlease specify the NGS of interest by typing NGS and number for the experiment (i.e. NGS1978)\n").upper()

with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/genotyping_by_genes.js",'r') as program:
    default_lines = program.read()
    update = re.sub("source.name like '[A-Z0-9]*%'","source.name like '" + NGSId + "%'",default_lines)
    program.close()

with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/glue/genotyping_by_genes.js",'w') as program:
    program.write(update)
    program.close()

GLUE_commnads ="""
project hcv_glue_avu
run script glue/genotyping_by_genes.js
exit
quit
\
"""

genotype_sequences = subprocess.run("gluetools.sh", text = True, input= GLUE_commnads)


if genotype_sequences.returncode == 0:
    print("\nGenotyping completed.\nCheck results.\n")
else:
    print("\nSomething went wrong")