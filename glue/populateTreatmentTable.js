function nullTrim(string) {
	if(string == null) {
		return "-"; //return null;
	}
	return string.trim();
}

var treatment_entries = glue.getTableColumn(glue.command(["list","custom-table-row", "treatment"]),"id");

var treatments;

// access module tabularUtilityCsv and load data from file
glue.inMode("module/tabularUtilityCsv", function(){
    treatments = glue.tableToObjects(glue.command(["load-tabular","tabular/epi_data/Treatment_NGS99.csv"]));
}
);

//ITERATE THE SAMPLES AND IDENTIFY THOSE ONES ALREADY INLCUDE IN GLUE 
_.each(treatments, function(treatment){
    var treatmentId = nullTrim(treatment["id"]); 
    var patientId = nullTrim(treatment["pid"]); 
    var drugId = nullTrim(treatment["drug_id"]);  
    var dose = nullTrim(treatment["regime"]);
    var treatmentDt = nullTrim(treatment["treatment_date"]);
    
    if (treatment_entries.indexOf(treatmentId)!=-1) {print("treatment", treatmentId, "from patient",patientId,"ALREADY in GLUE")}
    else{
        print("New treatment (", treatmentId, ") for patient" ,patientId, "added in GLUE") 
    glue.command(["create", "custom-table-row", "treatment", treatmentId]); //create custom-table-row sample <rowId> 
    glue.inMode("custom-table-row/treatment/"+treatmentId, function(){ // access the row to set the fields
        //glue.command(["set", "field", "patient_id", patientId]); // not set becuase it is link to another table
        //glue.command(["set", "field", "drug_id", drugId]);// not set becuase it is link to another table 
        glue.command(["set", "field", "regime", dose]);
        glue.command(["set", "field", "treatment_date", treatmentDt]);
        glue.command(["set", "link-target", "drug", "custom-table-row/drug/"+drugId]);
        glue.command(["set", "link-target", "patient", "custom-table-row/patient/"+patientId]);
        });
        }
    });

