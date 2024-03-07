#############################
Compatibility and Translators
#############################

The BioRECIPE format is currently compatible with the following representation formats. 

.. csv-table:: Representation Format Compatibility
    :header: Format Name, Translator
    :widths: 20, 80

    SBML, `Link <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`__
    JSON, `Link <#>`__
    other, `Link <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`__

The BioRECIPE format is currently compatible with the following tools, their inputs and/or outputs.

.. csv-table:: Format Compatibility with BioRECIPE
    :header: Tool (external), Format, To BioRECIPE, From BioRECIPE, Translation description, Tool link
    :widths: 20, 20, 15, 15, 50, 80

    Cytoscape,SIF CX (INDRA),✓, ✓,See SIF conversion or conversion through INDRA statements, `Link <https://indra.readthedocs.io/en/latest/modules/assemblers/cx_assembler.html>`__
    Cell Collective, SBML-qual, ✓, ✓,See SBML-qual conversion, `Link <https://cellcollective.org/#>`__
    CellNetAnalyzer, SBML, ✓, ✓, See SBML conversion, `Link <https://www2.mpi-magdeburg.mpg.de/projects/cna/manual_cellnetanalyzer.pdf>`__
    CellDesigner,SBML, ✓, ✓,See SBML conversion, `Link <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`__
    INDRA, JSON, ✓, ✓,Conversion to and from BioRECIPE Interaction List, `Link <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/indra>`__
    REACH, JSON, ✓, N/A, Conversion to BioRECIPE Interaction List, `Link <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/indra>`__
    TRIPS, XML,✓, N/A, Conversion to BioRECIPE Interaction List, `Link <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/indra>`__

.. csv-table:: Format Compatibility with BioRECIPE
    :header: Tool, Format, To BioRECIPE, From BioRECIPE, Translation description, Tool link
    :widths: 20, 20, 15, 15, 50, 80

    DiSH, BioRECIPE,  ✓, ✓,Uses BioRECIPE format at input, `Link <https://github.com/pitt-miskov-zivanov-lab/dyse_wm>`__
    FLUTE, BioRECIPE, ✓, ✓,Uses BioRECIPE format at input, `Link <https://github.com/pitt-miskov-zivanov-lab/flute>`__
    VIOLIN, BioRECIPE,✓, ✓,Uses BioRECIPE format at input, `Link <#>`__
    CLARINET, BioRECIPE,✓, ✓,Uses BioRECIPE format at input,`Link <https://github.com/pitt-miskov-zivanov-lab/clarinet>`__
    ACCORDION, BioRECIPE,✓, ✓,Uses BioRECIPE format at input,`Link <https://github.com/pitt-miskov-zivanov-lab/ACCORDION>`__
    PIANO, BioRECIPE,✓, ✓,Uses BioRECIPE format at input,`Link <https://dl.acm.org/doi/10.1145/3233547.3233694>`__
    FIDDLE,BioRECIPE,✓, ✓,Uses BioRECIPE format at input,`Link <https://melody-fiddle.readthedocs.io/>`__
    MINUET, BioRECIPE,✓, ✓,Uses BioRECIPE format at input,`Link <#>`__



.. csv-table:: Format Compatibility with BioRECIPE
    :header: Standard, Format, To BioRECIPE, From BioRECIPE, Translation description, Translation link
    :widths: 20, 20, 15, 15, 50, 80

    SBML, RDF/XML, ✓, ✓, Translation to BioRECIPE Executable Model and from BioRECIPE Interaction List, `Link <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`__
    SBML-qual, RDF/XML, ✓, ✓, Translation to and from BioRECIPE Executable Model, `Link <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbmlqual>`__
    SIF, TXT,✓, ✓,Translation to and from BioRECIPE Interaction List and from BioRECIPE Executable Model, `Link <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/SIF>`__
    BioPAX, RDF/OWL SBML,✓, ✓,Conversion from and to BioPAX files can be done through SBML translation to and from BioRECIPE, `Link <https://sbml.org/software/converters/>`__ `Link <https://www.celldesigner.org/help/CDH_File_07.html>`__
    BEL, TXT (INDRA), ✓, ✓, Conversion from and to BEL statements through INDRA statements, `Link <https://indra.readthedocs.io/en/latest/modules/sources/bel/index.html>`__ `Link <https://github.com/pybel/pybel>`__
    PySB, SBML,✓, ✓,Translation from and to PySB files can be done through the SBML translation to and from BioRECIPE, `Link <https://pysb.readthedocs.io/en/stable/modules/export/sbml.html>`__ `Link <https://pysb.readthedocs.io/en/stable/modules/importers/index.html>`__

The BioRECIPE format is compatible with the representation formats used in these databases.

.. csv-table:: Format Compatibility with BioRECIPE
    :header: Database, Format, To BioRECIPE, From BioRECIPE, Translation description, Translation link
    :widths: 20, 20, 15, 15, 50, 80

    KEGG, KGML SBML,✓, ✓,Conversion from and to KGML files through the SBML translation to and from BioRECIPE, `Link <https://github.com/draeger-lab/KEGGtranslator>`__
    REACTOME, SBML BioPAX,✓, ✓,See SBML and BioPAX conversion ,`Link <https://reactome.org/>`__
    Pathway Commons,SIF BioPAX,✓, ✓,See SIF and BioPAX conversion,`Link <https://www.pathwaycommons.org/pc2/formats>`__
    NDEx,SIF BEL (INDRA) BioPAX, ✓, ✓, See SIF BEL and BioPAX conversion, `Link <https://home.ndexbio.org/network-formats/>`__
    BioModels, SBML SBML-qual, ✓, ✓,See SBML and SBML-qual conversion, `Link <https://www.ebi.ac.uk/biomodels/>`__

