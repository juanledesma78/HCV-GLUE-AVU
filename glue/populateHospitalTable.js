function nullTrim(string) {
	if(string == null) {
		return "-"; //return null;
	}
	return string.trim();
}

var hospitals;
glue.inMode("module/tabularUtilityCsv", function(){
    hospitals = glue.tableToObjects(glue.command(["load-tabular","tabular/hospital_list.csv"]));
}
);

_.each(hospitals, function(hospital){
        var hospitalId = nullTrim(hospital["CORNB"]); 
        var hospitalName = nullTrim(hospital["CORNB_FULLNAME"]);  
        
        glue.command(["create", "custom-table-row", "hospital", hospitalId]);
        glue.inMode("custom-table-row/hospital/"+hospitalId, function(){ // access the row to set the fields
            glue.command(["set", "field", "hospital_name", hospitalName ]);  
            }); 
        }
    );