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

Compatibility
---------------------

The BioRECIPE format can be translated from/to the following formats:

- SBML (need a link to the translator)
- machine readers, REACH, TRIPS (need a link to the translator)
- INDRA (need a link to the translator)

The BioRECIPE format is compatible with the MeLoDy Lab tools:

- `DiSH simulator <https://scholar.google.com/citations?view_op=view_citation&hl=en&user=tUrAYVsAAAAJ&citation_for_view=tUrAYVsAAAAJ:GFxP56DSvIMC>`_ 
- `FLUTE <https://melody-flute.readthedocs.io>`_ 
- `VIOLIN <https://theviolin.readthedocs.io>`_ 
- `CLARINET <https://theclarinet.readthedocs.io>`_ 
- `ACCORDION <https://accordion.readthedocs.io>`_ 
- `FIDDLE <https://melody-fiddle.readthedocs.io/>`_ 
- `PIANO <https://dl.acm.org/doi/10.1145/3233547.3233694>`_ 

Main Applications
---------------------

The BioRECIPE format has been used for modeling, simulation, and analysis of:

- `T cells <https://scholar.google.com/citations?view_op=view_citation&hl=en&user=tUrAYVsAAAAJ&citation_for_view=tUrAYVsAAAAJ:3fE2CSJIrl8C>`_ 
- `CAR T cells <https://www.nmzlab.pitt.edu/research>`_ 
- `macrophages <https://www.nmzlab.pitt.edu/research>`_ 
- `melanoma cells <https://www.nmzlab.pitt.edu/research>`_ 
- `pancreatic cancer cells <https://www.nmzlab.pitt.edu/research>`_ 
- `glioblastoma multiforme stem cells <https://www.nmzlab.pitt.edu/research>`_ 
- `colon cancer cells <https://www.nmzlab.pitt.edu/research>`_ 
- `ovarian cancer cells <https://www.nmzlab.pitt.edu/research>`_.

Acknowledgements
---------------------

Many previous and current members of MeLoDy Lab have contributed to the brainstorming and development of the BioRECIPE format. The format has gone through several versions and revisions.

The first version of the BioRECIPE format was developed by Dr. Khaled Sayed, Dr. Cheryl Telmer, Adam Butchy, and Dr. Natasa Miskov-Zivanov, and it was presented at the Machine Learning, Optimization, and Big Data (MOD) conference, where it received the Best Paper Award.

The current version of the BioRECIPE format has been developed thanks to the additional efforts of Dr. Kara Bocan, Dr. Casey Hansen, Dr. Emilee Holtzapple, Gaoxiang Zhou, Difei Tang, Dr. Yasmine Ahmed, and Stefan Andjelkovic.

The authors of this documentation are Dr. Natasa Miskov-Zivanov, Gaoxiang Zhou, Dr. Emilee Holtzapple, and Difei Tang.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   graph_structure
   bio_interactions
   repre_interactions_biorecipe
   hybrid_ebm_def
   repre_model_biorecipe
   Legal
