// if genotype is done by segments , alignment by segments should be done to include the new sequences
// if recombination, there is no point of alignments accordign to whole genome
/** 

*/

//Precursor polyprotein  >>>>>>>>>>>>>
var sequences = [];

var genotypingResultsPOLYPROTEIN;
glue.inMode("module/MaxLikelihoodGenotyper", function() {
	genotypingResultsPOLYPROTEIN = glue.tableToObjects(glue.command([
     "genotype", "sequence", "--whereClause", "reference_status ='recombinant'","--detailLevel", "HIGH"]));
    });
glue.logInfo("genotypingResults POLYPROTEIN",genotypingResultsPOLYPROTEIN)

  for(var i = 0; i < genotypingResultsPOLYPROTEIN.length; i++) {
    var resultPOLYPROTEIN = genotypingResultsPOLYPROTEIN[i]; 
    var queryNameBitsPOLYPROTEIN = resultPOLYPROTEIN.queryName.split("/"); // "ncbi-refseqs", "JF779679"
    var sourceName = queryNameBitsPOLYPROTEIN[0]; // "ncbi-refseqs"
	var sequenceID = queryNameBitsPOLYPROTEIN[1]; // "JF779679"
	var genotypeAlmtPOLYPROTEIN = resultPOLYPROTEIN.genotypeFinalClade; //"AL_1
	var subtypeAlmtPOLYPROTEIN = resultPOLYPROTEIN.subtypeFinalClade; //AL_1a
    var genotypeCladeBalancePOLYPROTEIN = resultPOLYPROTEIN.genotypeCladeBalance.split(":"); //"AL_2:100.00%"
    var genotypeCladePercentagePOLYPROTEIN = genotypeCladeBalancePOLYPROTEIN[1] ;
    var genotypeClosestMemberSequenceIDPOLYPROTEIN = resultPOLYPROTEIN.genotypeClosestMemberSequenceID; //"AB661382"
    var subtypeCladeBalancePOLYPROTEIN = resultPOLYPROTEIN.subtypeCladeBalance.split(":"); //"AL_2b:100.00%",
    var subtypetypeCladePercentagePOLYPROTEIN = subtypeCladeBalancePOLYPROTEIN[1] ;
    var subtypeClosestMemberSequenceIDPOLYPROTEIN = resultPOLYPROTEIN.subtypeClosestMemberSequenceID; //"AB661382"

    sequences.push(sequenceID)
   
   /** Update the result of the genotyping in the table sequence*/	
   glue.inMode("sequence/"+sourceName+"/"+sequenceID, function() 
   {
   var genotyping_polyprotein =""
       if(genotypeAlmtPOLYPROTEIN != null) {
           var gtRegex = /AL_([\d])/;
           var gtMatchPOLYPROTEIN = gtRegex.exec(genotypeAlmtPOLYPROTEIN);
           genotyping_polyprotein += gtMatchPOLYPROTEIN[1];
       }
       
       if(subtypeAlmtPOLYPROTEIN != null) {
           var stRegex = /AL_[\d](.+)/;
           var stMatchPOLYPROTEIN = stRegex.exec(subtypeAlmtPOLYPROTEIN);
           genotyping_polyprotein += stMatchPOLYPROTEIN[1];}
   //add in a single column
   glue.command(["set", "field", "genotyping_polyprotein", genotyping_polyprotein ]) //}
                                           
       });
                                          
    }



//CORE  >>>>>>>>>>>>>
var sequences = [];

var genotypingResultsCORE;
glue.inMode("module/MaxLikelihoodGenotyperCore", function() {
	genotypingResultsCORE = glue.tableToObjects(glue.command([
     "genotype", "sequence", "--whereClause", "reference_status ='recombinant'","--detailLevel", "HIGH"]));
    });
