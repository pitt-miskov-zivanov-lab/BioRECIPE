Welcome to BioRECIPE's documentation!
=======================================
.. image:: https://readthedocs.org/projects/melody-biorecipe/badge/?version=latest
    :target: https://melody-biorecipe.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

BioRECIPE: Biological system Representation for Evaluation, Curation, Interoperability, Preserving, and Execution
--------------------------------------------------------------------------------------------------------

The BioRECIPE representation format was introduced to facilitate seamless human-machine interaction while creating, verifying, evaluating, curating, and expanding *executable models* of intra- and intercellular signaling. This format allows a human user to easily preview and modify any model components, while it is at the same time readable by machines and can be processed by a range of model development and analysis tools. The BioRECIPE format is a tabular format used for models that have a *directed graph* as their underlying structure.

BioRECIPE Workflow
---------------------

(Figures & Texts, TODO here)




Examples
---------------------

Several examples of interactions, their source and representation in the BioRECIPE format are listed in the table below.

.. csv-table:: Examples
    :header: Source, Original statement, Translation, BioRECIPE representation
    :widths: 10, 20, 20, 50

    Text in natural language, "TNFa reduces BMPR-II expression in vitro and in vivo", "a reading engine extracts the interaction that TNFa negatively regulates BMPR-II", "TODO biorecipe example"
    "Interaction database, STRING", an interaction between TRADD and TNF is predicted with high confidence, "TODO: translation procedure", "TODO: biorecipe example"
    Inferrence from data, "In the BioGRID database, we find that STAMBP deubiquitinates TNFRSF1A", "TODO: translation procedure", "TODO: biorecipe example"
    Experts enter manually, "NOTCH positively regulates stemness", "TODO: translation procedure", "TODO: biorecipe example"

   

Applications
---------------------

The BioRECIPE format has been used when modeling, simulating, and analyzing a number of systems.

.. csv-table:: Models
    :header: System, BioRECIPE representation, Publication 
    :widths: 20, 20, 60
    
    T cell, <link to BioRECIPE file>, `link <https://scholar.google.com/citations?view_op=view_citation&hl=en&user=tUrAYVsAAAAJ&citation_for_view=tUrAYVsAAAAJ:3fE2CSJIrl8C>`_ 
    CAR T cell, <link to BioRECIPE file>, `link <https://www.nmzlab.pitt.edu/research>`_ 
    macrophage, <link to BioRECIPE file>, `link <https://www.nmzlab.pitt.edu/research>`_ 
    melanoma, <link to BioRECIPE file>, `link <https://www.nmzlab.pitt.edu/research>`_ 
    pancreatic cancer cell, <link to BioRECIPE file>, `link <https://www.nmzlab.pitt.edu/research>`_ 
    GBM stem cell, <link to BioRECIPE file>, `link <https://www.nmzlab.pitt.edu/research>`_ 
    colon cancer cell, <link to BioRECIPE file>, `link <https://www.nmzlab.pitt.edu/research>`_ 
    ovarian cancer cell, <link to BioRECIPE file>, `link <https://www.nmzlab.pitt.edu/research>`_



Compatibility and Translators
---------------------

The BioRECIPE format is currently compatible with the following representation formats. 

.. csv-table:: Representation Format Compatibility
    :header: Format Name, Translator
    :widths: 10, 90

    SBML, <link to translator>
    JSON, <link to translator>
    other, <link to translator>

The BioRECIPE format is currently compatible with the following tools, their inputs and/or outputs.

.. csv-table:: Tool Compatibility
    :header: Tool Name, Translator to BioRECIPE, Translator from BioRECIPE 
    :widths: 10, 45, 45

    REACH, <link to translator>, NA
    TRIPS, <link to translator>, NA
    INDRA, <link to translator>, NA
    `DiSH simulator <https://scholar.google.com/citations?view_op=view_citation&hl=en&user=tUrAYVsAAAAJ&citation_for_view=tUrAYVsAAAAJ:GFxP56DSvIMC>`_, compatible
    `FLUTE <https://melody-flute.readthedocs.io>`_, compatible
    `VIOLIN <https://theviolin.readthedocs.io>`_, compatible
    `CLARINET <https://theclarinet.readthedocs.io>`_, compatible
    `ACCORDION <https://accordion.readthedocs.io>`_, compatible 
    `FIDDLE <https://melody-fiddle.readthedocs.io/>`_, compatible 
    `PIANO <https://dl.acm.org/doi/10.1145/3233547.3233694>`_, compatible


Acknowledgements
---------------------

Many previous and current members of MeLoDy Lab have contributed to the brainstorming and development of the BioRECIPE format. The format has gone through several versions and revisions.

The first version of the BioRECIPE format was developed by Dr. Khaled Sayed, Dr. Cheryl Telmer, Adam Butchy, and Dr. Natasa Miskov-Zivanov, and it was presented at the Machine Learning, Optimization, and Big Data (MOD) conference, where it received the Best Paper Award.

The current version of the BioRECIPE format has been developed thanks to the additional efforts of Dr. Kara Bocan, Dr. Casey Hansen, Dr. Emilee Holtzapple, Gaoxiang Zhou, Difei Tang, Dr. Yasmine Ahmed, and Stefan Andjelkovic.

The authors of this documentation are Dr. Natasa Miskov-Zivanov, Gaoxiang Zhou, Dr. Emilee Holtzapple, and Difei Tang.

.. toctree::
   :maxdepth: 2
   :caption: Contents
 
   bio_interactions
   graph_structure
   repre_interactions_biorecipe
   hybrid_ebm_def
   repre_model_biorecipe
   Legal
