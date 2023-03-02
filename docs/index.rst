Welcome to BioRECIPE's documentation!
=======================================
.. image:: https://readthedocs.org/projects/melody-biorecipe/badge/?version=latest
    :target: https://melody-biorecipe.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

The BioRECIPE representation format was introduced to facilitate seamless human-machine interaction while creating, verifying, evaluating, curating, and expanding executable models of intra- and intercellular signaling when studying immune system and diseases. This format allows a human user to easily preview and modify any model components, while it is at the same time readable by machines and can be processed by a range of model development and analysis tools. The BioRECIPE format is a tabular format used for models that have a directed graph as their underlying structure.

Graph Structure and Attributes
----------------------------------
The components of a directed graph :math:`G(V,E)`, and the attributes of these components relevant for modeling intracellular networks, are defined as follows.

========================================   ============
Notation                                    Definition
========================================   ============
:math:`V=\{v_1,v_2,…,v_N\}`                 a set of N nodes :math:`v_i, (i=1,...,N)`, each assigned to one model element, where each element represents a component of the system being modeled
:math:`E=\{e_1,e_2,…,e_M\}`                 a set of M directed edges :math:`e_j, (j=1,...,M)`, each assigned to an interaction between elements
:math:`v_i=v(a_i^v)`                        each node :math:`v_i` has an attribute vector :math:`a^v≡(a^{name},a^{type},a^{subtype},a^{database},a^{ID},a^{location},a^{locationID})`
:math:`e_j=e(V_{s_j},v_{t_j},a_j^e)`        each edge :math:`e_j` has one or more source nodes in a set :math:`V_{s_j}`, a target node :math:`v_{t_j}`, and an attribute vector :math:`a^e≡(a^{sign},a^{connectiontype},a^{mechanism},a^{site},a^{cellline},a^{celltype},a^{tissuetype},a^{organism},a^{score},a^{source},a^{statements},a^{paperIDs})`
========================================   ============

Biological Interactions
----------------------------------
Here, we provide formal definitions of the components of a biological interaction, and the attributes of this components.

.. admonition:: Definition 1...

An element (node), v=v(a^v ), is defined by its name, type, and unique identifier (ID) and these attributes are written as a vector a^v=(a^name,a^type,a^ID ).

The attribute a^name is an element name, usually following the standard nomenclature used by biologists and in the literature (e.g., acronym ERK1 is used instead of a longer name “extracellular signal-regulated kinase 1”). The attribute a^type represents element type, usually genes, RNAs, proteins, chemicals, or biological processes. Biological entity names often have multiple synonyms (e.g., ERK1 may also be referred to as MAPK3), and therefore, unique identifiers (IDs) are used, which are stored in attribute a^ID. These IDs can be obtained from standard databases such as UniProt [5], PubChem [6], or the Gene Ontology Databases (GO) [7].
In addition to these three required attributes, the node attribute vector a^v may also include other attributes that help describe the element. For example, attributes a^location and a^locationID hold information about the cellular compartment where the element is found and the compartment ID, respectively. We use the GO database to obtain these location IDs [7]. A subtype attribute, a^subtype, may be used to indicate additional type of an element, such as a^subtype = “receptor” for an element with a^type = “protein”. Additionally, the unique ID attribute may be split into two attributes, the name of the database from which the ID is retrieved, a^database, and the ID, a^ID.

.. admonition:: Definition 2...

A directed signed interaction (also referred to as a directed edge) e=e(v_s,v_t,a^e) is defined with its source element v_s, target element v_t, and vector of attributes a^e. The interaction attribute vector always includes at least the sign a^sign and connection type a^connectiontype attributes: a^e=(a^sign,a^connectiontype). The direction of an interaction is always implicitly defined with source and target nodes, and therefore, not explicitly listed among its attributes.

