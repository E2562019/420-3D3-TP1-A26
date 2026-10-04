from models.sujet import Sujet
import yfinance as yf

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
            t = yf.Ticker(ticker)
            prix = t.fast_info['lastPrice']
            ouverture = t.fast_info['open']

            donnees[ticker] = {
                "quantite": quantite,
                "prix": round(prix, 2),
                "ouverture": round(ouverture, 2)
            }
        return donnees