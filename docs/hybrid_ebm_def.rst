############################################################################
Hybrid Element-based Modeling Approach Definitions
############################################################################

In element-based modeling of biological systems, an element represents a biomolecular species (and in some cases even a biological process) and all reactions that lead to changes in a single species are lumped together within the corresponding element’s update rule. A hybrid element-based model can be more formally defined as follows.

.. admonition:: Definition 3

 The static structure of a model can be defined as a directed graph :math:`G(V,E)`, where :math:`V=\{v_1,v_2,...,v_N\}` is a set of nodes, and each node :math:`v_i=v(\mathbf{a}_i^v) (i=1,...,N)` is one model element, while :math:`E=\{e_1,e_2,...,e_M\}` is a set of directed edges, and an edge :math:`e_j=e(v_{s_j},v_{t_j},\mathbf{a}_j^e), (v_{s_j},v_{t_j}\in V,j=1,...,M)` indicates a directed interaction between elements :math:`v_{s_j}` and :math:`v_{t_j}`, in which source node :math:`v_{s_j}` influences target node :math:`v_{t_j}`. Vectors :math:`\mathbf{a}_i^v` and :math:`\mathbf{a}_j^e` are formed following the definitions of node and edge attribute vectors.

.. admonition:: Definition 4

 An input node is a node that is not a target node of any edge in the model, and an output node is a node that is not a source node of any edge in the model.

We also refer to input and output nodes as “hanging” from the rest of the model, and they are often important for modeling outcomes: input nodes are used as pathway catalysts, and output nodes can represent model outcomes.

.. admonition:: Definition 5

 We define a path in a model as :math:`n>1` connected edges: :math:`p(v_{s_p},v_{t_p},a^{\mathrm{sign}_p})=(e(v_{k_1}=v_{s_p},v_{k_2},\mathbf{a}_{k_1}^e),e(v_{k_2},v_{k_3},\mathbf{a}_{k_2}^e),...,e(v_{k_n},v_{k_{n+1}}=v_{t_p},\mathbf{a}_{k_n}^e))`. The direction of the path is implicitly defined with the source node :math:`v_{s_p}` and target node :math:`v_{t_p}`. The regulation sign :math:`a^{\mathrm{sign}_p}` is considered positive when the number of negative signs in the set :math:`\{a_{k_1}^{\mathrm{sign}},a_{k_2}^{\mathrm{sign}},...,a_{k_n}^{\mathrm{sign}}\}` is even, and negative when this number is odd. Cycles and feedback loops may be defined in cases where the path source is also the path target, i.e., :math:`p(v_{s_p},v_{s_p},a^{\mathrm{sign}_p})`.

For example, in :numref:`figure_toy_model_graph`, on the path from source node :math:`v_6` to target node :math:`v_{13}`, the number of negative regulations is odd, due to only one negative regulation from node :math:`v_8` to :math:`v_9`, and so the sign of this overall path is negative.

.. admonition:: Definition 6

 An element-based model is a triple :math:`\mathcal{M}(G,\mathcal{X},\mathcal{F})`, where :math:`G(V,E)` is a network structure of the model (defined earlier in Definition 3), :math:`\mathcal{X}=\{x_1,x_2,...,x_N\}` is a set of :math:`N` state variables corresponding to nodes in :math:`V=\{v_1,v_2,...,v_N\}`, and :math:`\mathcal{F}=\{f_1,f_2,...,f_N\}` is a set of :math:`N` regulatory (update) functions such that each element :math:`v_i \in V` has a corresponding function :math:`f_i \in \mathcal{F}`.

.. admonition:: Definition 7

 For each element :math:`v_i \in V`, its state variable :math:`x_i \in \mathcal{X}` can take any value from a set or an interval of values :math:`X_i`. The state variable :math:`x_i \in X` can represent either the amount or activity of :math:`v_i`, represented with attribute :math:`a^{\mathrm{valuetype}}`.

.. admonition:: Definition 8

 When :math:`\mathbb{X}_i` is a set of discrete values, :math:`|\mathbb{X}_i|` is referred to as the number of levels of :math:`v_i`, represented with attribute :math:`a^{\mathrm{levels}}`.

.. admonition:: Definition 9

 A source node :math:`v_j` of an edge in graph :math:`G(V,E)` that has :math:`v_i` as a target node is called a regulator of :math:`v_i`. In other words, for each element :math:`v_i`, any element :math:`v_j` that influences the state of :math:`v_i` such that the function :math:`f_i` is sensitive to the value of :math:`x_j` is called a regulator of :math:`v_i`.

.. admonition:: Definition 10

 For each element :math:`v_i`, an influence set, denoted as :math:`V_i^{\mathrm{influence}} \in V`, consists of all regulators of :math:`v_i`. The state variables that correspond to the elements in :math:`V_i^{\mathrm{influence}}` form set :math:`\mathcal{X}_i^{\mathrm{influence}}`

.. admonition:: Definition 11

 Any element :math:`v_j \in V_i^{\mathrm{influence}}`, for which the edge :math:`e(v_j,v_i,\mathbf{a}^e)` has a positive sign, :math:`a_e^{\mathrm{sign}}` = ``positive``, also belongs to the positive list of regulators of element :math:`v_i`, denoted as :math:`v_j \in V_i^{\mathrm{influence},+} \subset V_i^{\mathrm{influence}}`, represented with attribute :math:`a^{\mathrm{poslist}}`.

