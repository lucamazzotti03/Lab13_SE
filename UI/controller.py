import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.nodi = None
        self.archi = None


    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        self._view.lista_visualizzazione_1.clean()
        self.nodi, self.archi,minimo, massimo =self._model.crea_grafo()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Numero di vertici:{self.nodi} Numero di archi: {self.archi}"))
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"valore minimo:{minimo} valore massimo: {massimo}"))
        self._view.page.update()


    def handle_conta_edges(self, e):
        """ Handler per gestire il conteggio degli archi """""
        # TODO
        lista = []
        archi = self._model.get_edges()
        for arco in archi(data=True):
            if float(arco[2]["peso"]) < float(self._view.txt_name.value):
                lista.append(arco)

        maggiore = len(archi)-len(lista)
        self._view.lista_visualizzazione_2.clean()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Numero di archi con peso Maggiore della soglia: {maggiore}"))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Numero di archi con peso Minore della soglia: {len(lista)}"))
        self._view.page.update()


    def handle_ricerca(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """""
        # TODO

        cammino_massimo = self._model.ricerca_cammino_massimo(float(self._view.txt_name.value))
        self._view.lista_visualizzazione_3.clean()
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Numero di archi percorso più lungo: {len(cammino_massimo)-1}"))
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Peso cammino massimo: {self._model.peso}"))
        for i in range(len(cammino_massimo)-1):
            u = cammino_massimo[i]
            v = cammino_massimo[i+1]
            peso = self._model.grafo[u][v]["peso"]
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"{u}-->{v}: {peso}"))
        self._view.page.update()
