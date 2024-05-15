#################
Executable models
#################

The BioRECIPE format supports representation of the static graph structure of models, as well as attributes necessary to study the dynamics. Models are represented in the BioRECIPE format using *element-based* approach.

A toy example of a model graph, including input and output nodes, directed edges, paths, feedback and feedforward loops, and cellular compartments is shown in the `introduction <https://melody-biorecipe.readthedocs.io/en/latest/introduction.html#introduction>`_. 



Model formats
-------------

In the BioRECIPE format, each element in a model is assigned a row in the model table/spreadsheet. Different from *event-based* representation of `interactions <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#interaction-representation>`_, in this *element-based* representation interactions in which the element participates as a regulated element (target node of interaction edge) can be combined into an element update rule. The BioRECIPE format supports several different model representation schemes, ranging from less detailed to more detailed, from static graph attributes to dynamic attributes and parameters necessary for analysis of dynamic behavior, as illustrated in the table below (x indicates attributes included in the representation scheme):

.. figure:: figures/figure_BioRECIPE_model_format.png
    :align: center
    :alt: internal figure

|

Model attributes
----------------

The following tables provide details for each attribute, including attribute name used in the BioRECIPE spreadsheet, a symbol used in `detailed definitions <https://melody-biorecipe.readthedocs.io/en/latest/definitions.html#formal-definitions>`_, a brief description of the attribute, its allowed values, and a few examples for the attribute. Model examples can be found `here <https://github.com/pitt-miskov-zivanov-lab/BioRECIPE/blob/main/examples/models>`_. 


The `basic <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#basic-element-attributes>`_ element (node) attributes, and `context <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#context-attributes>`_ attributes are inherited from the interactions in which the element participates (as a regulated element), and they are included in the element representation, as shown in the figure above (columns under **Element** header). 


Several other interaction attributes are ordered lists of values from all individual interactions where the element is a regulated element (target node on the interaction edge). These are referred to as **Regulation** attributes and include basic and provenance attributes combined from indvidual interactions (`basic <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#basic-interaction-attributes>`_ interaction attributes and `provenance <https://melody-biorecipe.readthedocs.io/en/latest/bio_interactions.html#provenance-attributes>`_ attributes).

| 

.. csv-table:: Regulation attributes - basic
    :header: Attribute, Symbol, Description, Format, Examples
    :widths: 10, 10, 40, 25, 15

    Positive regulator list, ":math:`a^{\mathrm{posreglist}}`", "All positive regulators of the element from individual interactions, combined into a list", "<positive regulator 1>, <positive regulator 2>, ..., <positive regulator :math:`k`>", "PDPK1pn_cytoPCC"
    Positive connection type list, ":math:`a^{\mathrm{posconnectiontypelist}}`", "All connection types of element's positive regulators from individual interactions, combined into a list, following the same order as in the positive regulator list", "<positive connection type 1>, <positive connection type 2>, ..., <positive connection type :math:`k`>", "direct"
    Positive mechanism list, ":math:`a^{\mathrm{posmechanismlist}}`", "All mechanisms of element's positive regulators from individual interactions, combined into a list, following the same order as in the positive regulator list", "<positive mechanism 1>, <positive mechanism 2>, ..., <positive mechanism :math:`k`>", "phosphorylation"
    Positive site list, ":math:`a^{\mathrm{possitelist}}`", "All interaction sites of element's positive regulators from individual interactions, combined into a list, following the same order as in the positive regulator list", "<positive site 1>, <positive site 2>, ..., <positive site :math:`k`>", "T308"
    Negative regulator list, ":math:`a^{\mathrm{negreglist}}`", "All negative regulators of the element from individual interactions, combined into a list", "<negative regulator 1>, <negative regulator 2>, ..., <negative regulator :math:`l`>", "ICMTpn_erPCC,PP2Apf_cytoPCC"
    Negative connection type list, ":math:`a^{\mathrm{negconnectiontypelist}}`", "All connection types of element's negative regulators from individual interactions, combined into a list, following the same order as in the negative regulator list", "<negative connection type 1>, <negative connection type 2>, ..., <negative connection type :math:`l`>", "indirect,direct"
    Negative mechanism list, ":math:`a^{\mathrm{negmechanismlist}}`", "All mechanisms of element's negative regulators from individual interactions, combined into a list, following the same order as in the negative regulator list", "<negative mechanism 1>, <negative mechanism 2>, ..., <negative mechanism :math:`l`>", "N/A,dephosphorylation"
    Negative site list, ":math:`a^{\mathrm{negsitelist}}`", "All interaction sites of element's negative regulators from individual interactions, combined into a list, following the same order as in the negative regulator list", "<negative site 1>, <negative site 2>, ..., <negative site :math:`l`>", "N/A,T308"

|

