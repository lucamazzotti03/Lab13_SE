import networkx as nx

import database.dao


class Model:
    def __init__(self):
        self.dao = database.dao.DAO
        self.grafo = nx.DiGraph()
        self._id_gene_cromosoma_dict = {}


    def crea_grafo(self):
        self.grafo.clear()
        interazioni = self.dao.get_interazioni()
        geni = self.dao.get_geni()
        lista_nodi = []

        for gene in geni:
            self._id_gene_cromosoma_dict[gene.id] = gene
            if gene.cromosoma not in lista_nodi and gene.cromosoma != 0:
                lista_nodi.append(gene.cromosoma)


        self.grafo.add_nodes_from(lista_nodi)

        interazioni_visitate = []
        for interazione in interazioni:
            if interazione.id_gene1 in self._id_gene_cromosoma_dict and interazione.id_gene2 in self._id_gene_cromosoma_dict:
                c1 = self._id_gene_cromosoma_dict[interazione.id_gene1].cromosoma
                c2 = self._id_gene_cromosoma_dict[interazione.id_gene2].cromosoma
                if c1 != c2:
                    if self.grafo.has_edge(c1, c2):
                        self.grafo[c1][c2]["peso"] += interazione.correlazione
                    else:
                        self.grafo.add_edge(c1, c2, peso = interazione.correlazione)


        pesi = []
        for arco in self.grafo.edges(data=True):
            pesi.append(float(arco[2]["peso"]))
        minimo =min(pesi)
        massimo = max(pesi)
        return len(self.grafo.nodes), len(self.grafo.edges), minimo, massimo

    def get_edges(self):
        return self.grafo.edges

    def ricerca_cammino_massimo(self, soglia):
        self.percorso_ottimo = []
        self.peso = 0
        nodi = list(self.grafo.nodes)
        for nodo_iniziale in nodi:
            self.ricorsione(soglia, parziale = [nodo_iniziale], peso_corrente = 0)
        print(self.percorso_ottimo)
        return self.percorso_ottimo

    def ricorsione(self, soglia, parziale, peso_corrente):

        if peso_corrente > self.peso:
            self.peso = peso_corrente
            self.percorso_ottimo = parziale.copy()

        ultimo = parziale[-1]
        vicini = [
            v for v in self.grafo.neighbors(ultimo)
            if self.grafo[ultimo][v]["peso"] > soglia
        ]

        for vicino in vicini:
            peso = self.grafo[ultimo][vicino]["peso"]

            # controllo arco già usato (NON orientato)
            arco_usato = False
            for i in range(len(parziale) - 1):
                a = parziale[i]
                b = parziale[i + 1]
                if (a == ultimo and b == vicino) or (a == vicino and b == ultimo):
                    arco_usato = True
                    break

            if arco_usato:
                continue

            parziale.append(vicino)
            self.ricorsione(soglia, parziale, peso_corrente + peso)
            parziale.pop()







