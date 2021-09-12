'''Script to change the taxon names in newick file before importing the phylogeny in GLUE.
This is only useful if the phylogeny has been generated using an alternative software to RAXMLsuch as FASTTRE
'''
import pandas as pd
import re

fig_annotations = pd.read_csv("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/trees/figtreeAnnotations_UNconstrained_Smith2019.txt", delimiter="\t")
taxon = list(fig_annotations["taxon"])
accession=[]
for row in fig_annotations["genotypeSubtypePrimaryAcc"]:
    row = re.sub(r'^[1-8]/[a-z-?]*/','',row)
    accession.append(row)

annotations = zip(accession, taxon)
dict_annotations =dict(annotations)


with open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/trees/Smith2019_phylogeny_rerootedMidpoint_fasttree.txt",'r') as phylogeny:
    fasttree_phylogeny = phylogeny.read()
    for acc,tax in dict_annotations.items():
        if acc in fasttree_phylogeny:
            fasttree_phylogeny = fasttree_phylogeny.replace(acc, tax)
    annotated_file=open("/home/phe.gov.uk/juan.ledesma/gluetools/projects/hcv_glue_avu/trees/Smith2019_phylogeny_rerootedMidpoint_fasttree_annotated.nwk", "wt")
    annotated_file.write(fasttree_phylogeny)
    annotated_file.close()
