function nullTrim(string) {
	if(string == null) {
		return "-"; //return null;
	}
	return string.trim();
}

var treatments;

// access module tabularUtilityCsv and load data from file
glue.inMode("module/tabularUtilityCsv", function(){
    treatments = glue.tableToObjects(glue.command(["load-tabular","tabular/table_treatment/treatment.csv"]));
}
);


//ITERATE THE SAMPLES AND IDENTIFY THOSE ONES ALREADY INLCUDE IN GLUE 
_.each(treatments, function(treatment){
    var treatmentId = nullTrim(treatment["id"]); // 
    var patientId = nullTrim(treatment["patient_id"]); // 
    var drugId = nullTrim(treatment["drug_id"]); // 
    var dose = nullTrim(treatment["dose"]);
    var treatmentDt = nullTrim(treatment["treatment_date"]); 
    glue.command(["create", "custom-table-row", "treatment", treatmentId]); //create custom-table-row sample <rowId> 
    glue.inMode("custom-table-row/treatment/"+treatmentId, function(){ // access the row to set the fields
        //glue.command(["set", "field", "patient_id", patientId]); // 
        //glue.command(["set", "field", "drug_id", drugId]);
        glue.command(["set", "field", "dose", dose]);
        glue.command(["set", "field", "treatment_date", treatmentDt]);
        glue.command(["set", "link-target", "drug", "custom-table-row/drug/"+drugId]);
        //glue.command(["add", "link-target", "patient", "custom-table-row/patient/"+patientId]);
        });
    });