The a^sign attribute indicates the sign (also referred to as polarity) of the influences, and it can take two values, a^sign= “positive” (e.g., activation) or a^sign= “negative” (e.g., inhibition). Sometimes, only the information about indirect influences on pathways of interest is known, and therefore, the attribute a^connectiontype is used to indicate whether the interaction e is a direct physical interaction (a^connectiontype = “direct”) or an indirect influence from the source node to the target node (a^connectiontype = “indirect”). Since the interaction definition allows for indirect interactions, it is possible that source and target node are not in the same compartment, and this is the reason we assign the location attribute to nodes and not to the interaction.
The list of other attributes is not necessarily fixed; the components in it may vary, dependent on the goals of the analysis. A more specific information about the biological mechanism and the molecular site of an interaction can be included in the a^mechanism and the a^site attributes, respectively. We note here that, in some cases, a^sign is not explicitly stated in statements about influences that describe mechanisms (e.g., A phosphorylates B). In this case, it would be up to the user to either fill in this information from other sources or accept a default attribute assignment. For example, the default assignment could be “positive” for phosphorylation, although this may not always be the case, and would require curation.
The edge attribute vector can also include the a^cellline, a^celltype, a^tissuetype, a^organism attributes, which hold the context information about the cell line, cell type, tissue type, and organism where the interaction is observed, respectively.
Finally, provenance attributes can be used. The a^score attribute provides a summary score for confidence in the interaction, or the amount of available evidence for the interaction. The a^source attribute indicates the source of evidence, which can be literature, expert knowledge, databases, or data. The a^statement attribute is used to store the statements, parts of sentences or sentences where the interaction is mentioned. The a^paperIDs attribute holds paper IDs (e.g., PMCID [8]) where the sentences mentioning the interaction are found. When the information about the additional non-essential attributes is not available, these attributes are assigned an “empty” value.
In Figure 1, we show an example biological interaction, with all node and edge attributes.

.. image:: Figure1.png

Figure 1: An example biological interaction represented as a directed signed edge between two nodes, including node, edge, context, and provenance attributes.


The table below summarizes the node and edge attributes in a directed graph G(V,E):

Representation of Individual Events and Interactions
-----------------------------------------------------

The BioRECIPE format supports individual event and interaction representation for:
- events that are retrieved in an automated manner by NLP-based machine readers
- interactions found in interaction databases
- interactions inferred from data
- interactions entered manually by experts.

In the BioRECIPE format, a list of interactions is written such that each interaction is one row in a table (or a spreadsheet) and attributes are assigned to columns, as illustrated below:

Model Structure and Attributes
-------------------------------

Here, we provide a formal definition of a model structure and attributes, as well as a definition of a path.

.. admonition:: Definition 3...

The static structure of a model can be defined as a directed graph G(V,E), where V={v_1,v_2,…,v_N } is a set of nodes, and each node v_i=v(a_i^v )  (i=1..N) is one model element, while E={e_1,e_2,…,e_M } is a set of directed edges, and an edge e_j=e(v_(s_j ),v_(t_j ),a_j^e) 〖(v〗_(s_j ),v_(t_j )∈V,j=1..M) indicates a directed interaction between elements v_(s_j ) and v_(t_j ), in which source node v_(s_j ) influences target node v_(t_j ). Vectors a_i^v and a_j^e are formed following the definitions of node and edge attribute vectors.

.. admonition:: Definition 4...

An input node is a node that is not a target node of any edge in the model, and an output node is a node that is not a source node of any edge in the model.

We also refer to input and output nodes as “hanging” from the rest of the model, and they are often important for modeling outcomes: input nodes are used as pathway catalysts, and output nodes can represent model outcomes.

.. admonition:: Definition 5...

We define a path in a model as n>1 connected edges: p(v_(s_p ),v_(t_p ),a^(〖sign〗_p ) )=(e(v_(k_1 )=v_(s_p ),v_(k_2 ),a_(k_1)^e),e(v_(k_2 ),v_(k_3 ),a_(k_2)^e),…,e(v_(k_n ),v_(k_(n+1) ) 〖=v〗_(t_p ),a_(k_n)^e)). The direction of the path is implicitly defined with the source node v_(s_p ) and target node v_(t_p ). The regulation sign a^(〖sign〗_p ) is considered positive when the number of negative signs in the set {a_(k_1)^sign,a_(k_2)^sign,..,a_(k_n)^sign} is even, and negative when this number is odd. Cycles and feedback loops may be defined in cases where the path source is also the path target, i.e., p(v_(s_p ),v_(s_p ),a^(〖sign〗_p )).

