# -*- coding: utf-8 -*-
#
# This file is a part of translator for BioRECIPE format.
#
# __author__ = "Difei Tang"
# __email__ = "DIT18@pitt.edu"

import networkx as nx
from translators.utils import get_model, model_to_networkx

class SIF():
    """SBMLQual processor
    """

    def biorecipeM_sif(self, input_file, output_file):
        """Translate BioRECIPE model to SIF"""
        df_model = get_model(input_file)
        graph = model_to_networkx(df_model)

        self.write_sif(output_file, graph)

    def write_sif(self, sbml_filename: str, graph: nx.DiGraph):
        """Write a SIF file.

        http://www.cbmc.it/fastcent/doc/SifFormat.htm
        """
        with open(sbml_filename, "w", encoding="utf-8", newline="") as f:

            for source, target, sign in graph.edges.data("interaction"):
                print(
                    source.replace(" ", "_"),
                    sign.upper(),
                    target.replace(" ", "_"),
                    file=f,
                )

    def biorecipeI_sif(self, input_file, output_file):
        """Translate BioRECIPE interaction lists to SIF"""
        pass

    def sif_biorecipeI(self, input_file, output_file):
        """Translate SIF to BioRECIPE interaction lists """
        pass


