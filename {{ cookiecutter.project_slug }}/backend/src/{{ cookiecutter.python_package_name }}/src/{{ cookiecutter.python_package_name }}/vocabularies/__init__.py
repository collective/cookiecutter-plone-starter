from {{ cookiecutter.python_package_name }} import _
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


INDUSTRIES = [
    ("government", _("Government")),
    ("ngo", _("NGO")),
    ("edu", _("Education")),
]


@provider(IVocabularyFactory)
def industries_vocabulary(context):
    """Vocabulary of industries."""
    terms = []
    for id_, title in INDUSTRIES:
        terms.append(SimpleTerm(id_, id_, title))
    return SimpleVocabulary(terms)
