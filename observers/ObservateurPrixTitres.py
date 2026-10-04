import tkinter as tk
from observers.observateur import Observateur


class ObservateurPrixTitres(Observateur):
    def __init__(self, frame_prix: tk.LabelFrame):
        super().__init__()
        self.frame_prix = frame_prix
        self.labels_prix = {}
        self.frames_prix = {}

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()
        if not donnees:
            for frame in self.frames_prix.values():
                frame.destroy()
            self.labels_prix.clear()
            self.frames_prix.clear()
            return

        tickers_actuels = set(donnees.keys())
        tickers_obsoletes = set(self.frames_prix.keys()) - tickers_actuels
        for ticker in tickers_obsoletes:
            self.frames_prix[ticker].destroy()
            del self.frames_prix[ticker]
            del self.labels_prix[ticker]

        for ticker, info in donnees.items():
            prix = info.get("prix", 0.0)
            ouverture = info.get("ouverture", 0.0)
            variation = ((prix - ouverture) / ouverture * 100) if ouverture else 0.0
            symbole = "▲" if variation >= 0 else "▼"
            couleur = "green" if variation >= 0 else "red"
            texte = f"{prix:.2f} $  {symbole} {abs(variation):.2f}%"

            if ticker not in self.labels_prix:
                frame = tk.Frame(self.frame_prix)
                frame.pack(fill=tk.X, pady=2)

                tk.Label(
                    frame,
                    text=f"{ticker}:",
                    width=8,
                    font=("Segoe UI", 10, "bold"),
                    anchor="w"
                ).pack(side=tk.LEFT)

                label = tk.Label(frame, text=texte, fg=couleur)
                label.pack(side=tk.LEFT)

                self.frames_prix[ticker] = frame
                self.labels_prix[ticker] = label
            else:
                self.labels_prix[ticker].config(text=texte, fg=couleur)
