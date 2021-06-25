function nullTrim(string) {
	if(string == null) {
		return null;
	}
	return string.trim();
}

var patients;
glue.inMode("module/tabularUtilityCsv", function(){
    patients = glue.tableToObjects(glue.command(["load-tabular","tabular/table_patient/metadata_table_PATIENT_NGS91.csv"]));
}
);
_.each(patients, function(patient){
    var patientId = nullTrim(patient["pid"]); 
    var nhs = nullTrim(patient["NHS"]);  
    var nhsid = nhs.toLowerCase(); // GLUE does not accept Upper cases for the headers so this two steps are to make the header of the file and the fields in custom table to match
    var dob = nullTrim(patient["ORDPATBIRTHDT"]);
    var sx = nullTrim(patient["ORDPATSX"]); 
    //var age_diagnosis; 
    // var city_of_residence;
    // var country_of_birth;    
    // var ethnicity;            
    // var nationality; 

    glue.command(["create", "custom-table-row", "patient", patientId]); //create custom-table-row samples <rowId> this will be the key, as it is molis you shoudl not add molis again
    glue.inMode("custom-table-row/patient/"+patientId, function(){ // access the row to set the fields
    glue.command(["set", "field", "nhs", nhs ]);  // hcvgen       molis        nhs          recept_dt    sample_dt --> fields in the custom table
	glue.command(["set", "field", "date_of_birth", dob]);
    glue.command(["set", "field", "gender", sx]);
    //glue.command(["add", "link-target", "molis_ids","custom-table-row/molis_ids/"+molisName]); 
    //glue.command(["set", "link", "nhs", nhsName]);
    // add link-target sequence sequence/ncbi-refseqs/ i need to create the link with sequence, regular experssion to get the molis number only and link to samples
    }
    );
    
}
);

