var samples;

// access module tabularUtilityCsv and load data from file
glue.inMode("module/tabularUtilityCsv", function(){
    samples = glue.tableToObjects(glue.command(["load-tabular","tabular/made-up_MolisData_test_PATIENTS_NGS91.csv"]));
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
    var patientId = sample["NHS"].trim(); // remove white spaces in header,  
    var nhsid = patientId.toLowerCase(); // GLUE does not accept Upper cases for the headers so this two steps are to make the header of the file and the fields in custom table to match
    var dob = sample["ORDPATBIRTHDT"].trim();
    var sx = sample["ORDPATSX"].trim();   
    

    glue.command(["create", "custom-table-row", "patient", nhsid]); //create custom-table-row samples <rowId> this will be the key, as it is molis you shoudl not add molis again
    glue.inMode("custom-table-row/patient/"+nhsid, function(){ // access the row to set the fields
        //glue.command(["set", "field", "molis",molisName ]);  // hcvgen       molis        nhs          recept_dt    sample_dt --> fields in the custom table
		glue.command(["set", "field", "date_of_birth", dob]);
        glue.command(["set", "field", "gender", sx]);
        //glue.command(["add", "link-target", "molis_ids","custom-table-row/molis_ids/"+molisName]); 
        //glue.command(["set", "link", "nhs", nhsName]);
        // add link-target sequence sequence/ncbi-refseqs/ i need to create the link with sequence, regular experssion to get the molis number only and link to samples
    }
    );
    
}
);

