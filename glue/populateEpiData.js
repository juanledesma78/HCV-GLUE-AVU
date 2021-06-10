var epi_updates;

// access module tabularUtilityCsv and load data from file
glue.inMode("module/tabularUtilityCsv", function(){
    //epi_updates = glue.tableToObjects(glue.command(["load-tabular","tabular/made-up_MolisData_test_EPIDATA_NGS91.csv"]));
    epi_updates = glue.tableToObjects(glue.command(["load-tabular","tabular/made-up_MolisData_test_EPIDATA_NGS91_NA.csv"]));   
}
);

_.each(epi_updates, function(update){
    var patientId = update["NHS"].trim(); // remove white spaces in header,  
    //var nhsid = patientId.toLowerCase(); // GLUE does not accept Upper cases for the headers so this two steps are to make the header of the file and the fields in custom table to match
    var nationality = update["nationality"];
    var country = update["country_of_birth"];
    var ethnicity = update["ethnicity"];

    //glue.command(["create", "custom-table-row", "patient", nhsid]); //create custom-table-row samples <rowId> this will be the key, as it is molis you shoudl not add molis again
    glue.inMode("custom-table-row/patient/"+patientId, function(){ // access the row to set the fields
        //glue.command(["set", "field", "molis",molisName ]);  // hcvgen       molis        nhs          recept_dt    sample_dt --> fields in the custom table
		glue.command(["set", "field", "nationality", nationality]);
        glue.command(["set", "field", "country_of_birth", country]);
        glue.command(["set", "field", "ethnicity", ethnicity]);
            }
    );
    
}
);

