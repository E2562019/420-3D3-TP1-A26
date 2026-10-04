import yfinance as yf
from models.sujet import Sujet


class Portfolio(Sujet):
    def __init__(self):
        super().__init__()
        self.titres = {}  # { ticker: quantite }

    def ajouter_titre(self, ticker: str, quantite: int) -> None:
        self.titres[ticker.upper()] = quantite

    def supprimer_titre(self, ticker: str) -> None:
        ticker = ticker.upper()
        if ticker in self.titres:
            del self.titres[ticker]

    def rafraichir(self) -> None:
        self.notifier()

    def get_donnees(self) -> dict:
        donnees = {}
        for ticker, quantite in self.titres.items():
            price = yf.Ticker(ticker).fast_info['lastPrice']
            donnees[ticker] = {
                "quantite": quantite,
                "prix": round(price, 2),
                "valeur_totale": round(price * quantite, 2)
            }
        return donnees