For example, in Figure 2, on the path from source node v_6 to target node v_13, the number of negative regulations is odd, due to only one negative regulation from node v_8 to v_9, and so the sign of this overall path is negative.



Figure 2. A toy example of a model graph, showing input and output nodes, directed edges, paths, feedback and feedforward loops, and cellular compartments used for location. An edge example and a path example with notation details. (ER-endoplasmic reticulum)



	Element-based modeling approach definitions

In element-based modeling of biological systems [30-33], an element represents a biomolecular species (and in some cases even a biological process) and all reactions that lead to changes in a single species are lumped together within the corresponding element’s update rule. Therefore, a model is a collection of element update rules, each update rule is associated with a different model element, which can be more formally defined as follows.

Definition 6. An element-based model is a triple M(G,X,F), where G(V,E) is a network structure of the model (defined earlier in Definition 3), X ={x_1,x_2,…,x_N} is a set of N state variables corresponding to nodes in V={v_1,v_2,…,v_N }, and F={f_1,f_2,…,f_N} is a set of N regulatory (update) functions such that each element v_i ÎV has a corresponding function f_i ÎF.

Definition 7. For each element v_i∈V, its state variable x_i∈X can take any value from a set or an interval of values X_i.

Definition 8. For each element v_i, any element v_j that influences the state of v_i such that the function f_i is sensitive to the value of x_j is called a regulator of v_i.

Definition 9. For each element v_i, an influence set, denoted as V_i^influence Í V, consists of all regulators of v_i. We will refer to the set of state variables that correspond to the elements in V_i^influence as X_i^influence.

Definition 10. The next state of element v_i, denoted as x_i^*, is computed given current states of all elements in its influence set, that is, given values of all variables in X_i^influence:
x_i^*=f_i (X_i^influence ).

In general, functions in F can have different types, discrete or continuous, and moreover, individual elements within the same model could have very different update functions, thus forming hybrid models. The set or interval of possible values, X_i, assigned to each model element x_i can also vary. The function and element types are usually decided based on the knowledge or the information available about the modeled system and its components.
The element-based modeling approach can represent indirect influences between elements, and it can model systems where the knowledge about element interaction mechanisms is incomplete. Using element update rules in simulations allows for studies of cell dynamics, state transitions, and feedback loops [34, 35], and does not require full knowledge of the interaction mechanisms [36]. Element-based models can also allow for integration of both prior knowledge and data [13, 37, 38] and analysis of hybrid networks (systems involving protein-protein interactions, gene regulations, and/or metabolic pathways) [39].
An example of element-based models are discrete models, where each element state variable x_i is assigned a discrete set of values [38]. Following Definition 7, x_i can take any value from the set X_i:{0,1,2,…,n_i-1}, where n_i is the number of different states that element, v_i can have. Often, these different states represent different levels of activity or concentration for element v_i. Element update functions in discrete models can be of different type, some examples are min and max functions, and (rounded) weighted sums.
Boolean models are a subset of discrete models [29, 30, 40], where elements can have only two values, 0 (also referred to as OFF or False) or 1 (also referred to as ON or True). In Boolean models, value 0 represents states such as “inactive”, “absent”, or “low concentration” and value 1 represents states such as “active”, “present”, or “high concentration”. Element update functions in these models are Boolean functions where logic operators such as AND, OR, and NOT are used [31]. As an extension of Boolean networks, in the Probabilistic Boolean Network (PBN), randomness is introduced by assigning multiple candidate Boolean functions to the variables. At each time step during simulation, one of element’s candidate functions is chosen at random to determine its state [41, 42].
Other examples of commonly used element-based models are Bayesian Networks [35, 43] and Dynamic Bayesian Networks [34]. Bayesian networks introduce probability distributions into the governing rules of elements, increasing the freedom in updating element states. Similar to Bayesian Networks are structural equation models (SEMs) [44].
Given that the element-based modeling approach can be used for indirect influences and it can abstract away from detailed reaction mechanisms, additional methods have been introduced to account for the timing in biological systems, rates at which elements change, or delays in element updating and delays in pathways [38].

.. toctree::
   :maxdepth: 2
   :caption: Contents

   Legal
