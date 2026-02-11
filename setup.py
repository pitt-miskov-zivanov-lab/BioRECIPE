from setuptools import setup

setup(
    name='biorecipe',
    version='0.0.1',
    packages=[
        'translators',
        'translators.sbml',
        'translators.sbmlqual',
        'translators.SIF',
        'translators.biopax',
        'translators.indra_engine',
        'translators.reach_engine',
        'translators.within_biorecipe',
    ],

    install_requires=[
        'pandas',
        'python-libsbml',
        'loguru',
        'openpyxl',
        'sympy==1.12',
        'lxml',
        'bs4',
        'nltk',
        'casq==1.2.0',
        'numpy',
        'indra==1.23',
        'gilda',
        'pybiopax',
        'bioregistry',
    ],

)
