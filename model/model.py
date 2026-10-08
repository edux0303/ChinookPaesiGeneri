import networkx as nx
from database.DAO import DAO
from itertools import combinations


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._nodes = []
        self.idMap = {}
        self._solBest = []
        self._pesoBest = 0
        self._maxSpesa = 0

        # ---------- PUNTO 1 ----------

    def getGeneri(self):
        return DAO.getGeneri()

    def buildGraph(self, genere):
        self._grafo.clear()
        self.idMap = {}

        self._nodes = DAO.getNodi()
        for n in self._nodes:
            self.idMap[n.nome] = n

        self._grafo.add_nodes_from(self._nodes)

        for s1,s2 in DAO.getVendite(genere):
            if s1 in self.idMap:
                self.idMap[s1].venduti = s2


        for c1, c2 in combinations(self._nodes, 2):
            if c1.venduti == 0 or c2.venduti == 0:
                continue

            peso = c1.venduti +c2.venduti
            if c1.venduti >= c2.venduti:
                self._grafo.add_edge(c1, c2, weight=peso)
            if c2.venduti >= c1.venduti:
                self._grafo.add_edge(c2, c1, weight=peso)

    def getNodes(self):
        return self._nodes

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getPaesiMigliori(self):
        migliori = []

        for p in self._grafo.nodes:
            uscenti = self._grafo.out_degree(p,weight="weight")
            entranti = self._grafo.in_degree(p,weight="weight")
            migliori.append((p,uscenti-entranti))
        migliori.sort(key=lambda x: x[1], reverse=True)
        return migliori[:5]


    def getCammino(self,partenza,arrivo,lun):
        self._solBest = []
        self._pesoBest = 0
        self._ricorsione([partenza],0,arrivo,lun)
        return self._solBest, self._pesoBest

    def _ricorsione(self,parziale,pesoParziale,arrivo,lun):
        if len(parziale) - 1 == lun:
            if parziale[-1] == arrivo and pesoParziale > self._pesoBest:
                self._pesoBest = pesoParziale
                self._solBest = list(parziale)          # COPIA!
            return

        ultimo = parziale[-1]
        for vicino in self._grafo.successors(ultimo):
            if vicino in parziale:
                continue
            peso = self._grafo[ultimo][vicino]["weight"]
            parziale.append(vicino)
            self._ricorsione(parziale,pesoParziale+peso,arrivo,lun)
            parziale.pop()

    def getPeso(self, p1, p2):
        return self._grafo[p1][p2]["weight"]


