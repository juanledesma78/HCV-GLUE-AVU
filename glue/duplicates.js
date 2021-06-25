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

var newqs;
glue.inMode("/project/hcv_glue_avu", function(){
    newqs = glue.tableToObjects(glue.command(["list","sequence", "sequenceID"]));
}
);

_.each(newqs, function(newq){
	_.each(GLUEsamples, function(GLUEsample){
	glue.logInfo("TEXT",newq)
	glue.logInfo("GLUE samples", GLUEsample)
		});
});

//20:07:25.589 NashornJsScript INFO: GLUE samples
//{
//  "sample.id": "H210281395",
//  "sample.patient.id": "4669"
//}
//20:07:25.589 NashornJsScript INFO: TEXT
//{
//  "sequenceID": "H210760105-1_NGS93"
//}
//20:07:25.589 NashornJsScript INFO: GLUE samples
//{
//  "sample.id": "H210281396",
//  "sample.patient.id": "4670"
//}
//20:07:25.589 NashornJsScript INFO: TEXT
//{
//  "sequenceID": "H210760105-1_NGS93"
//}





// list sequence --whereClause "source.name != 'ncbi-refseqs' and sample.id!= null" sample.id sample.patient.id
