import tkinter as tk
from observers.observateur import Observateur


class ObservateurValeurPortfolio(Observateur):
    def __init__(self, label_valeur: tk.Label, label_variation: tk.Label):
        super().__init__()
        self.label_valeur = label_valeur
        self.label_variation = label_variation

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()
        if not donnees:
            self.label_valeur.config(text="Valeur totale : 0.00 $")
            self.label_variation.config(text="")
            return

        valeur_totale = 0.0
        valeur_ouverture = 0.0

        for info in donnees.values():
            qte = info.get("quantite", 0)
            prix = info.get("prix", 0.0)
            ouverture = info.get("ouverture", 0.0)

            valeur_totale += prix * qte
            valeur_ouverture += ouverture * qte

        variation = valeur_totale - valeur_ouverture
        symbole = "▲" if variation >= 0 else "▼"
        couleur = "green" if variation >= 0 else "red"

        self.label_valeur.config(text=f"Valeur totale : {valeur_totale:.2f} $")
        self.label_variation.config(
            text=f"{symbole} {abs(variation):.2f} $ depuis l'ouverture",
            fg=couleur
        )