.. admonition:: Definition 12

 The state variables :math:`x_j` that correspond to elements in :math:`V_i^{\mathrm{influence},+}` form set :math:`X_i^{\mathrm{influence},+} \subset X_i^{\mathrm{influence}}`, and are used for creating a positive regulation rule for :math:`v_i`, represented with attribute :math:`a^{\mathrm{posregulation}}`.

.. admonition:: Definition 13

 Any element :math:`v_j \in V_i^{\mathrm{influence}}`, for which the edge :math:`e(v_j,v_i,\mathbf{a}^e)` has a negative sign, :math:`a_e^{\mathrm{sign}}` = ``negative``, also belongs to the negative list of regulators of element :math:`v_i`, denoted as :math:`v_j \in V_i^{\mathrm{influence},-} \subset V_i^{\mathrm{influence}}`, represented with attribute :math:`a^{\mathrm{neglist}}`.

.. admonition:: Definition 14

 The state variables :math:`x_j` that correspond to elements in :math:`V_i^{\mathrm{influence},-}` form set :math:`X_i^{\mathrm{influence},-} \subset X_i^{\mathrm{influence}}`, and are used for creating a negative regulation rule for :math:`v_i`, represented with attribute :math:`a^{\mathrm{negregulation}}`.

.. admonition:: Definition 15

 An array of :math:`k` state values :math:`X_i^{t_0},X_i^{t_1},X_i^{t_2},...,X_i^{t_{k-1}}` that are assigned to :math:`v_i` at :math:`\{t_0,t_1,t_2,...,t_{k-1}\}` time steps during simulation, where :math:`t_0` is the initial time step, and :math:`t_0<t_1<t_2<...<t_{k-1}`, is called state list and is represented with attribute :math:`a^{\mathrm{statelist}}`.

.. admonition:: Definition 16

 When the state variable :math:`x_i` has a constant 0 value throughout the entire simulation, this is referred to as a constant OFF state, and represented with attribute :math:`a^{\mathrm{a^constOFF}}`.

.. admonition:: Definition 17

 When the state variable :math:`x_i` has a constant non-0 value (e.g., the highest value from :math:`X_i`) throughout the entire simulation, this is referred to as a constant ON state, and represented with attribute :math:`a^{\mathrm{constON}}`.

.. admonition:: Definition 18

 The next state of element :math:`v_i`, denoted as :math:`x_i^{*}`, is computed given current states of all elements in its influence set, that is, given values of all variables in :math:`X_i^{\mathrm{influence}}`: :math:`x_i^{*}=f_i(X_i^{\mathrm{influence}})`.

In general, functions in :math:`\mathcal{F}` can have different types, discrete or continuous, and moreover, individual elements within the same model could have very different update functions, thus forming hybrid models. The set or interval of possible values, :math:`X_i`, assigned to each model element :math:`x_i` can also vary. The function and element types are usually decided based on the knowledge or the information available about the modeled system and its components.

The element-based modeling approach can represent indirect influences between elements, and it can model systems where the knowledge about element interaction mechanisms is incomplete. Using element update rules in simulations allows for studies of cell dynamics, state transitions, and feedback loops, and does not require full knowledge of the interaction mechanisms. Element-based models can also allow for integration of both prior knowledge and data and analysis of hybrid networks (systems involving protein-protein interactions, gene regulations, and/or metabolic pathways).

An example of element-based models are discrete models, where each element state variable :math:`x_i` is assigned a discrete set of values. Following Definition 7, :math:`x_i` can take any value from the set :math:`X_i:\{0,1,2,…,n_{i-1}\}`, where :math:`n_i` is the number of different states that element, :math:`v_i` can have. Often, these different states represent different levels of activity or concentration for element :math:`v_i`. Element update functions in discrete models can be of different type, some examples are ``min`` and ``max`` functions, and (rounded) weighted sums.

Boolean models are a subset of discrete models, where elements can have only two values, ``0`` (also referred to as OFF or False) or ``1`` (also referred to as ON or True). In Boolean models, value ``0`` represents states such as “inactive”, “absent”, or “low concentration” and value ``1`` represents states such as “active”, “present”, or “high concentration”. Element update functions in these models are Boolean functions where logic operators such as AND, OR, and NOT are used. As an extension of Boolean networks, in the Probabilistic Boolean Network (PBN), randomness is introduced by assigning multiple candidate Boolean functions to the variables. At each time step during simulation, one of element’s candidate functions is chosen at random to determine its state.

Other examples of commonly used element-based models are Bayesian Networks and Dynamic Bayesian Networks. Bayesian networks introduce probability distributions into the governing rules of elements, increasing the freedom in updating element states. Similar to Bayesian Networks are structural equation models (SEMs).

Given that the element-based modeling approach can be used for indirect influences and it can abstract away from detailed reaction mechanisms, additional methods have been introduced to account for the timing in biological systems, rates at which elements change, or delays in element updating and delays in pathways.
