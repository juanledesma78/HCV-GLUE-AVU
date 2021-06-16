import subprocess
#subprocess.run(["gluetools.sh"])

#comm = 'list project\nproject hcv_glue_avu\nlist sequence\nQ\n'
#p1 = subprocess.run("gluetools.sh" , text=True, input=comm)


comm = 'project hcv_glue_avu\nimport source sources/NGS93\nQ\nexit\n'
p1 = subprocess.run("gluetools.sh" , text=True, input=comm)




