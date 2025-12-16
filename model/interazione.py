from dataclasses import dataclass


@dataclass
class Interazione:
    id_gene1 : str
    id_gene2 : str
    tipo : str
    correlazione : int
