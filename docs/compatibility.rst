#############################
Compatibility and translators
#############################

The BioRECIPE format is compatible with a range of representation formats, databases, and tools, either directly, or through translation. 

Attribute compatibility
-----------------------
Here we provide an overview of which attributes that BioRECIPE considers are included in other representation formats, output by several tools, including LLMs, or input in models by human curators.

Additional standards, databases, and tools and their compatibilities with BioRECIPE are listed in the following sections.

.. figure:: figures/figure_attribute_comparison_acrros_tools_representations.png
    :align: center
    :alt: internal figure

|

Translators summary
-------------------

The tables below list example formats, databases, and tools and links to translators.

| 

.. csv-table:: Formats compatible with BioRECIPE
    :header: Standard, Format, To BioRECIPE, From BioRECIPE, Description
    :widths: 15, 15, 10, 10, 50

    `SBML <https://sbml.org>`_, RDF/XML, ✓, ✓, `Direct translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`_ to and from BioRECIPE 
    `SBML-qual <https://sbml.org/documents/specifications/level-3/version-1/qual/>`_, RDF/XML, ✓, ✓, `Direct translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbmlqual>`_ to and from BioRECIPE
    `SIF <https://manual.cytoscape.org/en/stable/Supported_Network_File_Formats.html>`_, TXT, ✓, ✓, `Direct translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/SIF>`_ to and from BioRECIPE
    `BioPAX <https://www.biopax.org>`_, "RDF/OWL, SBML", ✓, ✓, Translation from and to BioPAX files can be done via `SBML translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`_ to and from BioRECIPE
    `BEL <https://bel.bio>`_, Structured TXT (BEL statements), ✓, ✓, Translation from and to `BEL statements <https://indra.readthedocs.io/en/latest/modules/sources/bel/index.html>`_ via `INDRA engine translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/indra_engine>`_
    `PySB <https://pysb.org>`_, `SBML <https://pysb.readthedocs.io/en/stable/modules/export/sbml.html>`_, ✓, ✓, `Translation from and to PySB files can be done via `SBML translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`_ to and from BioRECIPE 
    `REACH <http://agathon.sista.arizona.edu:8080/odinweb/>`_, Tabular (e.g., tsv), ✓, N/A, `Direct translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/reach_engine>`_ from REACH tabular format to BioRECIPE interaction list
    `TRIPS <https://trips.ihmc.us/parser/cgi/drum-dev>`_, XML, ✓, N/A, ???Translation from TRIPS output to BioRECIPE interaction list

|

.. csv-table:: Databases compatible with BioRECIPE
    :header: Database, Format, To BioRECIPE, From BioRECIPE, Description
    :widths: 15, 15, 10, 10, 50

    `KEGG <https://www.genome.jp/kegg/>`_, "KGML, SBML", ✓, ✓, Translation from and to `KGML files <https://github.com/draeger-lab/KEGGtranslator>`_ through the SBML translation to and from BioRECIPE
    `REACTOME <https://reactome.org/>`_, "SBML, BioPAX", ✓, ✓, See `SBML <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`_ and BioPAX translation
    `Pathway Commons <https://www.pathwaycommons.org/pc2/formats>`_, "SIF, BioPAX", ✓, ✓, See `SIF <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/SIF>`_ and BioPAX translation
    `NDEx <https://home.ndexbio.org/network-formats/>`_, "SIF, BEL(INDRA), BioPAX", ✓, ✓, See `SIF <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/SIF>`_ BEL and BioPAX translation
    `BioModels <https://www.ebi.ac.uk/biomodels/>`_, "SBML, SBML-qual", ✓, ✓, See `SBML <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`_ and `SBML-qual <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbmlqual>`_ translation


|


.. csv-table:: External tools compatible with BioRECIPE
    :header: Tool (external), Format, To BioRECIPE, From BioRECIPE, Description
    :widths: 15, 15, 10, 10, 50

    `Cytoscape <https://manual.cytoscape.org/en/stable/Supported_Network_File_Formats.html>`_, "SIF, CX(INDRA)", ✓, ✓, See `SIF translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/SIF>`_ or `INDRA translation  <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/indra>`_ and `CX assembler  <https://indra.readthedocs.io/en/latest/modules/assemblers/cx_assembler.html>`_ 
    `Cell Collective <https://cellcollective.org/#>`_, SBML-qual, ✓, ✓, See `SBML-qual translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbmlqual>`_
    `CellNetAnalyzer <https://www2.mpi-magdeburg.mpg.de/projects/cna/manual_cellnetanalyzer.pdf>`_, SBML, ✓, ✓, See `SBML translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`_ 
    `CellDesigner <https://www.celldesigner.org/help/CDH_File_07.html>`_, SBML, ✓, ✓, See `SBML translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/sbml>`_
    `INDRA <https://indra.readthedocs.io/en/latest/>`_, JSON, ✓, ✓, `Translation <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/indra>`_ to and from BioRECIPE Interaction List
    `REACH <https://github.com/clulab/reach/wiki/Supported-Output-Formats>`_, JSON, ✓, N/A, Translation to BioRECIPE Interaction List directly or through `INDRA <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/indra>`_
    `TRIPS <https://trips.ihmc.us/parser/api.html>`_, XML, ✓, N/A, Translation to BioRECIPE Interaction List directly or through `INDRA <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/tree/main/translators/indra>`_

|

.. csv-table:: MeLoDy Lab tools compatible with BioRECIPE
    :header: Tool, Description
    :widths: 20, 80

    `DiSH <https://github.com/pitt-miskov-zivanov-lab/dyse_wm>`_, Uses BioRECIPE Executable Model format at input
    `FLUTE <https://melody-flute.readthedocs.io/>`_, Uses BioRECIPE Interaction List format at input and output
    VIOLIN, Uses BioRECIPE Interaction List and Executable Model formats at input and output
    `CLARINET <https://melody-clarinet.readthedocs.io/>`_, Uses BioRECIPE Interaction List and Executable Model formats at input and output
    `ACCORDION <https://melody-accordion.readthedocs.io/>`_, Uses BioRECIPE Interaction List and Executable Model formats at input and output
    PIANO, Uses BioRECIPE Executable Model format at input
    `FIDDLE <https://melody-fiddle.readthedocs.io/>`_, Uses BioRECIPE Interaction List and Executable Model formats at input
    MINUET, Uses BioRECIPE Interaction List format at input and output

