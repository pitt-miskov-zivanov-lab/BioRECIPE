# -*- coding: utf-8 -*-
#
# This file is a part of INDRA translator for BioRECIPE format.
#
# __author__ = "Difei Tang"
# __email__ = "DIT18@pitt.edu"

import pandas as pd
import math
from indra.statements import *

# TODO: map to INDRA statments representing post-translational modifications
# TODO: add database attributes to db_ref
stmts_mapping = {
    "phosphorylation": Phosphorylation,
    "dephosphorylation": Dephosphorylation,
    "ubiquitination": Ubiquitination,
    "activation": Activation,
    "inhibition": Inhibition,
    "increaseamount": IncreaseAmount,
    "DecreaseAmount": DecreaseAmount
}


class INDRA():
    """INDRA processor
    """

    def biorecipeI_stmts(self, infile, outfile):
        """Translate BioRECIPE interaction lists to INDRA statements """

        df = pd.read_excel(infile, dtype=">U50", keep_default_na=False)

        stmts = []
        for i in range(len(df)):
            t = df.loc[i, 'Regulated Name']
            s = df.loc[i, 'Regulator Name']
            sign = df.loc[i, 'Sign']
            m = df.loc[i, 'Mechanism']

            ta = Agent(t)
            sa = Agent(s)

            if not m and m.lower() not in stmts_mapping.keys():
                # default statements decided by interaction sign
                if sign == 'positive':
                    stmt = Activation(ta, sa)
                elif sign == 'negative':
                    stmt = Inhibition(ta, sa)
                else:
                    raise ValueError('Invalid value was found in Sign column')
            else:
                # find an indra statement
                  stmt = stmts_mapping[m.lower()](ta, sa)

            stmts.append(stmt)

            # TODO: other output formats
            stmts_to_json_file(stmts, outfile)

