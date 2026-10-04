import csv
from datetime import datetime
from observers.observateur import Observateur


class Logger(Observateur):
    def __init__(self, fichier_csv="portfolio_log.csv"):
        super().__init__()
        self.fichier_csv = fichier_csv

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()
        if not donnees:
            return

        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.fichier_csv, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for ticker, info in donnees.items():
                writer.writerow([
                    horodatage,
                    ticker,
                    info.get("prix"),
                    info.get("ouverture")
                ])