######################
Biocuration resources
######################




.. raw:: html

    <div class="sticky-first-column">

.. csv-table:: Biocuration Resource Table - main table
    :header: Name,GO (Gene Ontology),miRBase,UniProt,ChEBI,BioGRID,HPRD,KEGG,MINT,PathwayCommons ,Reactome,SIGNOR,STITCH,STRING,WikiPathways,FLUTE,INDRA,IntAct,OmniPath,PCnet,BioModels,CellCollective,Path2Models,MINERVA,BioKC,nDex,REACH,RLIMS-P,Sparser
    :widths: 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5

    Type,Entity database,Entity database,Entity database,Entity database,Interaction database,Interaction database,Interaction database,Interaction database,Interaction database,Interaction database,Interaction database,Interaction database,Interaction database,Interaction database,Metadatabase,Metadatabase,Metadatabase,Metadatabase,Metadatabase,Model repository,Model repository,Model repository,Model repository,Model repository,Model repository/metadatabase,Reader,Reader,Reader
    Curation? (Manual/Automated),Maual and automated,Manual (staff curators),Maual and automated,Manual (staff curators),Manual and automated,Manual (staff curators),Manual (staff curators and data providers),Manual (registered users),Manual (from data providers),Manual (staff curators),Manual (staff curators),Manual and automated,Manual and automated,Manual (registered users),Manual (staff curators),Manual and automated,Manual (staff curators),Manual (staff curators),Manual (staff curators),Manual (registered users),Manual (registered users),Automated (from other databases),Manual (registered users),Manual (registered users),Manual (registered users),N/A,N/A,N/A
    Programmatic access?,Yes (API),No,Yes (API),Yes (Web service),Yes (API),No,Yes (API),Yes (API),No,Yes (API),Yes (API),Yes (API),Yes (API),No,Yes (Python script),Yes (API),No,Yes (API),No,No,No,No,Yes (API),Yes (API),Yes (API),Yes (API),No,Yes (Lisp)
    Input format,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,GPML,N/A,N/A,N/A,N/A,N/A,"SBML (preferred), CellML, matlab","SBML, boolean expressions",N/A,SBML,SBML,CX,"NXML, text","Keywords, PMIDs","Text, XML"
    Output format,"OWL, OBO, GAF, etc.","FASTA, EMBL","FASTA, TSV, XML, JSON, etc.","Molfile, XML, SDF","PSI-MITAB, XML, BioGRID TAB","BioPAX, SBML, PSI-MI","KGML, PNG",MITAB,"PNG, SIF, JSON, SBGN, BioPAX","SBML, BioPAX, SBGN,PNG","SBML, TSV","TSV, PNG, XML, MFA","TSV, PNG, XML, MFA","PNG, JSON, GPML, SVG","BioRECIPE, SIF","PySB, SBML, BEL, JSON",PSI-MITAB,SIF,SIF,"SBML,XPP, VCML, SciLab, Octave, BioPAX, PNG, SVG","SBML, GML, truth tables, boolean expressions","SBML,XPP, VCML, SciLab, Octave, BioPAX, PNG, SVG","CellDesigner SBML, SBML, SBGN, PNG",,"TSV, CX","JSON,TSV",TSV,None
    Number of models/pathways/interactions if database,"43,850 GO terms / 7,928,834 annotations /1,568,828 gene products","38,589 miRNAs","569,213 reviewed / 245,871,679  unreviewed proteins","151,344 substances / 139,678 annotations",>3 million interactions,">40,000 PPI, 36 pathways","70,423 references ","136,218 interactions","5,772 pathways /2,424,055 interactions/ 22 databases","13,827 interactions / 2536 pathways","29,245 interactions",1.6 billion interactions,>20 billion interactions,">1,100 pathways",30 million+ interactions,N/A,"5,565,271 interactions",100+ networks/databases,21 networks/databases,"2,914 models",229 models,"~140,00 models",9 networks,No public networks,">5,000 networks",N/A,N/A,N/A
    Systems modeled?,Multiple species,Multiple species,Multiple species,Multiple species,Multiple species,Homo sapiens,Multiple Species,Multiple Species,Multiple species,Homo sapiens,"Homo sapiens, Mus musculus, Rattus norvegicus",Multiple species,Multiple species,Multiple species,Homo sapiens,Multiple Species,Multiple Species,Multiple Species,Homo sapiens,Multiple species,Multiple species,Multiple Species,Multiple species,Multiple species,Multiple species,N/A,N/A,N/A
    Automated verification or validation?,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,Has model-checking function,No,No,No,No,Yes (simulation),No,Yes (model annotation requirements),Yes (model annotation requirements),No,No,No,No
    Automated filtering?,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,Belief score,No,No,No,No,No,Models are sorted by genus,No,No,No,No,No,No
    Automated identification of extensions/contradictions,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No
    Automatically resolve contradictions?,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No,No
    Automated recommendations?,No,No,No,No,No,No,No,No,No,No,No,Yes,Yes,No,No,No,No,No,No,No,No,No,No,Yes,No,No,No,No
.. raw:: html

    </div>


- ChEBI: Chemical Entities of Biological Interest
- BioGRID: The Biological General Repository for Interaction Datasets
- HPRD: Human Protein Reference Database
- KEGG: Kyoto Encyclopedia of Genes and Genomes
- MINT: Molecular Interaction Database
- SIGNOR: Signaling Network Open Resource
- STITCH: Search Tool for Interacting Chemicals
- STRING: Search Tool for Retrieval of Interacting Genes/Proteins
- FLUTE: FiLter for Understanding True Events
- INDRA: Integrated Network and Dynamical Reasoning Assembler
- PCnet: Parsimonius Composite Network
- nDex: The Network Data Exchange
- REACH: Reading and Assembling Contextual and Holistic Mechanisms from Text
- RRLIMS-P: Rule-based Literature Mining System for Protein Phosphorylation


| 
.. csv-table:: Biocuration Resource Table - metadatabase source
    :header: blank,INDRA,PCnet,FLUTE,OmniPath
    :widths: 5, 5, 6, 6, 6

    3DComplex,,,,X
    ABS ,,,,X
    ACSN,X,,,X
    Adhesome,,,,X
    AlzPathway,,,,X
    ARACNe,,,,X
    ARN ,,,,X
    Ataxia,,,,X
    BIND,,X,,
    BioCarta,,,,X
    BioGRID,X,X,X,X
    BioPLEX,,X,,
    CancerCellMap,,,,X
    CancerDrugsDB ,,,,X
    CancerSEA,,,,X
    CARFMAP,,,,X
    CellCall ,,,,X
    CellCellInteractions,,,,X
    CellChatDB,,,,X
    Cellinker ,,,,X
    CellPhoneDB,,,,X
    cellsignal.com,,,,X
    CellTalkDB,,,,X
    CellTypist,,,,X
    CFinder,,,,X
    Compleat ,,,,X
    ComplexPortal,,,,X
    ComPPI,,,,X
    connectomeDB2020,,,,X