glue.logInfo("genotypingResults CORE",genotypingResultsCORE)

  for(var i = 0; i < genotypingResultsCORE.length; i++) {
    var resultCORE = genotypingResultsCORE[i]; 
    var queryNameBitsCORE = resultCORE.queryName.split("/"); // "ncbi-refseqs", "JF779679"
    var sourceName = queryNameBitsCORE[0]; // "ncbi-refseqs"
	var sequenceID = queryNameBitsCORE[1]; // "JF779679"
	var genotypeAlmtCORE = resultCORE.genotypeFinalClade; //"AL_1
	var subtypeAlmtCORE = resultCORE.subtypeFinalClade; //AL_1a
    var genotypeCladeBalanceCORE = resultCORE.genotypeCladeBalance.split(":"); //"AL_2:100.00%"
    var genotypeCladePercentageCORE = genotypeCladeBalanceCORE[1] ;
    var genotypeClosestMemberSequenceIDCORE = resultCORE.genotypeClosestMemberSequenceID; //"AB661382"
    var subtypeCladeBalanceCORE = resultCORE.subtypeCladeBalance.split(":"); //"AL_2b:100.00%",
    var subtypetypeCladePercentageCORE = subtypeCladeBalanceCORE[1] ;
    var subtypeClosestMemberSequenceIDCORE = resultCORE.subtypeClosestMemberSequenceID; //"AB661382"

    sequences.push(sequenceID)
   
   /** Update the result of the genotyping in the table sequence*/	
   glue.inMode("sequence/"+sourceName+"/"+sequenceID, function() 
   {
   var genotyping_core =""
       if(genotypeAlmtCORE != null) {
           var gtRegex = /AL_([\d])/;
           var gtMatchCORE = gtRegex.exec(genotypeAlmtCORE);
           genotyping_core += gtMatchCORE[1];
       }
       
       if(subtypeAlmtCORE != null) {
           var stRegex = /AL_[\d](.+)/;
           var stMatchCORE = stRegex.exec(subtypeAlmtCORE);
           genotyping_core += stMatchCORE[1];}
   //add in a single column
   glue.command(["set", "field", "genotyping_core", genotyping_core ]) //}
                                           
       });
                                          
    }



//E1 >>>>>>>>>>>>>

var genotypingResultsE1;
glue.inMode("module/MaxLikelihoodGenotyperE1", function() {
	genotypingResultsE1 = glue.tableToObjects(glue.command([
     "genotype", "sequence", "--whereClause", "reference_status ='recombinant'","--detailLevel", "HIGH"]));
    });
glue.logInfo("genotypingResults E1",genotypingResultsE1)

  for(var i = 0; i < genotypingResultsE1.length; i++) {
    var resultE1 = genotypingResultsE1[i]; 
    var queryNameBitsE1 = resultE1.queryName.split("/"); // "ncbi-refseqs", "JF779679"
    var sourceName = queryNameBitsE1[0]; // "ncbi-refseqs"
	var sequenceID = queryNameBitsE1[1]; // "JF779679"
	var genotypeAlmtE1 = resultE1.genotypeFinalClade; //"AL_1
	var subtypeAlmtE1 = resultE1.subtypeFinalClade; //AL_1a
    var genotypeCladeBalanceE1 = resultE1.genotypeCladeBalance.split(":"); //"AL_2:100.00%"
    var genotypeCladePercentageE1 = genotypeCladeBalanceE1[1] ;
    var genotypeClosestMemberSequenceIDE1 = resultE1.genotypeClosestMemberSequenceID; //"AB661382"
    var subtypeCladeBalanceE1 = resultE1.subtypeCladeBalance.split(":"); //"AL_2b:100.00%",
    var subtypetypeCladePercentageE1 = subtypeCladeBalanceE1[1] ;
    var subtypeClosestMemberSequenceIDE1 = resultE1.subtypeClosestMemberSequenceID; //"AB661382"

    /** Update the result of the genotyping in the table sequence*/	
    glue.inMode("sequence/"+sourceName+"/"+sequenceID, function() 
    {
    var genotyping_e1 =""
        if(genotypeAlmtE1 != null) {
            var gtRegex = /AL_([\d])/;
            var gtMatchE1 = gtRegex.exec(genotypeAlmtE1);
            genotyping_e1 += gtMatchE1[1];
        }
        
        if(subtypeAlmtE1 != null) {
            var stRegex = /AL_[\d](.+)/;
            var stMatchE1 = stRegex.exec(subtypeAlmtE1);
            genotyping_e1 += stMatchE1[1];}
    //add in a single column
    glue.command(["set", "field", "genotyping_e1", genotyping_e1 ]) //}
                                            
        });
                                        }


//E2 >>>>>>>>>>>>>

