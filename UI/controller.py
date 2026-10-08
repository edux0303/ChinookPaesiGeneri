import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view.txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    def fillDDGeneri(self):              # punto 1a: riempie il menu "Genere"
        for a,b in self._model.getGeneri():
            self._view._ddGenere.options.append(ft.dropdown.Option(key=str(a), text=b))


    def handleCreaGrafo(self, e):        # punto 1b/1c
        self._view.txt_result.controls.clear()

        idGenere = self._view._ddGenere.value
        if idGenere is None:
            self._errore("Selezionare un genere!")
            return

        self._model.buildGraph(int(idGenere))
        self._view.txt_result.controls.append(ft.Text("Grafo creato!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        # riempio i due menu dei paesi (servono per il punto 2)
        self._view._ddPartenza.options.clear()
        self._view._ddArrivo.options.clear()
        self._view._ddPartenza.value = None
        self._view._ddArrivo.value = None
        for p in sorted(self._model.getNodes(), key=str):
            self._view._ddPartenza.options.append(ft.dropdown.Option(str(p)))
            self._view._ddArrivo.options.append(ft.dropdown.Option(str(p)))

        self._view.update_page()

    def handlePaesiMigliori(self, e):    # punto 1d
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        self._view.txt_result.controls.append(ft.Text("I 5 paesi migliori:"))
        i = 1
        for paese, diff in self._model.getPaesiMigliori():
            self._view.txt_result.controls.append(ft.Text(f"{i}. {paese} ({diff})"))
            i += 1
        self._view.update_page()

    def handleCammino(self, e):          # punto 2
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # i due paesi
        if self._view._ddPartenza.value is None or self._view._ddArrivo.value is None:
            self._errore("Selezionare il paese di partenza e quello di arrivo!")
            return
        partenza = self._model.idMap.get(self._view._ddPartenza.value)
        arrivo = self._model.idMap.get(self._view._ddArrivo.value)
        if partenza is None or arrivo is None:
            self._errore("Paese non trovato!")
            return
        if partenza == arrivo:
            self._errore("Partenza e arrivo devono essere paesi diversi!")
            return

        # la lunghezza
        lun = self._view._txtLun.value
        if lun is None or lun == "":
            self._errore("Inserire la lunghezza del cammino!")
            return
        try:
            lun = int(lun)
        except ValueError:
            self._errore("La lunghezza deve essere un numero intero!")
            return
        if lun <= 0:
            self._errore("La lunghezza deve essere maggiore di 0!")
            return
        if lun > self._model.getNumNodi() - 1:
            self._errore("Lunghezza troppo grande: un cammino senza vertici ripetuti "
                         "non può avere più archi dei paesi meno uno!")
            return

        cammino, pesoTot = self._model.getCammino(partenza, arrivo, lun)
        if len(cammino) == 0:
            self._errore(f"Nessun cammino di lunghezza {lun} da {partenza} a {arrivo}!")
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Cammino ottimo da {partenza} a {arrivo} con {lun} archi:"))
        for i in range(len(cammino) - 1):
            peso = self._model.getPeso(cammino[i], cammino[i + 1])
            self._view.txt_result.controls.append(
                ft.Text(f"{cammino[i]} --> {cammino[i + 1]} (peso {peso})"))
        self._view.txt_result.controls.append(ft.Text(f"Somma dei pesi: {pesoTot}"))
        self._view.update_page()