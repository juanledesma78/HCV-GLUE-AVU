function nullTrim(string) {
	if(string == null) {
		return "-"; //return null;
	}
	return string.trim();
}

var drugs;

// access module tabularUtilityCsv and load data from file
glue.inMode("module/tabularUtilityCsv", function(){
    drugs = glue.tableToObjects(glue.command(["load-tabular","tabular/hcv_medication.csv"]));
}
);
_.each(drugs, function(drug){
    var drugId = nullTrim(drug["drug_id"]); // 
    var manufacturer = nullTrim(drug["manufacturer"]); 
    var therapy_class = nullTrim(drug["therapy_class"]); 
    glue.command(["create", "custom-table-row", "drug", drugId]); //create custom-table-row sample <rowId> 
    glue.inMode("custom-table-row/drug/"+drugId, function(){ 
        glue.command(["set", "field", "manufacturer", manufacturer]);
        glue.command(["set", "field", "therapy_class", therapy_class]);
        });
    });