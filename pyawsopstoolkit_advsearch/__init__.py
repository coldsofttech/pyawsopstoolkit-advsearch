__all__ = [
    "AND",
    "OR",
    "LESS_THAN",
    "LESS_THAN_OR_EQUAL_TO",
    "GREATER_THAN",
    "GREATER_THAN_OR_EQUAL_TO",
    "EQUAL_TO",
    "NOT_EQUAL_TO",
    "BETWEEN",
    "iam",
    "ec2"
]
__name__ = "pyawsopstoolkit_advsearch"
__version__ = "0.1.1"
__description__ = """
This package delivers an exhaustive array of advanced search functionalities tailor-made for seamless integration with
AWS (Amazon Web Services). Meticulously engineered, these advanced searches are finely tuned to meet the distinctive
demands inherent to the expansive AWS ecosystem, encompassing a diverse spectrum of facets.
"""

from pyawsopstoolkit_advsearch.search import AND, OR, LESS_THAN, LESS_THAN_OR_EQUAL_TO, GREATER_THAN, \
    GREATER_THAN_OR_EQUAL_TO, EQUAL_TO, NOT_EQUAL_TO, BETWEEN