var genotypingResultsE2;
glue.inMode("module/MaxLikelihoodGenotyperE2", function() {
	genotypingResultsE2 = glue.tableToObjects(glue.command([
     "genotype", "sequence", "--whereClause", "reference_status ='recombinant'","--detailLevel", "HIGH"]));
    });
glue.logInfo("genotypingResults E2",genotypingResultsE2)

  for(var i = 0; i < genotypingResultsE2.length; i++) {
    var resultE2 = genotypingResultsE2[i]; 
    var queryNameBitsE2 = resultE2.queryName.split("/"); 
    var sourceName = queryNameBitsE2[0]; 
	var sequenceID = queryNameBitsE2[1]; 
	var genotypeAlmtE2 = resultE2.genotypeFinalClade; 
	var subtypeAlmtE2 = resultE2.subtypeFinalClade; 
    var genotypeCladeBalanceE2 = resultE2.genotypeCladeBalance.split(":"); //"AL_2:100.00%"
    var genotypeCladePercentageE2 = genotypeCladeBalanceE2[1] ;
    var genotypeClosestMemberSequenceIDE2 = resultE2.genotypeClosestMemberSequenceID; //"AB661382"
    var subtypeCladeBalanceE2 = resultE2.subtypeCladeBalance.split(":"); //"AL_2b:100.00%",
    var subtypetypeCladePercentageE2 = subtypeCladeBalanceE2[1] ;
    var subtypeClosestMemberSequenceIDE2 = resultE2.subtypeClosestMemberSequenceID; //"AB661382"

    /** Update the result of the genotyping in the table sequence*/	
    glue.inMode("sequence/"+sourceName+"/"+sequenceID, function() 
    {
    var genotyping_e2 =""
        if(genotypeAlmtE2 != null) {
            var gtRegex = /AL_([\d])/;
            var gtMatchE2 = gtRegex.exec(genotypeAlmtE2);
            genotyping_e2 += gtMatchE2[1];
        }
        
        if(subtypeAlmtE2 != null) {
            var stRegex = /AL_[\d](.+)/;
            var stMatchE2 = stRegex.exec(subtypeAlmtE2);
            genotyping_e2 += stMatchE2[1];}
    //add in a single column
    glue.command(["set", "field", "genotyping_e2", genotyping_e2 ]) //}
                                            
        });
                                        }


//P7 >>>>>>>>>>>>>

var genotypingResultsP7;
glue.inMode("module/MaxLikelihoodGenotyperP7", function() {
	genotypingResultsP7 = glue.tableToObjects(glue.command([
     "genotype", "sequence", "--whereClause", "reference_status ='recombinant'","--detailLevel", "HIGH"]));
    });
glue.logInfo("genotypingResults P7",genotypingResultsP7)

  for(var i = 0; i < genotypingResultsP7.length; i++) {
    var resultP7 = genotypingResultsP7[i]; 
    var queryNameBitsP7 = resultP7.queryName.split("/"); // "ncbi-refseqs", "JF779679"
    var sourceName = queryNameBitsP7[0]; // "ncbi-refseqs"
	var sequenceID = queryNameBitsP7[1]; // "JF779679"
	var genotypeAlmtP7 = resultP7.genotypeFinalClade; //"AL_1
	var subtypeAlmtP7 = resultP7.subtypeFinalClade; //AL_1a
    var genotypeCladeBalanceP7 = resultP7.genotypeCladeBalance.split(":"); //"AL_2:100.00%"
    var genotypeCladePercentageP7 = genotypeCladeBalanceP7[1] ;
    var genotypeClosestMemberSequenceIDP7 = resultP7.genotypeClosestMemberSequenceID; //"AB661382"
    var subtypeCladeBalanceP7 = resultP7.subtypeCladeBalance.split(":"); //"AL_2b:100.00%",
    var subtypetypeCladePercentageP7 = subtypeCladeBalanceP7[1] ;
    var subtypeClosestMemberSequenceIDP7 = resultP7.subtypeClosestMemberSequenceID; //"AB661382"

    /** Update the result of the genotyping in the table sequence*/	
    glue.inMode("sequence/"+sourceName+"/"+sequenceID, function() 
    {
    var genotyping_p7 =""
        if(genotypeAlmtP7 != null) {
            var gtRegex = /AL_([\d])/;
            var gtMatchP7 = gtRegex.exec(genotypeAlmtP7);
            genotyping_p7 += gtMatchP7[1];
        }
        
        if(subtypeAlmtP7 != null) {
            var stRegex = /AL_[\d](.+)/;
            var stMatchP7 = stRegex.exec(subtypeAlmtP7);
            genotyping_p7 += stMatchP7[1];}
    //add in a single column
    glue.command(["set", "field", "genotyping_p7", genotyping_p7 ]) //}
                                            
        });
                                        }


