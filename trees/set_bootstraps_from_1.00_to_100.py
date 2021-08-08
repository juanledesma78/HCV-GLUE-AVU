"""This scritp takes a nweick tree generated using FASTTREE and modifies the bootstrap values to be dispalyed as 100 rather than 1.000 """
import re
with open("Smith2019_phylogeny_rerootedMidpoint_fasttree_annotated.nwk", "r") as original_tree:
    tree = original_tree.read()
    
    floating_bootstraps = re.findall(r'(\)(1|0)\.[0-9]*:*)', tree)
    #print(floating_bootstraps)
    """[(')0.997:', '0'), (')0.984:', '0'), (')1.000:', '1'), (')1.000:', '1'), (')0.834:', '0'), (')1.000:', '1'), (')0.929:', '0'), (')1.000:', '1'), (')1.000:', '1'), (')0.866:', '0')]"""
    
    bootstrap_dictionary ={}
    for bootstrap in floating_bootstraps:
        floatBst = bootstrap[0]
        fn = int(float((floatBst.replace(")","")).replace(":",""))*100)
        intBst = ")"+str(fn)+":"
        bootstrap_dictionary[floatBst] = intBst
        
    #print(bootstrap_dictionary)

    for k, v in bootstrap_dictionary.items():
        if k in tree:
            tree = tree.replace(k,v)

    with open("Smith2019_phylogeny_rerootedMidpoint_fasttree_annotated_bootstraps_100.nwk", "w") as modified_tree:
        modified_tree.write(tree)
    
modified_tree.close()
original_tree.close()  

