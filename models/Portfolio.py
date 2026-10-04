import yfinance as yf
from models.sujet import Sujet


class Portfolio(Sujet):
    def __init__(self):
        super().__init__()
        # { ticker: {"quantite": q, "seuil_bas": sb, "seuil_haut": sh} }
        self.titres = {}

    def ajouter_titre(self, ticker: str, quantite: int, seuil_bas: float = None, seuil_haut: float = None) -> None:
        self.titres[ticker.upper()] = {
            "quantite": quantite,
            "seuil_bas": seuil_bas,
            "seuil_haut": seuil_haut
        }

    def supprimer_titre(self, ticker: str) -> None:
        ticker = ticker.upper()
        if ticker in self.titres:
            del self.titres[ticker]

    def rafraichir(self) -> None:
        self.notifier()

    def get_donnees(self) -> dict:
        donnees = {}
        for ticker, config in self.titres.items():
            t = yf.Ticker(ticker)
            prix = t.fast_info['lastPrice']
            ouverture = t.fast_info['open']
            donnees[ticker] = {
                "quantite": config["quantite"],
                "prix": round(prix, 2),
                "ouverture": round(ouverture, 2),
                "seuil_bas": config["seuil_bas"],
                "seuil_haut": config["seuil_haut"]
            }
        return donnees