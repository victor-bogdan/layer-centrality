from enum import Enum


class CentralityMeasure(Enum):
    Degree = 1,
    Harmonic = 2,
    Katz = 3,
    Subgraph = 4
