from enum import Enum, unique


@unique
class CalibrationType(Enum):
    ALTERNATE_CONJUGATE_GRADIENT = "AlternateConjugateGradient"
    CONJUGATE_GRADIENT = "ConjugateGradient"
    POWELL = "Powell"
    SIMPLEX_NELDER_MEAD = "SimplexNelderMead"