//NS2 >>>>>>>>>>>>>

var genotypingResultsNS2;
glue.inMode("module/MaxLikelihoodGenotyperNS2", function() {
	genotypingResultsNS2 = glue.tableToObjects(glue.command([
     "genotype", "sequence", "--whereClause", "reference_status ='recombinant'","--detailLevel", "HIGH"]));
    });
glue.logInfo("genotypingResults NS2",genotypingResultsNS2)

  for(var i = 0; i < genotypingResultsNS2.length; i++) {
    var resultNS2 = genotypingResultsNS2[i]; 
    var queryNameBitsNS2 = resultNS2.queryName.split("/"); // "ncbi-refseqs", "JF779679"
    var sourceName = queryNameBitsNS2[0]; // "ncbi-refseqs"
	var sequenceID = queryNameBitsNS2[1]; // "JF779679"
	var genotypeAlmtNS2 = resultNS2.genotypeFinalClade; //"AL_1
	var subtypeAlmtNS2 = resultNS2.subtypeFinalClade; //AL_1a
    var genotypeCladeBalanceNS2 = resultNS2.genotypeCladeBalance.split(":"); //"AL_2:100.00%"
    var genotypeCladePercentageNS2 = genotypeCladeBalanceNS2[1] ;
    var genotypeClosestMemberSequenceIDNS2 = resultNS2.genotypeClosestMemberSequenceID; //"AB661382"
    var subtypeCladeBalanceNS2 = resultNS2.subtypeCladeBalance.split(":"); //"AL_2b:100.00%",
    var subtypetypeCladePercentageNS2 = subtypeCladeBalanceNS2[1] ;
    var subtypeClosestMemberSequenceIDNS2 = resultNS2.subtypeClosestMemberSequenceID; //"AB661382"

    /** Update the result of the genotyping in the table sequence*/	
    glue.inMode("sequence/"+sourceName+"/"+sequenceID, function() 
    {
    var genotyping_ns2 =""
        if(genotypeAlmtNS2 != null) {
            var gtRegex = /AL_([\d])/;
            var gtMatchNS2 = gtRegex.exec(genotypeAlmtNS2);
            genotyping_ns2 += gtMatchNS2[1];
        }
        
        if(subtypeAlmtNS2 != null) {
            var stRegex = /AL_[\d](.+)/;
            var stMatchNS2 = stRegex.exec(subtypeAlmtNS2);
            genotyping_ns2 += stMatchNS2[1];}
    //add in a single column
    glue.command(["set", "field", "genotyping_ns2", genotyping_ns2 ]) //}
                                            
        });
                                        }


//NS3 >>>>>>>>>>>>>

var genotypingResultsNS3;
glue.inMode("module/MaxLikelihoodGenotyperNS3", function() {
	genotypingResultsNS3 = glue.tableToObjects(glue.command([
     "genotype", "sequence", "--whereClause", "reference_status ='recombinant'","--detailLevel", "HIGH"]));
    });
