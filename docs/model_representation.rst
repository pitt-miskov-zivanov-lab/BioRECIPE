#################
Executable models
#################

The BioRECIPE format supports representation of the static graph structure of models, as well as attributes necessary to study the dynamics. Models are represented in the BioRECIPE format using *element-based* approach.

A toy example of a model graph, including input and output nodes, directed edges, paths, feedback and feedforward loops, and cellular compartments is shown in the `introduction <https://melody-biorecipe.readthedocs.io/en/latest/introduction.html#introduction>`_. 



Model formats
-------------

In the BioRECIPE format, model representation, each element in a model is assigned a row in the model table/spreadsheet. Different from *event-based* representation of `interactions <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#interaction-representation>`_, in this *element-based* representation interactions in which the element participates as a regulated element (target node of interaction edge) can be combined into an element update rule. The BioRECIPE format supports several different model representation schemes, ranging from less detailed to more detailed, from static graph attributes to dynamic attributes and parameters necessary for analysis of dynamic behavior, as illustrated in the table below (x indicates attributes included in the representation scheme):

.. figure:: figures/figure_BioRECIPE_model_format.png
    :align: center
    :alt: internal figure

|

The following tables provide details for each attribute, including attribute name used in the BioRECIPE spreadsheet, a symbol used in `detailed definitions <https://melody-biorecipe.readthedocs.io/en/latest/definitions.html#formal-definitions>`_, a brief description of the attribute, its allowed values, and a few examples for the attribute. Model examples can be found `here <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/blob/main/examples>`_. 

|
|

The `basic <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#basic-element-attributes>`_ element (node) attributes, and `context <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#context-attributes>`_ attributes are inherited from the interactions in which the element participates (as a regulated element), and they are included in the element representation, as shown in the figure above (columns under **Element** header). 

|

|

Several other interaction attributes are ordered lists of values from all individual interactions where the element is a regulated element (target node on the interaction edge). These are referred to as **Regulation** attributes and include basic and provenance attributes combined from indvidual interactions (`basic interaction <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#basic-interaction-attributes>`_ and `provenance <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#provenance-attributes>`_ attributes) .

|

Regulation attributes - basic
-----------------------------

.. csv-table:: 
    :header: Attribute, Symbol, Description, Values, Examples
    :widths: 5, 3, 34, 38, 20

    Positive regulators list, ":math:`a^{\mathrm{posreglist}}`", description, "<positive regulator 1>, <positive regulator 2>, ..., <positive regulator :math:`k`>", examples
    Positive connection type, ":math:`a^{\mathrm{posconnectiontype}}`", description, "<positive connection type 1>, <positive connection type 2>, ..., <positive connection type :math:`k`>", examples
    Positive mechanism, ":math:`a^{\mathrm{posmechanism}}`", description, "<positive mechanism 1>, <positive mechanism 2>, ..., <positive mechanism :math:`k`>", examples
    Positive site, ":math:`a^{\mathrm{possite}}`", description, "<positive site 1>, <positive site 2>, ..., <positive site :math:`k`>", examples
    Negative regulators list, ":math:`a^{\mathrm{negreglist}}`", description, "<negative regulator 1>, <negative regulator 2>, ..., <negative regulator :math:`l`>", examples
    Negative connection type, ":math:`a^{\mathrm{negconnectiontype}}`", description, "<negative connection type 1>, <negative connection type 2>, ..., <negative connection type :math:`l`>", examples
    Negative mechanism, ":math:`a^{\mathrm{negmechanism}}`", description, "<negative mechanism 1>, <negative mechanism 2>, ..., <negative mechanism :math:`l`>", examples
    Negative site, ":math:`a^{\mathrm{negsite}}`", description, "<negative site 1>, <negative site 2>, ..., <negative site :math:`l`>", examples
    
|

Regulation attributes - provenance
-----------------------------

.. csv-table:: 
    :header: Attribute, Symbol, Description, Values, Examples
    :widths: 5, 3, 34, 38, 20

    Scores, ":math:`a^{\mathrm{score}}`", description, "<score 1>, <score 2>, ..., <score :math:`k+l`>", examples
    Sources, ":math:`a^{\mathrm{source}}`", description, "<source 1>, <source 2>, ..., <source :math:`k+l`>", examples
    Statements, ":math:`a^{\mathrm{statements}}`", description, "<statements 1>, <statements 2>, ..., <statements :math:`k+l`>", examples
    Paper IDs, ":math:`a^{\mathrm{paperIDs}}`", description, "<paper IDs 1>, <paper IDs 2>, ..., <paper IDs :math:`k+l`>", examples
|

Finally, several new model attributes are included in executable models to define element update rules, as well as value and timing parameters for the simulation. These attributes are included under **Simulation parameters** in the figure above.

|

Rule attributes
------------------------

.. csv-table:: 
    :header: Attribute, Symbol, Description, Values, Examples
    :widths: 5, 3, 34, 38, 20
    
     Positive regulation rule, ":math:`a^{\mathrm{posregrule}}`", description, "<string>  //The rules for creating these positive regulation strings are written separately.", examples
    Negative regulation rule, ":math:`a^{\mathrm{negregurule}}`", description, "<string>  //The rules for creating these negative regulation strings are written separately.", examples


|


Value attributes
------------------------

.. csv-table:: 
    :header: Attribute, Symbol, Description, Values, Examples
    :widths: 5, 3, 34, 38, 20
    
    Variable, ":math:`a^{\mathrm{variable}}`", description, <variable_name>, examples
    Value type, ":math:`a^{\mathrm{valuetype}}`", description, ``amount`` | ``activity``, examples
    Levels, ":math:`a^{\mathrm{levels}}`", description, <number of distinct levels> | ``inf``, examples
    State list number, ":math:`a^{\mathrm{statelist}}`", description, "<value>,<value>[time],...,<value>[time]", examples
    Const OFF, ":math:`a^{\mathrm{constOFF}}`", description, empty | :math:`\checkmark`, examples
    Const ON, ":math:`a^{\mathrm{constON}}`", description, empty | :math:`\checkmark`, examples
    Increment, ":math:`a^{\mathrm{increment}}`", description, ":math:`\Delta \mathrm{value}`", examples

|

Timing attributes
-----------------

.. csv-table:: 
    :header: Attribute, Symbol, Description, Values, Examples
    :widths: 5, 3, 34, 38, 20

    Spontaneous, ":math:`a^{\mathrm{spontaneous}}`", description, definition, examples
    Balancing, ":math:`a^{\mathrm{balancing}}`", description, definition, examples
    Delay, ":math:`a^{\mathrm{delay}}`", description, definition, examples
    Update group, ":math:`a^{\mathrm{updategroup}}`", description, definition, examples
    Update rate, ":math:`a^{\mathrm{updaterate}}`", description, definition, examples
    Update rank, ":math:`a^{\mathrm{updaterank}}`", description, definition, examples


