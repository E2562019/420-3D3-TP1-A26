
import tkinter as tk
from tkinter import messagebox
from models.Portfolio import Portfolio
from observers.Logger import Logger
from observers.ObservateurAlertes import ObservateurAlertes
from observers.ObservateurPrixTitres import ObservateurPrixTitres
from observers.ObservateurValeurPortfolio import ObservateurValeurPortfolio


class Dashboard(tk.Tk):
    def __init__(self, portfolio: Portfolio):
        super().__init__()
        self.portfolio = portfolio
        self.title("Tableau de bord - Gestion de Portefeuille")
        self.geometry("600x650")
        self.resizable(False, False)
        self._creer_interface()
        self._initialiser_observateurs()
        self._rafraichissement_automatique()

    def _creer_interface(self) -> None:

        frame_form = tk.LabelFrame(self, text="Gestion des Titres", padx=10, pady=10)
        frame_form.pack(fill=tk.X, padx=15, pady=10)


        tk.Label(frame_form, text="Titre (ex: AAPL):").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_ticker = tk.Entry(frame_form, width=10)
        self.entry_ticker.grid(row=0, column=1, pady=2, padx=5)

        tk.Label(frame_form, text="Quantité:").grid(row=0, column=2, sticky="w", pady=2)
        self.entry_quantite = tk.Entry(frame_form, width=8)
        self.entry_quantite.grid(row=0, column=3, pady=2, padx=5)

        tk.Label(frame_form, text="Seuil Bas ($):").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_seuil_bas = tk.Entry(frame_form, width=10)
        self.entry_seuil_bas.grid(row=1, column=1, pady=2, padx=5)

        tk.Label(frame_form, text="Seuil Haut ($):").grid(row=1, column=2, sticky="w", pady=2)
        self.entry_seuil_haut = tk.Entry(frame_form, width=8)
        self.entry_seuil_haut.grid(row=1, column=3, pady=2, padx=5)

        frame_boutons = tk.Frame(frame_form)
        frame_boutons.grid(row=2, column=0, columnspan=4, pady=10)

        btn_ajouter = tk.Button(frame_boutons, text="Ajouter / Modifier", command=self._action_ajouter)
        btn_ajouter.pack(side=tk.LEFT, padx=5)

        btn_supprimer = tk.Button(frame_boutons, text="Supprimer", command=self._action_supprimer)
        btn_supprimer.pack(side=tk.LEFT, padx=5)

        btn_rafraichir = tk.Button(frame_boutons, text="🔄 Rafraîchir", command=self.portfolio.rafraichir)
        btn_rafraichir.pack(side=tk.LEFT, padx=5)

        frame_valeur = tk.Frame(self, padx=10, pady=5)
        frame_valeur.pack(fill=tk.X, padx=15)

        self.lbl_valeur_totale = tk.Label(frame_valeur, text="Valeur totale : 0.00 $", font=("Segoe UI", 12, "bold"))
        self.lbl_valeur_totale.pack(anchor="w")

        self.lbl_variation = tk.Label(frame_valeur, text="", font=("Segoe UI", 10))
        self.lbl_variation.pack(anchor="w")


        self.frame_prix = tk.LabelFrame(self, text="Prix en Temps Réel", padx=10, pady=10)
        self.frame_prix.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)


        frame_alertes = tk.LabelFrame(self, text="Alertes de Seuils", padx=10, pady=10)
        frame_alertes.pack(fill=tk.X, padx=15, pady=10)

        self.lbl_alertes = tk.Label(frame_alertes, text="Aucune alerte", fg="gray", justify=tk.LEFT)
        self.lbl_alertes.pack(anchor="w")

    def _initialiser_observateurs(self) -> None:
        self.obs_logger = Logger(fichier_csv="portfolio_log.csv")
        self.obs_valeur = ObservateurValeurPortfolio(self.lbl_valeur_totale, self.lbl_variation)
        self.obs_prix = ObservateurPrixTitres(self.frame_prix)
        self.obs_alertes = ObservateurAlertes(self.lbl_alertes)

        self.portfolio.abonner(self.obs_logger)
        self.portfolio.abonner(self.obs_valeur)
        self.portfolio.abonner(self.obs_prix)
        self.portfolio.abonner(self.obs_alertes)

    def _action_ajouter(self) -> None:
        ticker = self.entry_ticker.get().strip()
        quantite_str = self.entry_quantite.get().strip()
        bas_str = self.entry_seuil_bas.get().strip()
        haut_str = self.entry_seuil_haut.get().strip()

        if not ticker or not quantite_str:
            messagebox.showwarning("Saisie invalide", "Veuillez entrer un ticker et une quantité.")
            return

        try:
            quantite = int(quantite_str)
            seuil_bas = float(bas_str) if bas_str else None
            seuil_haut = float(haut_str) if haut_str else None
        except ValueError:
            messagebox.showerror("Erreur", "La quantité doit être un entier et les seuils des nombres valides.")
            return

        self.portfolio.ajouter_titre(ticker, quantite, seuil_bas=seuil_bas, seuil_haut=seuil_haut)
        self.portfolio.rafraichir()
        self.entry_ticker.delete(0, tk.END)
        self.entry_quantite.delete(0, tk.END)
        self.entry_seuil_bas.delete(0, tk.END)
        self.entry_seuil_haut.delete(0, tk.END)

    def _action_supprimer(self) -> None:
        ticker = self.entry_ticker.get().strip()
        if not ticker:
            messagebox.showwarning("Saisie invalide", "Entrez le ticker à supprimer.")
            return

        self.portfolio.supprimer_titre(ticker)
        self.portfolio.rafraichir()
        self.entry_ticker.delete(0, tk.END)
    def _rafraichissement_automatique(self) -> None:
        if self.portfolio.titres:
            self.portfolio.rafraichir()
        self.after(30000, self._rafraichissement_automatique)