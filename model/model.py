import networkx as nx

import database.dao


class Model:
    def __init__(self):
        self.dao = database.dao.DAO
        self.grafo = nx.DiGraph()
        self._id_gene_cromosoma_dict = {}


    def crea_grafo(self):
        interazioni = self.dao.get_interazioni()
        print(interazioni)
        geni = self.dao.get_geni()
        #print(geni)
        lista_nodi = []

        for gene in geni:
            self._id_gene_cromosoma_dict[gene.id] = gene
            if gene.cromosoma not in lista_nodi and gene.cromosoma != 0:
                lista_nodi.append(gene.cromosoma)
        print(self._id_gene_cromosoma_dict)

        lista_zero = []
        for gene in geni:
            if gene.cromosoma == 0:
                lista_zero.append(gene.id)

        self.grafo.add_nodes_from(lista_nodi)

        interazioni_visitate = []
        for interazione in interazioni:
            if interazione.id_gene1 not in lista_zero and interazione.id_gene2 not in lista_zero:
                if interazione.id_gene1 in self._id_gene_cromosoma_dict and interazione.id_gene2 in self._id_gene_cromosoma_dict:
                    if self._id_gene_cromosoma_dict[interazione.id_gene1].cromosoma != self._id_gene_cromosoma_dict[interazione.id_gene2].cromosoma and (self._id_gene_cromosoma_dict[interazione.id_gene1].cromosoma, self._id_gene_cromosoma_dict[interazione.id_gene2].cromosoma) not in self.grafo.edges:
                        self.grafo.add_edge(self._id_gene_cromosoma_dict[interazione.id_gene1].cromosoma, self._id_gene_cromosoma_dict[interazione.id_gene2].cromosoma, peso = interazione.correlazione)
                    elif self._id_gene_cromosoma_dict[interazione.id_gene1].cromosoma != self._id_gene_cromosoma_dict[interazione.id_gene2].cromosoma and (self._id_gene_cromosoma_dict[interazione.id_gene1].cromosoma, self._id_gene_cromosoma_dict[interazione.id_gene2].cromosoma) in self.grafo.edges:
                        for arco in self.grafo.edges(data=True):
                            peso = arco[2]["peso"] + interazione.correlazione
                            self.grafo.add_edge(self._id_gene_cromosoma_dict[interazione.id_gene1].cromosoma, self._id_gene_cromosoma_dict[interazione.id_gene2].cromosoma, peso = peso)
        print(self.grafo)
        pesi = []
        for arco in self.grafo.edges(data=True):
            pesi.append(float(arco[2]["peso"]))
        minimo =min(pesi)
        massimo = max(pesi)
        return len(self.grafo.nodes), len(self.grafo.edges), minimo, massimo

