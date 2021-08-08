import subprocess
import pandas as pd

query = """
project hcv_glue_avu
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/recombinant_genotyping_results_GENES.csv
list sequence --whereClause "reference_status ='recombinant'" sequenceID  genotyping_core genotyping_e1 genotyping_e2 genotyping_p7 genotyping_ns2 genotyping_ns3 genotyping_ns4a genotyping_ns4b genotyping_ns5a genotyping_ns5b
Q
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/recombinant_genotyping_results_POLYPROTEIN.csv
list sequence --whereClause "reference_status ='recombinant'" sequenceID  genotyping_polyprotein
Q
exit
quit
\
"""

glueCalling = subprocess.run("gluetools.sh", text= True, input= query )

pathToFile = "/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/"
genotypingByGenes = pd.read_csv(pathToFile + "tmp/recombinant_genotyping_results_GENES.csv")
genotypingPrecursorPolyprotein = pd.read_csv(pathToFile + "tmp/recombinant_genotyping_results_POLYPROTEIN.csv")

genotypingByGenes.rename(columns={'sequenceID':'sequence id', 'genotyping_core':'Genotyping CORE','genotyping_e1':'Genotyping E1','genotyping_e2':'Genotyping E2' ,'genotyping_p7':'Genotyping P7','genotyping_ns2':'Genotyping NS2','genotyping_ns3':'Genotyping NS3'	,'genotyping_ns4a'	:'Genotyping NS4A','genotyping_ns4b':'Genotyping NS4B','genotyping_ns5a':'Genotyping NS5A'	,'genotyping_ns5b':'Genotyping NS5B'} ,inplace=True)
genotypingPrecursorPolyprotein.rename(columns={'sequenceID':'sequence id', 'genotyping_polyprotein':'Genotyping Precursor Polyprotein'} ,inplace=True)

recombinantResult = pd.merge(left = genotypingPrecursorPolyprotein, right = genotypingByGenes, how = "left" , left_on= 'sequence id', right_on='sequence id')
recombinantResult.to_csv(pathToFile + "recombinant_genotyping_results.csv" ,index=False)

