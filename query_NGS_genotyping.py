import subprocess
import pandas as pd

query = """
project hcv_glue_avu
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/NGS_genotyping_results_GENES.csv
list sequence --whereClause "source.name like 'NGS%' and sequenceID not like 'PC%'" sequenceID  genotyping_core genotyping_e1 genotyping_e2 genotyping_p7 genotyping_ns2 genotyping_ns3 genotyping_ns4a genotyping_ns4b genotyping_ns5a genotyping_ns5b
Q
console set cmd-output-file-format csv
console set next-cmd-output-file queries/tmp/NGS_genotyping_results_GenotypeSubtype.csv
list sequence --whereClause "source.name like 'NGS%' and sequenceID not like 'PC%'" sequenceID  genotype subtype
Q
exit
quit
\
"""

glueCalling = subprocess.run("gluetools.sh", text= True, input= query )

pathToFile = "/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/queries/"
genotypingByGenes = pd.read_csv(pathToFile + "tmp/NGS_genotyping_results_GENES.csv")
genotypingPrecursorPolyprotein = pd.read_csv(pathToFile + "tmp/NGS_genotyping_results_GenotypeSubtype.csv")

genotypingByGenes.rename(columns={'sequenceID':'sequence id', 'genotyping_core':'Genotyping CORE','genotyping_e1':'Genotyping E1','genotyping_e2':'Genotyping E2' ,'genotyping_p7':'Genotyping P7','genotyping_ns2':'Genotyping NS2','genotyping_ns3':'Genotyping NS3'	,'genotyping_ns4a'	:'Genotyping NS4A','genotyping_ns4b':'Genotyping NS4B','genotyping_ns5a':'Genotyping NS5A'	,'genotyping_ns5b':'Genotyping NS5B'} ,inplace=True)
genotypingPrecursorPolyprotein.rename(columns={'sequenceID':'sequence id'} ,inplace=True)

recombinantResult = pd.merge(left = genotypingPrecursorPolyprotein, right = genotypingByGenes, how = "left" , left_on= 'sequence id', right_on='sequence id')
recombinantResult.to_csv(pathToFile + "NGSsequences_genotyping_results.csv" ,index=False)

