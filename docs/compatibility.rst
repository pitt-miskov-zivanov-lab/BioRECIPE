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
    :header: Tool, Description
    :widths: 8, 92

    `DiSH <https://github.com/pitt-miskov-zivanov-lab/dyse_wm>`_, Uses BioRECIPE Executable Model format at input
    `FLUTE <https://melody-flute.readthedocs.io/>`_, Uses BioRECIPE Interaction List format at input and output
    VIOLIN, Uses BioRECIPE Interaction List and Executable Model formats at input and output
    `CLARINET <https://melody-clarinet.readthedocs.io/>`_, Uses BioRECIPE Interaction List and Executable Model formats at input and output
    `ACCORDION <https://melody-accordion.readthedocs.io/>`_, Uses BioRECIPE Interaction List and Executable Model formats at input and output
    PIANO, Uses BioRECIPE Executable Model format at input
    `FIDDLE <https://melody-fiddle.readthedocs.io/>`_, Uses BioRECIPE Interaction List and Executable Model formats at input
    MINUET, Uses BioRECIPE Interaction List format at input and output


|


The BioRECIPE format is compatible with the representation formats used in these databases.

.. csv-table:: Databases compatible with BioRECIPE
    :header: Database, Format, To BioRECIPE, From BioRECIPE, Translation description, Translation link
    :widths: 8, 8, 9, 9, 66

    KEGG, KGML SBML,✓, ✓,Conversion from and to KGML files through the SBML translation to and from BioRECIPE, `Link <https://github.com/draeger-lab/KEGGtranslator>`__
    REACTOME, SBML BioPAX,✓, ✓,See SBML and BioPAX conversion ,`Link <https://reactome.org/>`__
    Pathway Commons,SIF BioPAX,✓, ✓,See SIF and BioPAX conversion,`Link <https://www.pathwaycommons.org/pc2/formats>`__
    NDEx,SIF BEL (INDRA) BioPAX, ✓, ✓, See SIF BEL and BioPAX conversion, `Link <https://home.ndexbio.org/network-formats/>`__
    BioModels, SBML SBML-qual, ✓, ✓,See SBML and SBML-qual conversion, `Link <https://www.ebi.ac.uk/biomodels/>`__

