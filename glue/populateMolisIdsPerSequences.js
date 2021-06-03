var sequenceMolis;

// access module tabularUtilityCsv and load data from file
glue.inMode("module/tabularUtilityCsv", function(){
    sequenceMolis = glue.tableToObjects(glue.command(["load-tabular","tabular/made-up_MolisData_test_MOLIS_NGS91.csv"]));
}
);
// glue.logInfo()
// this is equivalent to 
// modules/tabularUtilityCsv
// load-tabular tabular/made-up_MolisData_test_SAMPLES_NGS91.csv
// exit


// _.each is used to iterate over a list (samples) using the function
// every single item from samples is going to be modify with a first varaible and a second one if needed.
// second one is usually in case the header is used for something else (lower cases), and first one should be fine for the values
_.each(sequenceMolis, function(seqMol){
    var molisName = seqMol["MOLIS"].trim(); // remove white spaces in header,  
    //var molisID = molisName.toLowerCase(); // GLUE does not accept Upper cases for the headers so this two steps are to make the header of the file and the fields in custom table to match
    var sequenceName = seqMol["sequenceID"].trim(); // this will be the value in the iteration
    var nhsnum = seqMol["NHS"].trim();
    var nhsid = nhsnum.toLowerCase() 
    var hospCode = seqMol["CORORDNB"];
    glue.command(["create", "custom-table-row", "molis_id", sequenceName]); //create custom-table-row samples <rowId> this will be the index key, as it is molis you shoudl not add molis again
    glue.inMode("custom-table-row/molis_id/"+sequenceName, function(){ // access the row to set the fields
		glue.command(["set", "field", "molis", molisName]);
        glue.command(["set", "field", "nhs", nhsnum]);
        glue.command(["set", "field", "hospital_code", hospCode]);
        glue.command(["set", "link-target", "sequence", "sequence/NGS91/"+sequenceName]); 
        glue.command(["set", "link-target", "sample", "custom-table-row/sample/"+molisName]);//set link-target samples custom-table-row/samples/H210380785
        glue.command(["set", "link-target", "patient", "custom-table-row/patient/"+nhsid]);//set link-target samples custom-table-row/patient/H210380785
    }
    );
}
);



