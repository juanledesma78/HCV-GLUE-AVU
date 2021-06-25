function nullTrim(string) {
	if(string == null) {
		return null;
	}
	return string.trim();
}

var samples;

// access module tabularUtilityCsv and load data from file
glue.inMode("module/tabularUtilityCsv", function(){
    samples = glue.tableToObjects(glue.command(["load-tabular","tabular/table_sample/metadata_table_SAMPLE_NGS91.csv"]));
}
);
// glue.logInfo()
// this is equivalent to 
// modules/tabularUtilityCsv
// load-tabular tabular/made-up_MolisData_test_SAMPLES_NGS91.csv
// exit


// _.each is used to iterate over a list (samples) using the function
// every single item from samples is going to be modify with a firt varaible and a second one.
// second one is usually for the header, and first one should be fine for the values
_.each(samples, function(sample){
    var molisId = nullTrim(sample["MOLIS"]); // 
    var sampleDate = nullTrim(sample["SAMPLE_DT"]); // this will be the value in the iteration
    var receptionDate = nullTrim(sample["RECEPT_DT"]);
    var initialGenotype = nullTrim(sample["HCVGEN"]);
    var patientId = nullTrim(sample["pid"]);// set links not fields
    
    glue.command(["create", "custom-table-row", "sample", molisId]); //create custom-table-row samples <rowId> this will be the key, as it is molis you shoudl not add molis again
    glue.inMode("custom-table-row/sample/"+molisId, function(){ // access the row to set the fields
        //glue.command(["set", "field", "XXX",XXXX ]);  // hcvgen       molis        nhs          recept_dt    sample_dt --> fields in the custom table
		glue.command(["set", "field", "sample_date", sampleDate]);
        glue.command(["set", "field", "reception_date", receptionDate]);
        glue.command(["set", "field", "initial_genotype", initialGenotype]);
        //glue.command(["set", "field", "patient", patientid]); // NOT SURE ABOUT THIS 
        glue.command(["set", "link-target", "patient", "custom-table-row/patient/"+patientId]);
        //glue.command(["set", "link-target", "hospital", "custom-table-row/hospital/"+XXXX]);
        //set link-target samples custom-table-row/sample/H210380785
    }
    );
}
);
