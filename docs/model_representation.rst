#####################
Model representation
#####################

The BioRECIPE format supports representation of the static `graph structure <https://melody-biorecipe.readthedocs.io/en/latest/model_representation.html#graph-structure>`_ of models, as well as the attributes necessary to study the dynamics. 


Graph structure
---------------


A toy example of a model graph, showing input and output nodes, directed edges, paths, feedback and feedforward loops, and cellular compartments is shown in the figure below. (ER-endoplasmic reticulum)

.. figure:: figures/figure_toy_model_graph.png
    :align: center
    :alt: internal figure

    

The components of a directed graph :math:`G(V,E)`, and the attributes of these components relevant for modeling intracellular networks, are defined as follows.

.. csv-table::
    :header: Notation, Definition
    :widths: 7, 25

    ":math:`V=\{v_1,v_2,...,v_N\}`", "a set of :math:`N` nodes :math:`v_i (i=1,...,N)`, each assigned to one model **element**, where each element represents a component of the system being modeled"
    ":math:`E=\{e_1,e_2,...,e_M\}`", "a set of :math:`M` directed edges :math:`e_j (j=1,...,M)`, each assigned to an **interaction** between elements"
    ":math:`v_i=v(\mathbf{a}_i^v)`", "each node :math:`v_i` has an attribute vector :math:`\mathbf{a}^v≡(a^{\mathrm{name}},a^{\mathrm{type}},a^{\mathrm{subtype}},a^{\mathrm{database}},a^{\mathrm{ID}},a^{\mathrm{compartment}},a^{\mathrm{compartmentID}})`"
    ":math:`e_j=e(V_{s_j},v_{t_j},\mathbf{a}_j^e)`", "each edge :math:`e_j` has one or more source nodes in a set :math:`V_{s_j}`, a target node :math:`v_{t_j}`, and an attribute vector :math:`\mathbf{a}^e≡(a^{\mathrm{sign}},a^{\mathrm{connectiontype}},a^{\mathrm{mechanism}},a^{\mathrm{site}},a^{\mathrm{cellline}},` :math:`a^{\mathrm{celltype}},a^{\mathrm{tissuetype}},a^{\mathrm{organism}},a^{\mathrm{score}},a^{\mathrm{source}},a^{\mathrm{statements}},a^{\mathrm{paperIDs}})`"


Element representation
----------------------

In the BioRECIPE format, as part of model representation, each element :math:`v_i \in V` in a model :math:`\mathcal{M}` is assigned a row in the model table/spreadsheet. Different from *event-based* representation of `interactions <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#interaction-representation>`_, in this *element-based* representation multiple interactions can be combined as part of element update rules.

Besides the `basic <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#id3>`_ element (node) attributes, `context <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#id5>`_ and `provenance <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#id6>`_ are inherited from the interactions in which the element participates, and they are included in the element representation. Additionally, several more attributes are included to define the role of elements in executable models.
