from automata.fa.fa import FA

from .mixins.analyse import AnalyseMixin
from .mixins.conversions import ConversionMixin
from .mixins.grammaire import GrammaireMixin
from .mixins.visualisation import VisualisationMixin


class ExtendedFA(
    AnalyseMixin,
    ConversionMixin,
    GrammaireMixin,
    VisualisationMixin,
    FA
):
    """
    Classe de base pour les automates finis étendus.

    Elle regroupe les fonctionnalités d'analyse,
    de conversion, de grammaire et de visualisation.
    """

    pass