var samples;

// access module tabularUtilityCsv and load data from file
glue.inMode("module/tabularUtilityCsv", function(){
    samples = glue.tableToObjects(glue.command(["load-tabular","tabular/made-up_MolisData_test_SAMPLES_NGS91.csv"]));
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
    var molisName = sample["MOLIS"].trim(); // remove white spaces in header,  
    var molisID = molisName.toLowerCase(); // GLUE does not accept Upper cases for the headers so this two steps are to make the header of the file and the fields in custom table to match
    var sampleDateName = sample["SAMPLE_DT"].trim(); // this will be the value in the iteration
    var sampleDateID = sampleDateName.toLowerCase(); // this is the header
    var receptionDateName = sample["RECEPT_DT"].trim();
    var receptionDateID = receptionDateName.toLowerCase();
    var initialGenotypeName = sample["HCVGEN"].trim();
    var initialGenotypeID = initialGenotypeName.toLowerCase();
    var nhsid = sample["NHS"].trim();
    var nhsNumber = initialGenotypeName.toLowerCase();
    


    glue.command(["create", "custom-table-row", "samples", molisName]); //create custom-table-row samples <rowId> this will be the key, as it is molis you shoudl not add molis again
    glue.inMode("custom-table-row/samples/"+molisName, function(){ // access the row to set the fields
        //glue.command(["set", "field", "molis",molisName ]);  // hcvgen       molis        nhs          recept_dt    sample_dt --> fields in the custom table
		glue.command(["set", "field", "sample_dt", sampleDateName]);
        glue.command(["set", "field", "recept_dt", receptionDateName]);
        glue.command(["set", "field", "hcvgen", initialGenotypeName]);
        glue.command(["set", "field", "nhs", nhsid]);
        glue.command(["set", "link-target", "patients", "custom-table-row/patients/"+nhsid]);//set link-target samples custom-table-row/samples/H210380785
    }
    );
    
}
);


//_.each(regions, function(region) {
//	var regionName = region["Region Name"].trim();
//	var regionId = regionName.toLowerCase();
//	var m49Code = region["Region Code"].trim();
//	glue.command(["create", "custom-table-row", "m49_region", regionId]); 
//	glue.inMode("custom-table-row/m49_region/"+regionId, function() {   
///		glue.command(["set", "field", "display_name", regionName]);
//		glue.command(["set", "field", "m49_code", m49Code]);
//	});
//});

// in project mode, equivalent to 
// 
