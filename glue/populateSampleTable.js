function nullTrim(string) {
	if(string == null) {
		return "-"; //return null;
	}
	return string.trim();
}

var samples;

// access module tabularUtilityCsv and load data from file
glue.inMode("module/tabularUtilityCsv", function(){
    samples = glue.tableToObjects(glue.command(["load-tabular","tabular/table_sample/metadata_table_SAMPLE_NGS94.csv"]));
}
);
// this is equivalent to 
// modules/tabularUtilityCsv
// load-tabular tabular/made-up_MolisData_test_SAMPLES_NGS91.csv
// exit

//RETRIEVE AN ARRAY WITH THE SAMPLES ALREADY IN GLUE 
var sample_entries = glue.getTableColumn(glue.command(["list","custom-table-row", "sample"]),"id");

//ITERATE THE SAMPLES AND IDENTIFY THOSE ONES ALREADY INLCUDE IN GLUE 
_.each(samples, function(sample){
    var molisId = nullTrim(sample["MOLIS"]); // 
    if (sample_entries.indexOf(molisId)!=-1) {print("sample", molisId, "already exists in GLUE")}
    else{
        print("sample ", molisId, " to be added in GLUE")
        var sampleDate = nullTrim(sample["SAMPLE_DT"]); 
        var receptionDate = nullTrim(sample["RECEPT_DT"]);
        var initialGenotype = nullTrim(sample["HCVGEN"]);
        var patientId = nullTrim(sample["pid"]);// set links,  not fields
        glue.command(["create", "custom-table-row", "sample", molisId]); //create custom-table-row sample <rowId> 
        glue.inMode("custom-table-row/sample/"+molisId, function(){ // access the row to set the fields
		    glue.command(["set", "field", "sample_date", sampleDate]);
            glue.command(["set", "field", "reception_date", receptionDate]);
            glue.command(["set", "field", "initial_genotype", initialGenotype]);
            //glue.command(["set", "field", "patient", patientid]); // NOT SURE ABOUT THIS 
            glue.command(["set", "link-target", "patient", "custom-table-row/patient/"+patientId]);
            //glue.command(["set", "link-target", "hospital", "custom-table-row/hospital/"+XXXX]);
            });
        }
                                });