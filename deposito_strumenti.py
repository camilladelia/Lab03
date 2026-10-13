from operator import attrgetter
class Strumento:
    # Il metodo __init__ è il costruttore: viene chiamato quando creiamo un nuovo strumento
    def __init__(self, id_strumento, tipo, marca, anno_acquisto, valore):
        self.id_strumento = id_strumento
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = int(anno_acquisto)  # assicuriamoci che sia un numero intero
        self.valore = float(valore)  # assicuriamoci che sia un numero con la virgola

    # Metodo "dunder" (double underscore) per la rappresentazione in formato stringa
    def __str__(self):
        return f"[{self.id_strumento}] {self.tipo} {self.marca} - Anno: {self.anno_acquisto}, Valore: {self.valore}€"


class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"Prestito {self.id_prestito}: Strumento {self.id_strumento} all'allievo {self.cognome_allievo} (dal {self.data})"

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self._responsabile = responsabile
        # Creiamo due dizionari vuoti pronti per essere riempiti
        self.strumenti = {}
        self.prestiti = {}

        # Aggiungiamo i metodi Getter e Setter per il responsabile richiesti dal testo

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, nuovo_nome):
        self._responsabile = nuovo_nome

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        # Il blocco 'try' serve per dire a Python: "Prova a fare queste operazioni"
        try:
            # 'with open' apre il file e si assicura di chiuderlo in automatico alla fine
            with open(file_path, 'r', encoding='utf-8') as file:
                # Leggiamo il file riga per riga
                for linea in file:
                    # strip() toglie gli "a capo" invisibili a fine riga
                    # split(',') taglia la riga in una lista ogni volta che trova una virgola
                    dati = linea.strip().split(',')

                    # Controlliamo che la riga sia corretta e abbia i 5 dati attesi
                    if len(dati) == 5:
                        # Estraiamo i 5 dati dalla lista
                        id_str, tipo, marca, anno, valore = dati

                        # Creiamo l'oggetto usando il nostro "stampo" Strumento (creato nel Blocco 1)
                        nuovo_strumento = Strumento(id_str, tipo, marca, anno, valore)

                        # Salviamo lo strumento nel dizionario usando il suo ID come chiave (es. 'S1')
                        self.strumenti[id_str] = nuovo_strumento

        # Se 'try' fallisce perché il file non c'è, Python passa a questo blocco 'except'
        except FileNotFoundError:
            # L'istruzione 'raise' forza l'interruzione e lancia l'errore richiesto dalla prof
            raise FileNotFoundError(f"Errore: Il file '{file_path}' non è stato trovato.")# Il blocco 'try' serve per dire a Python: "Prova a fare queste operazioni"

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        if not self.strumenti:
            nuovo_numero = 1
        else:
            # Estraiamo tutti i numeri dagli ID esistenti (es. da "S10" prendiamo "10" e lo convertiamo in intero)
            numeri_id = [int(id_strum[1:]) for id_strum in self.strumenti.keys()]
            # Troviamo il valore massimo tra i numeri esistenti e aggiungiamo 1
            nuovo_numero = max(numeri_id) + 1

            # Creiamo il nuovo ID unendo la lettera 'S' e il numero progressivo (es. "S11")
        nuovo_id = f"S{nuovo_numero}"

        # Creiamo l'oggetto Strumento sfruttando la nostra classe modello
        nuovo_strumento = Strumento(nuovo_id, tipo, marca, anno_acquisto, valore)

        # Salviamo lo strumento nel nostro dizionario usando l'ID come chiave
        self.strumenti[nuovo_id] = nuovo_strumento

        # Restituiamo il riferimento all'oggetto appena creato, come richiesto dalla consegna
        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        lista_strumenti = list(self.strumenti.values())
        # 2. Ordiniamo la lista usando 'sorted' e specificando come chiave l'attributo 'marca' tramite attrgetter
        lista_ordinata = sorted(lista_strumenti, key=attrgetter('marca'))
        # 3. Restituiamo la lista ordinata pronta per essere stampata dal main
        return lista_ordinata

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # 1. Controlliamo se lo strumento esiste nel deposito
        if id_strumento not in self.strumenti:
            raise Exception(f"Errore: Lo strumento {id_strumento} non esiste nel sistema.")

        # 2. Controlliamo se lo strumento è già in prestito esaminando i prestiti attivi
        for prestito in self.prestiti.values():
            if prestito.id_strumento == id_strumento:
                raise Exception(f"Errore: Lo strumento {id_strumento} è già in prestito.")

        # 3. Generiamo automaticamente l'ID del prestito (P1, P2, P3...) con la stessa logica degli strumenti
        if not self.prestiti:
            nuovo_numero = 1
        else:
            numeri_id = [int(id_pres[1:]) for id_pres in self.prestiti.keys()]
            nuovo_numero = max(numeri_id) + 1
        nuovo_id = f"P{nuovo_numero}"

        # 4. Creiamo l'oggetto Prestito e lo salviamo nel dizionario dei prestiti
        nuovo_prestito = Prestito(nuovo_id, data, id_strumento, cognome_allievo)
        self.prestiti[nuovo_id] = nuovo_prestito
        # Restituiamo il riferimento al prestito creato
        return nuovo_prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        # Verifichiamo se l'ID del prestito esiste nel dizionario
        if id_prestito in self.prestiti:
            # L'istruzione 'del' cancella la chiave e il valore corrispondente dal dizionario
            del self.prestiti[id_prestito]
        else:
            # Se non esiste, scateniamo un'eccezione di errore
            raise Exception(f"Errore: Nessun prestito trovato con ID {id_prestito}.")
