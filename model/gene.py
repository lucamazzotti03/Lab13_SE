from dataclasses import dataclass


@dataclass
class Gene:
    id : int
    funzione: str
    essenziale: str
    cromosoma: str