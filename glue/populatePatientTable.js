function nullTrim(string) {
	if(string == null) {
		return "-"; //return null;
	}
	return string.trim();
}

var patients;
glue.inMode("module/tabularUtilityCsv", function(){
    patients = glue.tableToObjects(glue.command(["load-tabular","tabular/table_patient/metadata_table_PATIENT_NGS93.csv"]));
}
);

//RETRIEVE AN ARRAY WITH THE SAMPLES ALREADY IN GLUE 
var patient_entries = glue.getTableColumn(glue.command(["list","custom-table-row", "patient"]),"id");

_.each(patients, function(patient){
    var patientId = nullTrim(patient["pid"]); 
    if (patient_entries.indexOf(patientId)!=-1) {print("patient", patientId, "already exists in GLUE")}
    else {
        print("patient ", patientId, " to be added in GLUE")
        var nhs = nullTrim(patient["NHS"]);  
        var dob = nullTrim(patient["ORDPATBIRTHDT"]);
        var sx = nullTrim(patient["ORDPATSX"]); 
        //var age_diagnosis; 
        // var city_of_residence;
        // var country_of_birth;    
        // var ethnicity;            
        // var nationality; 
        glue.command(["create", "custom-table-row", "patient", patientId]);
        glue.inMode("custom-table-row/patient/"+patientId, function(){ // access the row to set the fields
            glue.command(["set", "field", "nhs", nhs ]);  // hcvgen       molis        nhs          recept_dt    sample_dt --> fields in the custom table
	        glue.command(["set", "field", "date_of_birth", dob]);
            glue.command(["set", "field", "gender", sx]); 
            }); 
        }
    });