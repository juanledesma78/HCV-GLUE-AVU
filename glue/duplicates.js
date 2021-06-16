function nullTrim(string) {
	if(string == null) {
		return null;
	}
	return string.trim();
}

var GLUEsamples;


glue.inMode("/project/hcv_glue_avu", function(){
    GLUEsamples = glue.tableToObjects(glue.command(["list","sequence", "--whereClause","source.name != 'ncbi-refseqs' and sample.id!= null","sample.id","sample.patient.id"]));
}
);
glue.logInfo("GLUE samples", GLUEsamples)

// list sequence --whereClause "source.name != 'ncbi-refseqs' and sample.id!= null" sample.id sample.patient.id
