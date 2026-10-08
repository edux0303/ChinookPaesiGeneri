"""
DAO - CHINOOK: PAESI E GENERI

Parti della consegna che riguardano il DAO:

PUNTO 1
a. L'utente seleziona da un menu a tendina un genere musicale. Il menu va
   riempito all'avvio interrogando il database, con i generi in ordine
   alfabetico.                                               -> getGeneri()

b. I vertici sono tutti i paesi in cui risiede almeno un cliente.
                                                             -> getNodi()

c. Per ogni paese si calcoli il numero di brani del genere selezionato
   acquistati dai suoi clienti (somma del campo Quantity).   -> getVendite()
   Gli archi NON si leggono dal database: si calcolano nel Model confrontando
   i "venduti" dei paesi a due a due.

Percorso delle tabelle per getVendite:
   customer --CustomerId-- invoice --InvoiceId-- invoiceline --TrackId-- track
   (Country)                                     (Quantity)              (GenreId)
"""

from database.DB_connect import DBConnect
from model.paese import Paese


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getGeneri():
        """
        PUNTO 1a - generi per il menu a tendina, in ordine alfabetico.
        Restituisce una lista di coppie (id, nome).
        Nel controller: key=str(id), text=nome.
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT g.GenreId AS id, g.Name AS nome
            FROM genre g
            ORDER BY g.Name
        """
        cursor.execute(query)
        for row in cursor:
            result.append((row["id"], row["nome"]))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getNodi():
        """
        PUNTO 1b - vertici: tutti i paesi in cui risiede almeno un cliente.
        Solo la tabella customer: cosi' ci sono anche i paesi che non hanno
        comprato il genere scelto (resteranno isolati).
        Restituisce una lista di oggetti Paese, con venduti = 0.
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT DISTINCT c.Country AS paese
            FROM customer c
        """
        cursor.execute(query)
        for row in cursor:
            result.append(Paese(row["paese"]))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getVendite(idGenere):
        """
        PUNTO 1c - per ogni paese, numero di brani del genere scelto acquistati
        dai suoi clienti (somma di Quantity).
        Restituisce SOLO i paesi che hanno comprato almeno un brano del genere,
        come coppie (nomePaese, venduti).
        Gli altri paesi restano con venduti = 0 nel Model.
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT c.Country AS paese, SUM(il.Quantity) AS venduti
            FROM customer c, invoice i, invoiceline il, track t
            WHERE c.CustomerId = i.CustomerId
              AND i.InvoiceId = il.InvoiceId
              AND il.TrackId = t.TrackId
              AND t.GenreId = %s
            GROUP BY c.Country
        """
        cursor.execute(query, (idGenere,))
        for row in cursor:
            result.append((row["paese"], int(row["venduti"])))
        cursor.close()
        cnx.close()
        return result