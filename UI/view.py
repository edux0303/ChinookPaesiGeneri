import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "TdP - Paesi e generi"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None
        self.txt_result = None

    def load_interface(self):
        self._page.controls.append(
            ft.Text("TdP - Chinook: paesi e generi", color="blue", size=24))

        # ---------- RIGA 1: genere + crea grafo + paesi migliori (PUNTO 1) ----------
        self._ddGenere = ft.Dropdown(label="Genere", width=250)
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo",
                                               on_click=self._controller.handleCreaGrafo, width=200)
        self._btnMigliori = ft.ElevatedButton(text="Paesi migliori",
                                              on_click=self._controller.handlePaesiMigliori, width=200)
        row1 = ft.Row([self._ddGenere, self._btnCreaGrafo, self._btnMigliori],
                      alignment=ft.MainAxisAlignment.CENTER)

        # ---------- RIGA 2: partenza + arrivo + lunghezza + cerca cammino (PUNTO 2) ----------
        self._ddPartenza = ft.Dropdown(label="Paese di partenza", width=200)
        self._ddArrivo = ft.Dropdown(label="Paese di arrivo", width=200)
        self._txtLun = ft.TextField(label="Lunghezza cammino", width=180)
        self._btnCammino = ft.ElevatedButton(text="Cerca cammino",
                                             on_click=self._controller.handleCammino, width=180)
        row2 = ft.Row([self._ddPartenza, self._ddArrivo, self._txtLun, self._btnCammino],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)
        self._page.controls.append(row2)

        # ---------- area risultati ----------
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)

        # riempio il menu dei generi all'avvio (punto 1a)
        self._controller.fillDDGeneri()

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()