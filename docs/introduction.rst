############
Introduction
############

The **BioRECIPE (Biological system Representation for Evaluation, Curation, Interoperability, Preserving, and Execution)** representation format was introduced to facilitate seamless human-machine interaction while creating, verifying, evaluating, curating, and expanding *executable models* of intra- and intercellular signaling. This format allows a human user to easily preview and modify any model component, while it is at the same time readable by machines and can be processed by a `suite <https://melody-biorecipe.readthedocs.io/en/latest/compatibility.html#compatibility-and-translators>`_ of model development and analysis tools. The BioRECIPE format is a tabular format most suitable for models that have a *directed graph* as their underlying structure.

Networks such as the one in the figure below (part A) can be represented with the BioRECIPE format. When creating interaction lists or models in the BioRECIPE format, information and data can be obtained from different sources, and input into BioRECIPE tables or spreadsheets automatically or manually (part B). Interaction lists and models written in the BioRECIPE format are convenient for different types of analysis and use (part C), either with automated tools, or manually, when human input is needed.

.. figure:: figures/figure_biorecipe_example_flow.png
    :align: center
    :alt: internal figure


|

The BioRECIPE format can be used to represent: 

    - *event-based* `lists of interactions <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#interaction-lists>`_ 
    - *element-based* `models <https://melody-biorecipe.readthedocs.io/en/latest/model_representation.html#executable-models>`_ 

These two formats are shown in the examples below. In interaction list tables, each row corresponds to one interaction, and in model tables, each row corresponds to one model elements. In these tables, columns correspond to various element and interaction attributes. The details of all interaction attributes used in interaction lists can be found `here <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#interaction-lists>`_, and the details for additional element attributes used to represent executable models can be found `here <https://melody-biorecipe.readthedocs.io/en/latest/model_representation.html#executable-models>`_. 

|

.. csv-table:: Example interaction lists in the BioRECIPE format
    :header: Description, BioRECIPE representation
    :widths: 30, 70

    Example 1 (from INDRA), `download <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/blob/main/examples/lee/Reading_Output_Example.xlsx>`_

|


.. csv-table:: Example models in the BioRECIPE format
    :header: System, BioRECIPE representation, Publication 
    :widths: 30, 30, 40
    
    T cell, download, `Tcell_SciSignal_2013 <https://scholar.google.com/citations?view_op=view_citation&hl=en&user=tUrAYVsAAAAJ&citation_for_view=tUrAYVsAAAAJ:3fE2CSJIrl8C>`_ 
    CAR T cell, download, `link <https://www.nmzlab.pitt.edu/research>`_ 
    macrophage, download, `link <https://www.nmzlab.pitt.edu/research>`_ 
    melanoma, download, `link <https://www.nmzlab.pitt.edu/research>`_ 
    pancreatic cancer cell, download, `link <https://www.nmzlab.pitt.edu/research>`_ 
    GBM stem cell, download, `link <https://www.nmzlab.pitt.edu/research>`_ 
    colon cancer cell, download, `link <https://www.nmzlab.pitt.edu/research>`_ 
    ovarian cancer cell, download, `link <https://www.nmzlab.pitt.edu/research>`_

|


Citation
---------

When using the BioRECIPE representation format, please cite the following:

  - Sayed, Khaled, et al. "Recipes for translating big data machine reading to executable cellular signaling models." Machine Learning, Optimization, and Big Data: Third International Conference, MOD 2017, Volterra, Italy, September 14–17, 2017, Revised Selected Papers 3. Springer International Publishing, 2018.
  - Miskov-Zivanov, Natasa, et al. BioRECIPE format, technical report, 2023.

|