glue.logInfo("genotypingResults NS3",genotypingResultsNS3)

  for(var i = 0; i < genotypingResultsNS3.length; i++) {
    var resultNS3 = genotypingResultsNS3[i]; 
    var queryNameBitsNS3 = resultNS3.queryName.split("/"); // "ncbi-refseqs", "JF779679"
    var sourceName = queryNameBitsNS3[0]; // "ncbi-refseqs"
	var sequenceID = queryNameBitsNS3[1]; // "JF779679"
	var genotypeAlmtNS3 = resultNS3.genotypeFinalClade; //"AL_1
	var subtypeAlmtNS3 = resultNS3.subtypeFinalClade; //AL_1a
    var genotypeCladeBalanceNS3 = resultNS3.genotypeCladeBalance.split(":"); //"AL_2:100.00%"
    var genotypeCladePercentageNS3 = genotypeCladeBalanceNS3[1] ;
    var genotypeClosestMemberSequenceIDNS3 = resultNS3.genotypeClosestMemberSequenceID; //"AB661382"
    var subtypeCladeBalanceNS3 = resultNS3.subtypeCladeBalance.split(":"); //"AL_2b:100.00%",
    var subtypetypeCladePercentageNS3 = subtypeCladeBalanceNS3[1] ;
    var subtypeClosestMemberSequenceIDNS3 = resultNS3.subtypeClosestMemberSequenceID; //"AB661382"

    /** Update the result of the genotyping in the table sequence*/	
    glue.inMode("sequence/"+sourceName+"/"+sequenceID, function() 
    {
    var genotyping_ns3 =""
        if(genotypeAlmtNS3 != null) {
            var gtRegex = /AL_([\d])/;
            var gtMatchNS3 = gtRegex.exec(genotypeAlmtNS3);
            genotyping_ns3 += gtMatchNS3[1];
        }
        
        if(subtypeAlmtNS3 != null) {
            var stRegex = /AL_[\d](.+)/;
            var stMatchNS3 = stRegex.exec(subtypeAlmtNS3);
            genotyping_ns3 += stMatchNS3[1];}
    //add in a single column
    glue.command(["set", "field", "genotyping_ns3", genotyping_ns3 ]) //}
                                            
        });
                                        }
//NS4A >>>>>>>>>>>>>

var genotypingResultsNS4A;
glue.inMode("module/MaxLikelihoodGenotyperNS4A", function() {
	genotypingResultsNS4A = glue.tableToObjects(glue.command([
     "genotype", "sequence", "--whereClause", "reference_status ='recombinant'","--detailLevel", "HIGH"]));
    });
glue.logInfo("genotypingResults NS4A",genotypingResultsNS4A)

  for(var i = 0; i < genotypingResultsNS4A.length; i++) {
    var resultNS4A = genotypingResultsNS4A[i]; 
    var queryNameBitsNS4A = resultNS4A.queryName.split("/"); // "ncbi-refseqs", "JF779679"
    var sourceName = queryNameBitsNS4A[0]; // "ncbi-refseqs"
	var sequenceID = queryNameBitsNS4A[1]; // "JF779679"
	var genotypeAlmtNS4A = resultNS4A.genotypeFinalClade; //"AL_1
	var subtypeAlmtNS4A = resultNS4A.subtypeFinalClade; //AL_1a
    var genotypeCladeBalanceNS4A = resultNS4A.genotypeCladeBalance.split(":"); //"AL_2:100.00%"
    var genotypeCladePercentageNS4A = genotypeCladeBalanceNS4A[1] ;
    var genotypeClosestMemberSequenceIDNS4A = resultNS4A.genotypeClosestMemberSequenceID; //"AB661382"
    var subtypeCladeBalanceNS4A = resultNS4A.subtypeCladeBalance.split(":"); //"AL_2b:100.00%",
    var subtypetypeCladePercentageNS4A = subtypeCladeBalanceNS4A[1] ;
    var subtypeClosestMemberSequenceIDNS4A = resultNS4A.subtypeClosestMemberSequenceID; //"AB661382"

    /** Update the result of the genotyping in the table sequence*/	
    glue.inMode("sequence/"+sourceName+"/"+sequenceID, function() 
    {
    var genotyping_ns4a =""
        if(genotypeAlmtNS4A != null) {
            var gtRegex = /AL_([\d])/;
            var gtMatchNS4A = gtRegex.exec(genotypeAlmtNS4A);
            genotyping_ns4a += gtMatchNS4A[1];
        }
        
        if(subtypeAlmtNS4A != null) {
            var stRegex = /AL_[\d](.+)/;
            var stMatchNS4A = stRegex.exec(subtypeAlmtNS4A);
            genotyping_ns4a += stMatchNS4A[1];}
    //add in a single column
    glue.command(["set", "field", "genotyping_ns4a", genotyping_ns4a ]) //}
                                            
        });
                                        }


//NS4B >>>>>>>>>>>>>

var genotypingResultsNS4B;
glue.inMode("module/MaxLikelihoodGenotyperNS4B", function() {
	genotypingResultsNS4B = glue.tableToObjects(glue.command([
     "genotype", "sequence", "--whereClause", "reference_status ='recombinant'","--detailLevel", "HIGH"]));
    });
