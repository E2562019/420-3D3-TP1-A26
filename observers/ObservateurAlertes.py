import tkinter as tk
from observers.observateur import Observateur


class ObservateurAlertes(Observateur):
    def __init__(self, label_alertes: tk.Label):
        super().__init__()
        self.label_alertes = label_alertes

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()
        if not donnees:
            self.label_alertes.config(text="Aucune alerte", fg="gray")
            return

        alertes = []
        for ticker, info in donnees.items():
            prix = info.get("prix", 0.0)
            seuil_haut = info.get("seuil_haut")
            seuil_bas = info.get("seuil_bas")

            if seuil_haut is not None and prix >= seuil_haut:
                alertes.append(f"⚠️ {ticker} dépasse le seuil haut ({prix:.2f} $ ≥ {seuil_haut:.2f} $)")
            elif seuil_bas is not None and prix <= seuil_bas:
                alertes.append(f"⚠️ {ticker} sous le seuil bas ({prix:.2f} $ ≤ {seuil_bas:.2f} $)")

        if alertes:
            self.label_alertes.config(text="\n".join(alertes), fg="red")
        else:
            self.label_alertes.config(text="Aucune alerte", fg="gray")