from setuptools import setup

setup(
    name='biorecipe',
    version='0.0.1',
    packages=[
        'translators',
        'translators.sbml',
        'translators.sbmlqual',
        'translators.SIF',
        'translators.indra',
        'translators.interactions',
        'translators.STRING'
    ],

    install_requires=[
        'pandas',
        'python-libsbml',
        'loguru',
        'openpyxl',
        'sympy',
        'lxml',
        'bs4',
        'nltk',
        'numpy',
    ],

)