glue.logInfo("genotypingResults NS4B",genotypingResultsNS4B)

  for(var i = 0; i < genotypingResultsNS4B.length; i++) {
    var resultNS4B = genotypingResultsNS4B[i]; 
    var queryNameBitsNS4B = resultNS4B.queryName.split("/"); // "ncbi-refseqs", "JF779679"
    var sourceName = queryNameBitsNS4B[0]; // "ncbi-refseqs"
	var sequenceID = queryNameBitsNS4B[1]; // "JF779679"
	var genotypeAlmtNS4B = resultNS4B.genotypeFinalClade; //"AL_1
	var subtypeAlmtNS4B = resultNS4B.subtypeFinalClade; //AL_1a
    var genotypeCladeBalanceNS4B = resultNS4B.genotypeCladeBalance.split(":"); //"AL_2:100.00%"
    var genotypeCladePercentageNS4B = genotypeCladeBalanceNS4B[1] ;
    var genotypeClosestMemberSequenceIDNS4B = resultNS4B.genotypeClosestMemberSequenceID; //"AB661382"
    var subtypeCladeBalanceNS4B = resultNS4B.subtypeCladeBalance.split(":"); //"AL_2b:100.00%",
    var subtypetypeCladePercentageNS4B = subtypeCladeBalanceNS4B[1] ;
    var subtypeClosestMemberSequenceIDNS4B = resultNS4B.subtypeClosestMemberSequenceID; //"AB661382"

    /** Update the result of the genotyping in the table sequence*/	
    glue.inMode("sequence/"+sourceName+"/"+sequenceID, function() 
    {
    var genotyping_ns4b =""
        if(genotypeAlmtNS4B != null) {
            var gtRegex = /AL_([\d])/;
            var gtMatchNS4B = gtRegex.exec(genotypeAlmtNS4B);
            genotyping_ns4b += gtMatchNS4B[1];
        }
        
        if(subtypeAlmtNS4B != null) {
            var stRegex = /AL_[\d](.+)/;
            var stMatchNS4B = stRegex.exec(subtypeAlmtNS4B);
            genotyping_ns4b += stMatchNS4B[1];}
    //add in a single column
    glue.command(["set", "field", "genotyping_ns4b", genotyping_ns4b ]) //}
                                            
        });
                                        }

//NS5A >>>>>>>>>>>>>

var genotypingResultsNS5A;
glue.inMode("module/MaxLikelihoodGenotyperNS5A", function() {
	genotypingResultsNS5A = glue.tableToObjects(glue.command([
     "genotype", "sequence", "--whereClause", "reference_status ='recombinant'","--detailLevel", "HIGH"]));
    });
glue.logInfo("genotypingResults NS5A",genotypingResultsNS5A)

  for(var i = 0; i < genotypingResultsNS5A.length; i++) {
    var resultNS5A = genotypingResultsNS5A[i]; 
    var queryNameBitsNS5A = resultNS5A.queryName.split("/"); // "ncbi-refseqs", "JF779679"
    var sourceName = queryNameBitsNS5A[0]; // "ncbi-refseqs"
	var sequenceID = queryNameBitsNS5A[1]; // "JF779679"
	var genotypeAlmtNS5A = resultNS5A.genotypeFinalClade; //"AL_1
	var subtypeAlmtNS5A = resultNS5A.subtypeFinalClade; //AL_1a
    var genotypeCladeBalanceNS5A = resultNS5A.genotypeCladeBalance.split(":"); //"AL_2:100.00%"
    var genotypeCladePercentageNS5A = genotypeCladeBalanceNS5A[1] ;
    var genotypeClosestMemberSequenceIDNS5A = resultNS5A.genotypeClosestMemberSequenceID; //"AB661382"
    var subtypeCladeBalanceNS5A = resultNS5A.subtypeCladeBalance.split(":"); //"AL_2b:100.00%",
    var subtypetypeCladePercentageNS5A = subtypeCladeBalanceNS5A[1] ;
    var subtypeClosestMemberSequenceIDNS5A = resultNS5A.subtypeClosestMemberSequenceID; //"AB661382"

    /** Update the result of the genotyping in the table sequence*/	
    glue.inMode("sequence/"+sourceName+"/"+sequenceID, function() 
    {
    var genotyping_ns5a =""
        if(genotypeAlmtNS5A != null) {
            var gtRegex = /AL_([\d])/;
            var gtMatchNS5A = gtRegex.exec(genotypeAlmtNS5A);
            genotyping_ns5a += gtMatchNS5A[1];
        }
        
        if(subtypeAlmtNS5A != null) {
            var stRegex = /AL_[\d](.+)/;
            var stMatchNS5A = stRegex.exec(subtypeAlmtNS5A);
            genotyping_ns5a += stMatchNS5A[1];}
    //add in a single column
    glue.command(["set", "field", "genotyping_ns5a", genotyping_ns5a ]) //}
                                            
        });
                                        }


