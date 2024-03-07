#############################
Compatibility and translators
#############################

The BioRECIPE format is compatible with a range of representation formats, databases, and tools, either directly, or through translation. The tables below list example formats and tools and links to translators. The translator repositories provide further instructions for the use of translators.

| 

.. csv-table:: Formats compatible with BioRECIPE
    :header: Standard, Format, To BioRECIPE, From BioRECIPE, Description
    :widths: 8, 8, 9, 9, 66

    SBML, RDF/XML, ✓, ✓, `Translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`_ to BioRECIPE Executable Model and from BioRECIPE Interaction List 
    SBML-qual, RDF/XML, ✓, ✓, `Translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbmlqual>`_ to and from BioRECIPE Executable Model
    SIF, TXT, ✓, ✓, `Translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/SIF>`_ to and from BioRECIPE Interaction List and from BioRECIPE Executable Model
    BioPAX, "RDF/OWL, SBML", ✓, ✓, `Conversion <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`_ from and to BioPAX files can be done through SBML translation to and from BioRECIPE
    BEL, TXT (INDRA), ✓, ✓, `Conversion <https://indra.readthedocs.io/en/latest/modules/sources/bel/index.html>`__ from and to `BEL <https://github.com/pybel/pybel>`__ statements through INDRA statements  
    PySB, SBML, ✓, ✓, `Translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`_ from and to `PySB files <https://pysb.readthedocs.io/en/stable/modules/export/sbml.html>`_ can be done through the SBML translation to and from BioRECIPE  

|


.. csv-table:: External tools compatible with BioRECIPE
    :header: Tool (external), Format, To BioRECIPE, From BioRECIPE, Description
    :widths: 8, 8, 9, 9, 66

    Cytoscape, "SIF, CX(INDRA)", ✓, ✓, See `SIF translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/SIF>`_ or `INDRA translation  <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/indra>`_ and `CX assembler  <https://indra.readthedocs.io/en/latest/modules/assemblers/cx_assembler.html>`_ 
    `Cell Collective <https://cellcollective.org/#>`_, SBML-qual, ✓, ✓, See `SBML-qual translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbmlqual>`_
    `CellNetAnalyzer <https://www2.mpi-magdeburg.mpg.de/projects/cna/manual_cellnetanalyzer.pdf>`_, SBML, ✓, ✓, See `SBML translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`_ 
    CellDesigner, SBML, ✓, ✓, See `SBML conversion <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`_
    INDRA, JSON, ✓, ✓, `Conversion <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/indra>`_ to and from BioRECIPE Interaction List
    REACH, JSON, ✓, N/A, Conversion to BioRECIPE Interaction List directly or through `INDRA <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/indra>`_
    TRIPS, XML, ✓, N/A, Conversion to BioRECIPE Interaction List directly or through `INDRA <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/indra>`_

|

.. csv-table:: MeLoDy Lab tools compatible with BioRECIPE
    :header: Tool, Format, Description
    :widths: 8, 8, 84

    DiSH, BioRECIPE, Uses BioRECIPE format at input, `Link <https://github.com/pitt-miskov-zivanov-lab/dyse_wm>`__
    `FLUTE <https://github.com/pitt-miskov-zivanov-lab/flute>`_, BioRECIPE, Uses BioRECIPE format at input 
    VIOLIN, BioRECIPE, Uses BioRECIPE format at input, 
    `CLARINET <https://github.com/pitt-miskov-zivanov-lab/clarinet>`__, BioRECIPE, Uses BioRECIPE format at input
    `ACCORDION <https://github.com/pitt-miskov-zivanov-lab/ACCORDION>`_, BioRECIPE, Uses BioRECIPE format at input
    PIANO, BioRECIPE, Uses BioRECIPE format at input,
    `FIDDLE <https://melody-fiddle.readthedocs.io/>`__, BioRECIPE, Uses BioRECIPE format at input
    MINUET, BioRECIPE, Uses BioRECIPE format at input,


|


The BioRECIPE format is compatible with the representation formats used in these databases.

.. csv-table:: Format Compatibility with BioRECIPE
    :header: Database, Format, To BioRECIPE, From BioRECIPE, Translation description, Translation link
    :widths: 20, 20, 15, 15, 50, 80

    KEGG, KGML SBML,✓, ✓,Conversion from and to KGML files through the SBML translation to and from BioRECIPE, `Link <https://github.com/draeger-lab/KEGGtranslator>`__
    REACTOME, SBML BioPAX,✓, ✓,See SBML and BioPAX conversion ,`Link <https://reactome.org/>`__
    Pathway Commons,SIF BioPAX,✓, ✓,See SIF and BioPAX conversion,`Link <https://www.pathwaycommons.org/pc2/formats>`__
    NDEx,SIF BEL (INDRA) BioPAX, ✓, ✓, See SIF BEL and BioPAX conversion, `Link <https://home.ndexbio.org/network-formats/>`__
    BioModels, SBML SBML-qual, ✓, ✓,See SBML and SBML-qual conversion, `Link <https://www.ebi.ac.uk/biomodels/>`__

