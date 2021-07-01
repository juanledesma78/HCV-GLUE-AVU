function nullTrim(string) {
	if(string == null) {
		return "-"; //return null;
	}
	return string.trim();
}

var drugs;

// access module tabularUtilityCsv and load data from file
glue.inMode("module/tabularUtilityCsv", function(){
    drugs = glue.tableToObjects(glue.command(["load-tabular","tabular/table_drug/hcv_medication.csv"]));
}
);


//ITERATE THE SAMPLES AND IDENTIFY THOSE ONES ALREADY INLCUDE IN GLUE 
_.each(drugs, function(drug){
    var drugId = nullTrim(drug["drug_id"]); // 
    var manufacturer = nullTrim(drug["manufacturer"]); 
    glue.command(["create", "custom-table-row", "drug", drugId]); //create custom-table-row sample <rowId> 
    glue.inMode("custom-table-row/drug/"+drugId, function(){ // access the row to set the fields
        glue.command(["set", "field", "manufacturer", manufacturer]);
        });
    });