//NS5B >>>>>>>>>>>>>

var genotypingResultsNS5B;
glue.inMode("module/MaxLikelihoodGenotyperNS5B", function() {
	genotypingResultsNS5B = glue.tableToObjects(glue.command([
     "genotype", "sequence", "--whereClause", "reference_status ='recombinant'","--detailLevel", "HIGH"]));
    });
glue.logInfo("genotypingResults NS5B",genotypingResultsNS5B)

  for(var i = 0; i < genotypingResultsNS5B.length; i++) {
    var resultNS5B = genotypingResultsNS5B[i]; 
    var queryNameBitsNS5B = resultNS5B.queryName.split("/"); // "ncbi-refseqs", "JF779679"
    var sourceName = queryNameBitsNS5B[0]; // "ncbi-refseqs"
	var sequenceID = queryNameBitsNS5B[1]; // "JF779679"
	var genotypeAlmtNS5B = resultNS5B.genotypeFinalClade; //"AL_1
	var subtypeAlmtNS5B = resultNS5B.subtypeFinalClade; //AL_1a
    var genotypeCladeBalanceNS5B = resultNS5B.genotypeCladeBalance.split(":"); //"AL_2:100.00%"
    var genotypeCladePercentageNS5B = genotypeCladeBalanceNS5B[1] ;
    var genotypeClosestMemberSequenceIDNS5B = resultNS5B.genotypeClosestMemberSequenceID; //"AB661382"
    var subtypeCladeBalanceNS5B = resultNS5B.subtypeCladeBalance.split(":"); //"AL_2b:100.00%",
    var subtypetypeCladePercentageNS5B = subtypeCladeBalanceNS5B[1] ;
    var subtypeClosestMemberSequenceIDNS5B = resultNS5B.subtypeClosestMemberSequenceID; //"AB661382"

    /** Update the result of the genotyping in the table sequence*/	
    glue.inMode("sequence/"+sourceName+"/"+sequenceID, function() 
    {
    var genotyping_ns5b =""
        if(genotypeAlmtNS5B != null) {
            var gtRegex = /AL_([\d])/;
            var gtMatchNS5B = gtRegex.exec(genotypeAlmtNS5B);
            genotyping_ns5b += gtMatchNS5B[1];
        }
        
        if(subtypeAlmtNS5B != null) {
            var stRegex = /AL_[\d](.+)/;
            var stMatchNS5B = stRegex.exec(subtypeAlmtNS5B);
            genotyping_ns5b += stMatchNS5B[1];}
    //add in a single column
    glue.command(["set", "field", "genotyping_ns5b", genotyping_ns5b ]) //}
                                            
        });
                                        }


_.each(sequences, function(sequence){
    var seqID = sequence;
    var finalGenotyping="";
    genotyping = glue.tableToObjects(glue.command([
        "list", "sequence", "--whereClause", "sequenceID ='"+sequence+"'","genotyping_polyprotein","genotyping_core","genotyping_e1","genotyping_e2", "genotyping_p7", "genotyping_ns2", "genotyping_ns3", "genotyping_ns4a", "genotyping_ns4b", "genotyping_ns5a", "genotyping_ns5b"]));
    glue.logInfo("<Genotyping Results>",genotyping)  
});

 
/**
 * list sequence -w"reference_status ='recombinant'" sequenceID genotyping_polyprotein genotyping_core genotyping_e1 genotyping_e2 genotyping_p7 genotyping_ns2 genotyping_ns3 genotyping_ns4a genotyping_ns4b genotyping_ns5a genotyping_ns5b
 
list sequence --whereClause "reference_status ='recombinant'" sequenceID genotype subtype genotyping_polyprotein genotyping_core genotyping_e1 genotyping_e2 genotyping_p7 genotyping_ns2 genotyping_ns3

*/