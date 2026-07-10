import json
import os
import webbrowser
import requests
import customtkinter as ctk
from tkinter import messagebox

# Configuration de base et fichier de sauvegarde
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "theme_color": "green",
    "bg_color": "#0B0F12",
    "youtube_url": "https://www.youtube.com/watch?v=jfKfPfyJRdk" # Lofi de base
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

class ModernApiApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.config = load_config()
        
        # Configuration de la fenêtre
        self.title("Brix API - Nexus Terminal")
        self.geometry("850x600")
        self.configure(fg_color=self.config["bg_color"])
        
        # Effet d'opacité/translucidité (0.0 à 1.0)
        self.attributes("-alpha", 0.93) 
        
        # Thème CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme(self.config["theme_color"])

        # API Setup
        self.API_URL = "https://api.brix.example.com/api/v1/search" # À remplacer par la vraie URL
        self.API_KEY = "brix_pKc5Fr7NJw9LGN1mlv_0f9baNblBGcobG4u2ATRtBnNUK1iY"

        self.init_ui()

    def init_ui(self):
        # --- STYLE DU CURSEUR ---
        # "pirate", "heart", "crosshair" (viseur), "circle" ou "arrow"
        self.configure(cursor="crosshair") 

        # --- TITRE ---
        self.title_label = ctk.CTkLabel(self, text="⚡ BRIX SEARCH TERMINAL ⚡", font=ctk.CTkFont(family="Courier", size=24, weight="bold"))
        self.title_label.pack(pady=20)

        # --- ZONE DE RECHERCHE (TRANSLUCIDE / SOMBRE) ---
        self.search_frame = ctk.CTkFrame(self, fg_color="#12181D", border_color="#00FF66", border_width=1)
        self.search_frame.pack(fill="x", padx=40, pady=10)

        # Inputs
        self.entry_nom = ctk.CTkEntry(self.search_frame, placeholder_text="Nom de famille", width=150)
        self.entry_nom.grid(row=0, column=0, padx=10, pady=15)

        self.entry_prenom = ctk.CTkEntry(self.search_frame, placeholder_text="Prénom", width=150)
        self.entry_prenom.grid(row=0, column=1, padx=10, pady=15)

        self.entry_ville = ctk.CTkEntry(self.search_frame, placeholder_text="Ville (ex: Paris)", width=150)
        self.entry_ville.grid(row=0, column=2, padx=10, pady=15)

        self.btn_search = ctk.CTkButton(self.search_frame, text="RUN SEARCH", font=ctk.CTkFont(weight="bold"), command=self.execute_search)
        self.btn_search.grid(row=0, column=3, padx=10, pady=15)

        # --- ZONE DES RÉSULTATS ---
        self.result_display = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Courier", size=12), fg_color="#070A0E", border_color="#222", border_width=1)
        self.result_display.pack(fill="both", expand=True, padx=40, pady=10)
        self.result_display.insert("0.0", "[System] En attente de requêtes...\n")

        # --- PANNEL DE CONFIGURATION (BAS) ---
        self.config_frame = ctk.CTkFrame(self, height=50, fg_color="transparent")
        self.config_frame.pack(fill="x", padx=40, pady=20)

        # Bouton Couleur
        self.btn_theme = ctk.CTkButton(self.config_frame, text="Changer Couleur", width=120, fg_color="#222", text_color="#FFF", command=self.toggle_color)
        self.btn_theme.pack(side="left", padx=5)

        # Entrée YouTube
        self.entry_yt = ctk.CTkEntry(self.config_frame, placeholder_text="Lien YouTube Musique", width=300)
        self.entry_yt.insert(0, self.config["youtube_url"])
        self.entry_yt.pack(side="left", padx=10)

        self.btn_play = ctk.CTkButton(self.config_frame, text="▶ Jouer Musique", width=100, command=self.play_music)
        self.btn_play.pack(side="left", padx=5)

    def execute_search(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        ville = self.entry_ville.get()

        if not nom or not prenom:
            messagebox.showwarning("Champs manquants", "Veuillez entrer au moins un nom et un prénom.")
            return

        self.result_display.delete("0.0", "end")
        self.result_display.insert("end", f"[~] Connexion à l'API Brix en cours...\n")
        
        headers = {"X-API-Key": self.API_KEY, "Content-Type": "application/json"}
        payload = {"nom_famille": nom, "prenom": prenom, "ville": ville, "flexible": True}

        try:
            # Simulation ou requête réelle
            # Changez l'URL par votre vraie URL de production
            response = requests.post(self.API_URL, headers=headers, json=payload, timeout=10)
            
            # Code de test si l'URL n'est pas encore active :
            if response.status_code == 404: 
                # On simule la réponse reçue dans votre exemple pour la démo
                data = {
                    "results": [{
                        "nom_famille": nom, "prenom": prenom, "email": f"{prenom.lower()}.{nom.lower()}@email.com",
                        "telephone": "0612345678", "ville": ville, "_sources": ["Free (2024)", "Bouygues (2025)"], "_confidence": 85
                    }]
                }
            else:
                data = response.json().get("data", {})

            results = data.get("results", [])
            
            if not results:
                self.result_display.insert("end", "[-] Aucun résultat trouvé.\n")
                return

            for res in results:
                self.result_display.insert("end", f"\n[✔] RÉSULTAT TROUVÉ :\n")
                self.result_display.insert("end", f" ├─ Nom : {res.get('nom_famille')} {res.get('prenom')}\n")
                self.result_display.insert("end", f" ├─ Email : {res.get('email')}\n")
                self.result_display.insert("end", f" ├─ Tél : {res.get('telephone')}\n")
                self.result_display.insert("end", f" ├─ Ville : {res.get('ville')}\n")
                self.result_display.insert("end", f" ├─ Sources : {', '.join(res.get('_sources', []))}\n")
                self.result_display.insert("end", f" └─ Confiance : {res.get('_confidence') Black}%\n")

        except Exception as e:
            self.result_display.insert("end", f"[!] Erreur de connexion : {str(e)}\n")

    def toggle_color(self):
        # Alterne entre le vert (Hacker) et le bleu (Cyber)
        if self.config["theme_color"] == "green":
            self.config["theme_color"] = "blue"
            self.search_frame.configure(border_color="#0066FF")
        else:
            self.config["theme_color"] = "green"
            self.search_frame.configure(border_color="#00FF66")
            
        save_config(self.config)
        ctk.set_default_color_theme(self.config["theme_color"])
        self.result_display.insert("end", "[System] Thème mis à jour. Redémarrez pour appliquer la couleur des boutons.\n")

    def play_music(self):
        url = self.entry_yt.get()
        if url:
            self.config["youtube_url"] = url
            save_config(self.config)
            self.result_display.insert("end", f"[System] Lancement de la musique dans le navigateur...\n")
            webbrowser.open(url)

if __name__ == "__main__":
    app = ModernApiApp()
    app.mainloop()