.. csv-table:: Regulation attributes - provenance
    :header: Attribute, Symbol, Description, Format, Examples
    :widths: 10, 10, 40, 25, 15

    Score list, ":math:`a^{\mathrm{scorelist}}`", "all scores of element's positive and negative regulations from individual interactions, combined into a list, following the order of positive and then negative regulator lists", "<score 1>, <score 2>, ..., <score :math:`k+l`>", "1,1,1"
    Source list, ":math:`a^{\mathrm{sourcelist}}`", "all sources of element's positive and negative regulations from individual interactions, combined into a list, following the order of positive and then negative regulator lists", "<source 1>, <source 2>, ..., <source :math:`k+l`>", "literature,literature,literature"
    Statements list, ":math:`a^{\mathrm{statementslist}}`", "all support statements of element's positive and negative regulations from individual interactions, combined into a list, following the order of positive and then negative regulator lists", "<statements 1>, <statements 2>, ..., <statements :math:`k+l`>", "Akt is phosphorylated at its residue Thr308 by the 3-phosphoinositide-dependent protein kinase 1 (PDK1),'We find that PFKFB4 interacts with ICMT, a posttranslational modifier of RAS. PFKFB4 promotes ICMT/RAS interaction, controls RAS localization at the plasma membrane, activates AKT signaling and enhances cell migration.','The protein phosphatase 2A (PP2A) has long been known to negatively regulate Akt activity.'"
    Paper IDs list, ":math:`a^{\mathrm{paperIDslist}}`", "all paper IDs (where statements are found) of element's positive and negative regulations from individual interactions, combined into a list, following the order of positive and then negative regulator lists", "<paper IDs 1>, <paper IDs 2>, ..., <paper IDs :math:`k+l`>", "PMC6518649,PMC9348664,PMC10332018"

|

Whenever an individual regulator (positive or negative) has an *empty* attribute value, this is indicated with ``None`` in the list of attribute values. 

|

Finally, several new model attributes are included in executable models to define element update rules, as well as element value and timing parameters for the simulation. These attributes are included under **Simulation parameters** in the figure above.

|

.. csv-table:: Simulation attributes - rule
    :header: Attribute, Symbol, Description, Format or Values, Examples
    :widths: 10, 10, 40, 25, 15

     Variable, ":math:`a^{\mathrm{variable}}`", "Variable name assigned to model element used by simulators and other software", <variable_name>, "AKTpf_cytoPCC"
     Positive regulation rule, ":math:`a^{\mathrm{posregrule}}`", "A rule used in simulation to compute the level of element's positive regulation", "<string>  //The rules for creating these positive regulation strings are written separately.", "PDPK1pn_cytoPCC"
     Negative regulation rule, ":math:`a^{\mathrm{negregurule}}`", "A rule used in simulation to compute the level of element's negative regulation", "<string>  //The rules for creating these negative regulation strings are written separately.", "ICMTpn_erPCC,PP2Apf_cytoPCC"

|

.. csv-table:: Simulation attributes - value
    :header: Attribute, Symbol, Description, Format or Values, Examples
    :widths: 10, 10, 40, 25, 15
    
    Value type, ":math:`a^{\mathrm{valuetype}}`", "Type of value used for interpretting model outcomes", ``amount`` | ``activity``, "amount"
    Levels, ":math:`a^{\mathrm{levels}}`", "Number of different levels (values) an element can be assigned; or infinite if a continuous variable", <number of distinct levels> | ``inf``, "4"
    State list number, ":math:`a^{\mathrm{statelist}}`", "State list used in simulation to initialize the element and assign values throughout simulation; multiple state lists can be included and numbered, starting from 0", "<value>,<value>[time],...,<value>[time]", "1"
    Const OFF, ":math:`a^{\mathrm{constOFF}}`", "Indicates whether the element is assumed to be at the lowest allowed level (usually 0) for the entire simulation", empty | :math:`\checkmark`, "value you choose"
    Const ON, ":math:`a^{\mathrm{constON}}`", "Indicates whether the element is assumed to be at the highest allowed level for the entire simulation", empty | :math:`\checkmark`, "value you choose"
    Increment, ":math:`a^{\mathrm{increment}}`", "When the element can have more than two different levels, an increment indicates by how many levels it is allowed to increase or decrease in a single time step", ":math:`\Delta \mathrm{value}`", "1"

|

.. csv-table:: Simulation attributes - timing 
    :header: Attribute, Symbol, Description, Format or Values, Examples
    :widths: 10, 10, 40, 25, 15


    Spontaneous, ":math:`a^{\mathrm{spontaneous}}`", "Specifies spontaneous behavior of the element, if it has only positive or only negative regulators", <non-negative integer> | ``None``, "None"
    Balancing, ":math:`a^{\mathrm{balancing}}`", "Specifies the behavior of the element when its positive and negative regulation levels are equal", "{``increase``, <non-negative integer>}  | {``decrease``, <non-negative integer>} | ``None``", "decrease,0"
    Delay, ":math:`a^{\mathrm{delay}}`", description, definition, "0,0,100,0,0"
    Update group, ":math:`a^{\mathrm{updategroup}}`", description, definition, "1"
    Update rate, ":math:`a^{\mathrm{updaterate}}`", description, definition, "1"
    Update rank, ":math:`a^{\mathrm{updaterank}}`", description, definition, "1"


