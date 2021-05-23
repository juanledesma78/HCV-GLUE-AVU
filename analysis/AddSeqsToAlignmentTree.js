/**
 
*/

/** Adding and align (compute) the new sequences to all the alignment trees*/

function addToAlignment(sourceName, sequenceID, almtName) {
	glue.inMode("alignment/"+almtName, function() {
		glue.command(["add", "member", sourceName, sequenceID]);
	});
	glue.command(["compute", "alignment", almtName, "CompoundAligner", 
	              "--whereClause", "sequence.source.name = '"+sourceName+"' and sequence.sequenceID = '"+sequenceID+"'"]);
}



/** Genotyping and adding new sequences to the appropiate alignment tree*/
var genotypingResults;

glue.inMode("module/MaxLikelihoodGenotyper", function() {
	genotypingResults = glue.tableToObjects(glue.command([
	 "genotype", "sequence", "--whereClause", "source.name in ( 'NGS91')"]));
}); 
/** "genotype", "sequence", "--whereClause", "source.name in ( 'NGS91','NGS92')"])); ORIGINAL*/
/** genotype sequence --whereClause "sequence.source.name= 'fasta-hev-examples'" --detailLevel HIGH --dataDir genotyping_results.txt # it works in GLUE using commands*/
/** genotype sequence --whereClause "source.name= 'NGS91'" --detailLevel HIGH --dataDir genotyping_results_NGS91 # the results are not added to the tables if using the script
 * genotype", "sequence", "--whereClause", "sequence.source.name= 'NGS91'", it does not recognised sequence.source.name= 
 * 
*/

for(var i = 0; i < genotypingResults.length; i++) {
	var result = genotypingResults[i];
	var queryNameBits = result.queryName.split("/");
	var sourceName = queryNameBits[0];
	var sequenceID = queryNameBits[1];
	
	var genotypeAlmt = result.genotypeFinalClade;
	var subtypeAlmt = result.subtypeFinalClade;
	if(genotypeAlmt != null) {
		
		if(subtypeAlmt != null) {
			addToAlignment(sourceName, sequenceID, subtypeAlmt);
		} else {
			addToAlignment(sourceName, sequenceID, genotypeAlmt);
		}
	}


/** Update the result of the genotyping in the table sequence */	
	glue.inMode("sequence/"+sourceName+"/"+sequenceID, function() {

		if(genotypeAlmt != null) {
			var gtRegex = /AL_([\d])/;
			var gtMatch = gtRegex.exec(genotypeAlmt);
			if(gtMatch) {
				glue.command(["set", "field", "genotype", gtMatch[1]]);
			}
			if(subtypeAlmt != null) {
				var stRegex = /AL_[\d](.+)/;
				var stMatch = stRegex.exec(subtypeAlmt);
				if(stMatch) {
					glue.command(["set", "field", "subtype", stMatch[1]]);
				}
			}
		}
	});
	
}

/** GLUE> sequence fasta-hev-examples IND-HEV-AVH1-1991 
OK
Mode path: /project/learning/sequence/fasta-hev-examples/IND-HEV-AVH1-1991
GLUE> set 
GLUE> set field 
-C                      collection_year         gb_accession_version    
gb_create_date          gb_gi_number            gb_locus                
gb_organism             gb_primary_accession    gb_taxonomy             
gb_update_date          genotype                host_species            
isolate                 length                  subtype   

GLUE> set field genotype <fieldValue>
*/