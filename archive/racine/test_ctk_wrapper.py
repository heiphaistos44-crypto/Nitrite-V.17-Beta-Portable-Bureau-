"""
Test du module wrapper CustomTkinter
Vérifie que tous les widgets fonctionnent correctement
"""

import sys
import os

# Ajouter le dossier src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import customtkinter as ctk
from ctk_wrapper import (
    configure_ctk_theme,
    ModernButton, ModernFrame, ModernLabel, ModernEntry,
    ModernSwitch, ModernProgressBar, ModernSlider,
    ModernScrollableFrame,
    CardFrame, TitleLabel, SecondaryButton,
    SuccessButton, DangerButton, InfoButton,
    create_hover_button, create_info_card,
    NiTriTeTheme
)


class TestApp(ctk.CTk):
    """Application de test pour le wrapper CustomTkinter"""

    def __init__(self):
        super().__init__()

        # Configuration fenêtre
        self.title("Test CustomTkinter Wrapper - NiTriTe V13")
        self.geometry("900x700")
        self.configure(fg_color=NiTriTeTheme.BG_DARK)

        # Configurer thème
        configure_ctk_theme()

        # Créer interface de test
        self.create_test_interface()

    def create_test_interface(self):
        """Crée l'interface de test"""

        # Frame principal scrollable
        main_frame = ModernScrollableFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Titre
        title = TitleLabel(main_frame, text="🧪 Test du Wrapper CustomTkinter")
        title.pack(pady=(0, 20))

        # Section 1: Boutons
        self.create_buttons_section(main_frame)

        # Section 2: Entrées
        self.create_inputs_section(main_frame)

        # Section 3: Contrôles
        self.create_controls_section(main_frame)

        # Section 4: Cartes d'information
        self.create_info_cards_section(main_frame)

    def create_buttons_section(self, parent):
        """Section de test des boutons"""
        card = CardFrame(parent)
        card.pack(fill="x", pady=10)

        TitleLabel(card, text="🔘 Boutons").pack(anchor="w", padx=15, pady=10)

        button_frame = ModernFrame(card, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=10)

        # Bouton primaire
        ModernButton(
            button_frame,
            text="Bouton Primaire",
            command=lambda: self.show_message("Bouton primaire cliqué!")
        ).pack(side="left", padx=5)

        # Bouton secondaire
        SecondaryButton(
            button_frame,
            text="Bouton Secondaire",
            command=lambda: self.show_message("Bouton secondaire cliqué!")
        ).pack(side="left", padx=5)

        # Bouton succès
        SuccessButton(
            button_frame,
            text="✓ Succès",
            command=lambda: self.show_message("Succès!")
        ).pack(side="left", padx=5)

        # Bouton danger
        DangerButton(
            button_frame,
            text="✗ Danger",
            command=lambda: self.show_message("Danger!")
        ).pack(side="left", padx=5)

        # Bouton info
        InfoButton(
            button_frame,
            text="ℹ Info",
            command=lambda: self.show_message("Information!")
        ).pack(side="left", padx=5)

        # Bouton avec hover
        create_hover_button(
            card,
            text="Bouton avec Hover Effect",
            command=lambda: self.show_message("Hover button cliqué!"),
            icon="✨"
        ).pack(padx=15, pady=(0, 10))

    def create_inputs_section(self, parent):
        """Section de test des entrées"""
        card = CardFrame(parent)
        card.pack(fill="x", pady=10)

        TitleLabel(card, text="📝 Entrées").pack(anchor="w", padx=15, pady=10)

        # Entry simple
        ModernLabel(card, text="Champ de saisie:").pack(anchor="w", padx=15, pady=(5, 2))
        entry = ModernEntry(
            card,
            placeholder_text="Entrez du texte ici..."
        )
        entry.pack(fill="x", padx=15, pady=(0, 10))

        # Entry avec valeur par défaut
        ModernLabel(card, text="Avec valeur par défaut:").pack(anchor="w", padx=15, pady=(5, 2))
        entry2 = ModernEntry(card)
        entry2.insert(0, "Valeur par défaut")
        entry2.pack(fill="x", padx=15, pady=(0, 10))

    def create_controls_section(self, parent):
        """Section de test des contrôles"""
        card = CardFrame(parent)
        card.pack(fill="x", pady=10)

        TitleLabel(card, text="🎛️ Contrôles").pack(anchor="w", padx=15, pady=10)

        # Switch
        self.switch_var = ctk.BooleanVar(value=False)
        switch = ModernSwitch(
            card,
            text="Mode activé",
            variable=self.switch_var,
            command=self.on_switch_changed
        )
        switch.pack(anchor="w", padx=15, pady=5)

        # Progress bar
        ModernLabel(card, text="Barre de progression:").pack(anchor="w", padx=15, pady=(10, 5))
        self.progress = ModernProgressBar(card)
        self.progress.pack(fill="x", padx=15, pady=(0, 5))
        self.progress.set(0.6)  # 60%

        # Slider
        ModernLabel(card, text="Slider:").pack(anchor="w", padx=15, pady=(10, 5))
        self.slider = ModernSlider(
            card,
            from_=0,
            to=100,
            command=self.on_slider_changed
        )
        self.slider.pack(fill="x", padx=15, pady=(0, 5))
        self.slider.set(50)

        # Label pour afficher valeur du slider
        self.slider_value_label = ModernLabel(
            card,
            text="Valeur: 50",
            text_color=NiTriTeTheme.ORANGE_PRIMARY
        )
        self.slider_value_label.pack(anchor="w", padx=15, pady=(0, 10))

    def create_info_cards_section(self, parent):
        """Section de test des cartes d'information"""
        TitleLabel(parent, text="📊 Cartes d'information").pack(anchor="w", pady=(10, 5))

        info_frame = ModernFrame(parent, fg_color="transparent")
        info_frame.pack(fill="x", pady=10)

        # Créer plusieurs cartes
        create_info_card(
            info_frame,
            title="Processeur",
            value="Intel Core i7-12700K @ 3.60 GHz",
            icon="⚙️"
        )

        create_info_card(
            info_frame,
            title="Mémoire RAM",
            value="32 GB DDR4",
            icon="💾"
        )

        create_info_card(
            info_frame,
            title="Carte Graphique",
            value="NVIDIA GeForce RTX 3080 - 10 GB VRAM",
            icon="🎮"
        )

        create_info_card(
            info_frame,
            title="Système",
            value="Windows 11 Pro (64-bit)",
            icon="🖥️"
        )

    def show_message(self, message: str):
        """Affiche un message dans le terminal"""
        print(f"[TEST] {message}")

    def on_switch_changed(self):
        """Callback du switch"""
        state = "Activé" if self.switch_var.get() else "Désactivé"
        print(f"[TEST] Switch: {state}")

    def on_slider_changed(self, value):
        """Callback du slider"""
        self.slider_value_label.configure(text=f"Valeur: {int(value)}")
        # Mettre à jour la progress bar en même temps
        self.progress.set(value / 100)


def main():
    """Point d'entrée du test"""
    print("=" * 60)
    print("Test du Wrapper CustomTkinter pour NiTriTe V13")
    print("=" * 60)
    print("\nLancement de l'application de test...")
    print("Vérifiez que tous les widgets s'affichent correctement")
    print("avec le style NiTriTe (orange + noir).\n")

    app = TestApp()
    app.mainloop()


if __name__ == "__main__":
    main()
