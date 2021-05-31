'''Script to change the taxon names in newick file before importing the phylogeny in GLUE.
This is only useful if the phylogeny has been generated using an alternative software to RAXMLsuch as FASTTRE
'''
import pandas as pd
import re
#import sys
#annotation_file = argv[1] # run from main directory 
#newick_file = argv[1]

figAnnotations = pd.read_csv("trees/figtreeAnnotations_UNconstrained_Smith2019.txt", delimiter="\t")
taxon = list(figAnnotations["taxon"])
accession=[]
for row in figAnnotations["genotypeSubtypePrimaryAcc"]:
    row = re.sub(r'^[1-8]/[a-z-?]*/','',row)
    accession.append(row)

annotations = zip(accession, taxon)
dict_annotations =dict(annotations)


#with open("trees/Smith2019_referencePhylogeny_fasttree.nwk",'r') as phylogeny:
with open("trees/Smith2019_phylogeny_rerootedMidpoint_fasttree.txt",'r') as phylogeny:
    fasttree_phylogeny = phylogeny.read()
    for acc,tax in dict_annotations.items():
        if acc in fasttree_phylogeny:
            fasttree_phylogeny = fasttree_phylogeny.replace(acc, tax)
    annotated_file=open("trees/Smith2019_phylogeny_rerootedMidpoint_fasttree_annotated.nwk", "wt")
    annotated_file.write(fasttree_phylogeny)
    annotated_file.close()
