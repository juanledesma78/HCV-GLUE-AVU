function nullTrim(string) {
	if(string == null) {
		return "-"; //return null;
	}
	return string.trim();
}

var epi_updates;

// access module tabularUtilityCsv and load data from file
glue.inMode("module/tabularUtilityCsv", function(){
    epi_updates = glue.tableToObjects(glue.command(["load-tabular","tabular/epi_data/Epidata_table_PATIENT_NGS99.csv"]));   
}
);

_.each(epi_updates, function(update){
    var patientId = nullTrim(update["pid"]); // remove white spaces in header,  
    var nationality = nullTrim(update["nationality"]);
    var country = nullTrim(update["country_of_birth"]);
    var ethnicity = nullTrim(update["ethnicity"]);
    var diagnosis = nullTrim(update["diagnosis_date"]);
    var hiv_status = nullTrim(update["hiv_infection"]); 
    var city = nullTrim(update["city"]); 
    // NHS?
    //glue.command(["create", "custom-table-row", "patient", nhsid]); //create custom-table-row samples <rowId> this will be the key, as it is molis you shoudl not add molis again
    glue.inMode("custom-table-row/patient/"+patientId, function(){ // access the row to set the fields
        //glue.command(["set", "field", "molis",molisName ]);  // hcvgen       molis        nhs          recept_dt    sample_dt --> fields in the custom table
		glue.command(["set", "field", "nationality", nationality]);
        glue.command(["set", "field", "country_of_birth", country]);
        glue.command(["set", "field", "ethnicity", ethnicity]);
        glue.command(["set", "field", "diagnosis_date", diagnosis]);
        glue.command(["set", "field", "hiv_infection", hiv_status]);
        glue.command(["set", "field", "city_of_residence", city]);
        print("info for patient",patientId,"added")
            }
    );
    
}
);

