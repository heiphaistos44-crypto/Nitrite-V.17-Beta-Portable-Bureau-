"""
Page de paramètres pour NiTriTe V13
Gestion des thèmes, configuration et licences premium
"""

import tkinter as tk
import customtkinter as ctk
import json
import os

try:
    from .themes import ALL_THEMES, get_theme_names, set_current_theme, is_premium_theme, get_free_themes, get_premium_themes
    from .modern_colors import ModernColors, set_corner_radius, get_corner_radius, PremiumManager
    from .translations import get_text, set_language
except ImportError:
    from themes import ALL_THEMES, get_theme_names, set_current_theme, is_premium_theme, get_free_themes, get_premium_themes
    from modern_colors import ModernColors, set_corner_radius, get_corner_radius, PremiumManager
    from translations import get_text, set_language


CONFIG_FILE = "config/app_config.json"


class NewSettingsPage(ctk.CTkFrame):
    """Page Paramètres moderne avec thèmes CustomTkinter et système Premium"""

    def __init__(self, parent, root_window):
        super().__init__(parent, fg_color=ModernColors.BG_DARK, corner_radius=0)
        self.root_window = root_window
        self.config = self._load_config()
        self.current_theme_name = self.config.get('theme', 'Orange NiTriTe')
        self.premium_manager = PremiumManager.get_instance()

        # Appliquer la langue au démarrage
        lang_code = "fr" if self.config.get('language', 'Français') == "Français" else "en"
        set_language(lang_code)

        # Charger le corner radius au démarrage
        corner_radius = self.config.get('corner_radius', 15)
        set_corner_radius(corner_radius)

        self._create_widgets()
        self._setup_mousewheel()

    def _load_config(self):
        """Charger toute la configuration"""
        default_config = {
            'theme': 'Orange NiTriTe',
            'language': 'Français',
            'font_size': 12,
            'ui_scale': 100,  # Pourcentage
            'animations': True,
            'smooth_scroll': True,
            'notifications': True,
            'auto_update': False,
            'corner_radius': 15  # Arrondi des bords
        }
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    # Merge avec les valeurs par défaut
                    return {**default_config, **config}
        except:
            pass
        return default_config

    def _save_config(self):
        """Sauvegarder toute la configuration"""
        try:
            os.makedirs('config', exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Erreur sauvegarde config: {e}")

    def _create_widgets(self):
        """Créer les widgets de la page"""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))

        title_label = ctk.CTkLabel(
            header,
            text=get_text("settings_themes"),
            font=("Segoe UI", 24, "bold"),
            text_color=ModernColors.TEXT_PRIMARY
        )
        title_label.pack(side=tk.LEFT)

        # Scroll frame pour le contenu
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=ModernColors.BG_MEDIUM,
            corner_radius=20,
            scrollbar_button_color=ModernColors.ORANGE_PRIMARY,
            scrollbar_button_hover_color=ModernColors.ORANGE_HOVER
        )
        self.scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        scroll_frame = self.scroll_frame

        # Section Thèmes
        self._create_theme_section(scroll_frame)

        # Séparateur
        ctk.CTkFrame(scroll_frame, height=2, fg_color=ModernColors.BORDER_COLOR).pack(fill=tk.X, pady=20)

        # Section Langue
        self._create_language_section(scroll_frame)

        # Séparateur
        ctk.CTkFrame(scroll_frame, height=2, fg_color=ModernColors.BORDER_COLOR).pack(fill=tk.X, pady=20)

        # Section Police
        self._create_font_section(scroll_frame)

        # Séparateur
        ctk.CTkFrame(scroll_frame, height=2, fg_color=ModernColors.BORDER_COLOR).pack(fill=tk.X, pady=20)

        # Section Interface
        self._create_ui_scale_section(scroll_frame)

        # Séparateur
        ctk.CTkFrame(scroll_frame, height=2, fg_color=ModernColors.BORDER_COLOR).pack(fill=tk.X, pady=20)

        # Section Apparence
        self._create_appearance_section(scroll_frame)

        # Séparateur
        ctk.CTkFrame(scroll_frame, height=2, fg_color=ModernColors.BORDER_COLOR).pack(fill=tk.X, pady=20)

        # Section Avancée
        self._create_advanced_section(scroll_frame)

    def _create_theme_section(self, parent):
        """Créer la section des thèmes avec petits carrés et indicateurs premium"""
        # Header de section
        section_header = ctk.CTkLabel(
            parent,
            text=get_text("themes_title"),
            font=("Segoe UI", 18, "bold"),
            text_color=ModernColors.ORANGE_PRIMARY
        )
        section_header.pack(pady=(10, 15))
        
        # Indicateur de licence
        license_frame = ctk.CTkFrame(parent, fg_color=ModernColors.BG_CARD, corner_radius=10)
        license_frame.pack(pady=(0, 15), padx=50)
        
        license_label = ctk.CTkLabel(
            license_frame,
            text=f"🔑 {self.premium_manager.get_license_name()}",
            font=("Segoe UI", 12, "bold"),
            text_color=ModernColors.GOLD_PREMIUM if self.premium_manager.is_premium() else ModernColors.TEXT_SECONDARY
        )
        license_label.pack(padx=20, pady=10)

        # Grille compacte de thèmes
        themes_grid = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=0)
        themes_grid.pack(pady=10)

        row = 0
        col = 0
        for theme_name in get_theme_names():
            theme = ALL_THEMES[theme_name]
            is_active = theme_name == self.current_theme_name
            is_premium = is_premium_theme(theme_name)
            is_locked = is_premium and not self.premium_manager.is_premium()

            # Container pour le thème
            theme_container = ctk.CTkFrame(
                themes_grid,
                fg_color="transparent",
                corner_radius=0
            )
            theme_container.grid(row=row, column=col, padx=15, pady=10)

            # Carré de couleur (100x100)
            color_btn = ctk.CTkButton(
                theme_container,
                text="🔒" if is_locked else "",
                width=100,
                height=100,
                fg_color=theme.PRIMARY if not is_locked else ModernColors.BG_LIGHT,
                hover_color=theme.PRIMARY_HOVER if not is_locked else ModernColors.BG_HOVER,
                corner_radius=15,
                border_width=3 if is_active else 0,
                border_color="white" if is_active else None,
                command=lambda tn=theme_name, locked=is_locked: self._apply_theme(tn) if not locked else self._show_premium_dialog()
            )
            color_btn.pack()

            # Badge Premium si applicable
            name_text = f"{'✓ ' if is_active else ''}{theme_name}"
            if is_premium:
                name_text += " ⭐"

            # Nom du thème en dessous
            name_label = ctk.CTkLabel(
                theme_container,
                text=name_text,
                font=("Segoe UI", 10, "bold" if is_active else "normal"),
                text_color=ModernColors.GOLD_PREMIUM if is_premium else (ModernColors.TEXT_PRIMARY if is_active else ModernColors.TEXT_SECONDARY)
            )
            name_label.pack(pady=(5, 0))

            col += 1
            if col >= 5:  # 5 colonnes
                col = 0
                row += 1
    
    def _show_premium_dialog(self):
        """Afficher la boîte de dialogue pour activer une licence premium"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Activer une licence Premium")
        dialog.geometry("450x350")
        dialog.configure(fg_color=ModernColors.BG_DARK)
        dialog.transient(self.root_window)
        dialog.grab_set()
        
        # Centrer la fenêtre
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 450) // 2
        y = (dialog.winfo_screenheight() - 350) // 2
        dialog.geometry(f"450x350+{x}+{y}")
        
        # Titre
        ctk.CTkLabel(
            dialog,
            text="🔑 Activer Premium",
            font=("Segoe UI", 20, "bold"),
            text_color=ModernColors.GOLD_PREMIUM
        ).pack(pady=(20, 10))
        
        # Description
        ctk.CTkLabel(
            dialog,
            text="Débloquez tous les thèmes et fonctionnalités !",
            font=("Segoe UI", 12),
            text_color=ModernColors.TEXT_SECONDARY
        ).pack(pady=(0, 20))
        
        # Champ de saisie de la clé
        key_entry = ctk.CTkEntry(
            dialog,
            placeholder_text="NITRITE-PRO-XXXX-XXXX-XXXX",
            width=350,
            height=45,
            font=("Segoe UI", 12),
            fg_color=ModernColors.BG_CARD,
            border_color=ModernColors.ORANGE_PRIMARY
        )
        key_entry.pack(pady=10)
        
        # Message de statut
        status_label = ctk.CTkLabel(
            dialog,
            text="",
            font=("Segoe UI", 11),
            text_color=ModernColors.TEXT_SECONDARY
        )
        status_label.pack(pady=10)
        
        def activate():
            key = key_entry.get().strip()
            if key:
                success, message = self.premium_manager.activate_license(key)
                if success:
                    status_label.configure(text=message, text_color=ModernColors.GREEN_SUCCESS)
                    # Rafraîchir après 1 seconde
                    dialog.after(1500, lambda: [dialog.destroy(), self._refresh_page()])
                else:
                    status_label.configure(text=message, text_color=ModernColors.RED_ERROR)
            else:
                status_label.configure(text="Veuillez entrer une clé de licence", text_color=ModernColors.RED_ERROR)
        
        # Bouton d'activation
        ctk.CTkButton(
            dialog,
            text="Activer la licence",
            width=200,
            height=45,
            fg_color=ModernColors.ORANGE_PRIMARY,
            hover_color=ModernColors.ORANGE_HOVER,
            font=("Segoe UI", 14, "bold"),
            command=activate
        ).pack(pady=15)
        
        # Lien vers achat
        ctk.CTkLabel(
            dialog,
            text="Acheter une licence: contact@ordiplus.fr",
            font=("Segoe UI", 10),
            text_color=ModernColors.TEXT_MUTED
        ).pack(pady=10)
    
    def _refresh_page(self):
        """Rafraîchir la page des paramètres"""
        for widget in self.winfo_children():
            widget.destroy()
        self._create_widgets()
        self._setup_mousewheel()

    def _apply_theme(self, theme_name):
        """Appliquer un thème immédiatement"""
        # Changer le thème
        theme = set_current_theme(theme_name)

        # Mettre à jour ModernColors
        ModernColors.BG_DARK = theme.BG_DARK
        ModernColors.BG_MEDIUM = theme.BG_MEDIUM
        ModernColors.BG_LIGHT = theme.BG_LIGHT
        ModernColors.BG_CARD = theme.BG_CARD
        ModernColors.BG_HOVER = theme.BG_HOVER

        ModernColors.ORANGE_PRIMARY = theme.PRIMARY
        ModernColors.ORANGE_HOVER = theme.PRIMARY_HOVER
        ModernColors.ORANGE_PRESSED = theme.PRIMARY_PRESSED

        ModernColors.TEXT_PRIMARY = theme.TEXT_PRIMARY
        ModernColors.TEXT_SECONDARY = theme.TEXT_SECONDARY
        ModernColors.TEXT_MUTED = theme.TEXT_MUTED

        ModernColors.GREEN_SUCCESS = theme.SUCCESS
        ModernColors.ORANGE_WARNING = theme.WARNING
        ModernColors.RED_DANGER = theme.DANGER
        ModernColors.BLUE_INFO = theme.INFO

        ModernColors.BORDER_COLOR = theme.BORDER_COLOR
        ModernColors.BORDER_HOVER = theme.BORDER_HOVER

        # Sauvegarder la préférence
        self.config['theme'] = theme_name
        self._save_config()

        # Mettre à jour l'interface
        self.current_theme_name = theme_name

        # Rafraîchir la page pour montrer le nouveau thème actif
        # Détruire tous les widgets enfants et recréer
        for widget in self.winfo_children():
            widget.destroy()

        # Recréer l'interface avec le nouveau thème
        self._create_widgets()

    def _create_language_section(self, parent):
        """Créer la section de sélection de langue"""
        section_header = ctk.CTkLabel(
            parent,
            text=get_text("language_title"),
            font=("Segoe UI", 18, "bold"),
            text_color=ModernColors.ORANGE_PRIMARY
        )
        section_header.pack(pady=(10, 15))

        # Container pour les boutons de langue
        lang_container = ctk.CTkFrame(parent, fg_color="transparent")
        lang_container.pack(pady=10)

        languages = ["Français", "English"]
        current_lang = self.config.get('language', 'Français')

        for lang in languages:
            is_active = lang == current_lang
            btn = ctk.CTkButton(
                lang_container,
                text=f"{'✓ ' if is_active else ''}{lang}",
                width=150,
                height=40,
                fg_color=ModernColors.ORANGE_PRIMARY if is_active else ModernColors.BG_CARD,
                hover_color=ModernColors.ORANGE_HOVER,
                text_color=ModernColors.TEXT_PRIMARY,
                corner_radius=10,
                font=("Segoe UI", 12, "bold" if is_active else "normal"),
                command=lambda l=lang: self._change_language(l)
            )
            btn.pack(side=tk.LEFT, padx=10)

    def _change_language(self, language):
        """Changer la langue de l'application"""
        self.config['language'] = language
        self._save_config()

        # Appliquer la langue au système de traduction
        lang_code = "fr" if language == "Français" else "en"
        set_language(lang_code)

        # Rafraîchir l'interface
        for widget in self.winfo_children():
            widget.destroy()
        self._create_widgets()
        self._setup_mousewheel()

    def _create_font_section(self, parent):
        """Créer la section de taille de police"""
        section_header = ctk.CTkLabel(
            parent,
            text=get_text("font_size_title"),
            font=("Segoe UI", 18, "bold"),
            text_color=ModernColors.ORANGE_PRIMARY
        )
        section_header.pack(pady=(10, 15))

        # Container pour le slider
        font_container = ctk.CTkFrame(parent, fg_color=ModernColors.BG_CARD, corner_radius=15)
        font_container.pack(pady=10, padx=50, fill=tk.X)

        # Label de valeur actuelle
        current_size = self.config.get('font_size', 12)
        self.current_font_size = current_size
        value_label = ctk.CTkLabel(
            font_container,
            text=f"Taille actuelle: {current_size}px",
            font=("Segoe UI", 14),
            text_color=ModernColors.TEXT_SECONDARY
        )
        value_label.pack(pady=(15, 5))

        # Slider
        self.font_slider = ctk.CTkSlider(
            font_container,
            from_=8,
            to=24,
            number_of_steps=16,
            width=400,
            progress_color=ModernColors.ORANGE_PRIMARY,
            button_color=ModernColors.ORANGE_PRIMARY,
            button_hover_color=ModernColors.ORANGE_HOVER,
            command=lambda val: self._on_font_size_change(val, value_label)
        )
        self.font_slider.set(current_size)
        self.font_slider.pack(pady=10)

        # Bouton Appliquer
        apply_btn = ctk.CTkButton(
            font_container,
            text=get_text("apply_font"),
            width=250,
            height=35,
            fg_color=ModernColors.GREEN_SUCCESS,
            hover_color="#45a049",
            text_color=ModernColors.TEXT_PRIMARY,
            corner_radius=10,
            font=("Segoe UI", 12, "bold"),
            command=self._apply_font_size
        )
        apply_btn.pack(pady=(5, 15))

        # Labels min/max
        labels_frame = ctk.CTkFrame(font_container, fg_color="transparent")
        labels_frame.pack(pady=(0, 15))

        ctk.CTkLabel(
            labels_frame,
            text="Petit (8px)",
            font=("Segoe UI", 10),
            text_color=ModernColors.TEXT_MUTED
        ).pack(side=tk.LEFT, padx=145)

        ctk.CTkLabel(
            labels_frame,
            text="Grand (24px)",
            font=("Segoe UI", 10),
            text_color=ModernColors.TEXT_MUTED
        ).pack(side=tk.LEFT, padx=145)

    def _on_font_size_change(self, value, label):
        """Mettre à jour l'affichage de la taille (sans appliquer)"""
        size = int(value)
        label.configure(text=f"Taille sélectionnée: {size}px")
        self.current_font_size = size

    def _apply_font_size(self):
        """Appliquer la taille de police sélectionnée"""
        size = self.current_font_size
        self.config['font_size'] = size
        self._save_config()

        # Appliquer le scaling de police immédiatement
        # Note: set_font_scaling() n'existe plus dans CustomTkinter 5.2.2+
        # Le scaling de police se fait via les widgets individuellement
        try:
            import customtkinter as ctk
            # Activer la haute résolution DPI uniquement
            ctk.ScalingTracker.activate_high_dpi_awareness()
            print(f"✓ Police configurée: {size}px (appliquée au prochain redémarrage)")

            # Forcer le rafraîchissement de la fenêtre
            if self.root_window:
                self.root_window.update()
        except Exception as e:
            print(f"Erreur configuration police: {e}")

    def _create_ui_scale_section(self, parent):
        """Créer la section d'échelle de l'interface"""
        section_header = ctk.CTkLabel(
            parent,
            text=get_text("ui_scale_title"),
            font=("Segoe UI", 18, "bold"),
            text_color=ModernColors.ORANGE_PRIMARY
        )
        section_header.pack(pady=(10, 15))

        # Container pour le slider
        scale_container = ctk.CTkFrame(parent, fg_color=ModernColors.BG_CARD, corner_radius=15)
        scale_container.pack(pady=10, padx=50, fill=tk.X)

        # Label de valeur actuelle
        current_scale = self.config.get('ui_scale', 100)
        self.current_ui_scale = current_scale
        value_label = ctk.CTkLabel(
            scale_container,
            text=f"Échelle actuelle: {current_scale}%",
            font=("Segoe UI", 14),
            text_color=ModernColors.TEXT_SECONDARY
        )
        value_label.pack(pady=(15, 5))

        # Slider
        self.ui_scale_slider = ctk.CTkSlider(
            scale_container,
            from_=75,
            to=150,
            number_of_steps=15,
            width=400,
            progress_color=ModernColors.ORANGE_PRIMARY,
            button_color=ModernColors.ORANGE_PRIMARY,
            button_hover_color=ModernColors.ORANGE_HOVER,
            command=lambda val: self._on_ui_scale_change(val, value_label)
        )
        self.ui_scale_slider.set(current_scale)
        self.ui_scale_slider.pack(pady=10)

        # Bouton Appliquer
        apply_btn = ctk.CTkButton(
            scale_container,
            text=get_text("apply_scale"),
            width=200,
            height=35,
            fg_color=ModernColors.GREEN_SUCCESS,
            hover_color="#45a049",
            text_color=ModernColors.TEXT_PRIMARY,
            corner_radius=10,
            font=("Segoe UI", 12, "bold"),
            command=self._apply_ui_scale
        )
        apply_btn.pack(pady=(5, 15))

        # Labels min/max
        labels_frame = ctk.CTkFrame(scale_container, fg_color="transparent")
        labels_frame.pack(pady=(0, 15))

        ctk.CTkLabel(
            labels_frame,
            text="Petit (75%)",
            font=("Segoe UI", 10),
            text_color=ModernColors.TEXT_MUTED
        ).pack(side=tk.LEFT, padx=145)

        ctk.CTkLabel(
            labels_frame,
            text="Grand (150%)",
            font=("Segoe UI", 10),
            text_color=ModernColors.TEXT_MUTED
        ).pack(side=tk.LEFT, padx=145)

    def _on_ui_scale_change(self, value, label):
        """Mettre à jour l'affichage de l'échelle (sans appliquer)"""
        scale = int(value)
        label.configure(text=f"Échelle sélectionnée: {scale}%")
        self.current_ui_scale = scale

    def _apply_ui_scale(self):
        """Appliquer l'échelle d'interface sélectionnée"""
        scale = self.current_ui_scale
        self.config['ui_scale'] = scale
        self._save_config()

        # Appliquer le scaling à CustomTkinter immédiatement
        try:
            import customtkinter as ctk
            ctk.set_widget_scaling(scale / 100.0)
            ctk.ScalingTracker.activate_high_dpi_awareness()
            print(f"✓ Échelle appliquée: {scale}%")

            # Forcer le rafraîchissement
            if self.root_window:
                self.root_window.update()
        except Exception as e:
            print(f"Erreur scaling UI: {e}")

    def _create_appearance_section(self, parent):
        """Créer la section d'apparence"""
        section_header = ctk.CTkLabel(
            parent,
            text=get_text("appearance_title"),
            font=("Segoe UI", 18, "bold"),
            text_color=ModernColors.ORANGE_PRIMARY
        )
        section_header.pack(pady=(10, 15))

        # Container
        appearance_container = ctk.CTkFrame(parent, fg_color=ModernColors.BG_CARD, corner_radius=15)
        appearance_container.pack(pady=10, padx=50, fill=tk.X)

        # Arrondi des bords
        ctk.CTkLabel(
            appearance_container,
            text=get_text("corner_radius_label"),
            font=("Segoe UI", 14, "bold"),
            text_color=ModernColors.TEXT_PRIMARY
        ).pack(pady=(15, 5))

        current_radius = self.config.get('corner_radius', 15)
        self.current_corner_radius = current_radius
        radius_label = ctk.CTkLabel(
            appearance_container,
            text=get_text("corner_current").format(value=current_radius),
            font=("Segoe UI", 12),
            text_color=ModernColors.TEXT_SECONDARY
        )
        radius_label.pack(pady=5)

        # Slider pour l'arrondi
        radius_slider = ctk.CTkSlider(
            appearance_container,
            from_=0,
            to=30,
            number_of_steps=30,
            width=300,
            progress_color=ModernColors.ORANGE_PRIMARY,
            button_color=ModernColors.ORANGE_PRIMARY,
            button_hover_color=ModernColors.ORANGE_HOVER,
            command=lambda val: self._on_corner_radius_change(val, radius_label)
        )
        radius_slider.set(current_radius)
        radius_slider.pack(pady=10)

        # Bouton Appliquer
        ctk.CTkButton(
            appearance_container,
            text=get_text("apply_corner"),
            width=200,
            height=35,
            fg_color=ModernColors.GREEN_SUCCESS,
            hover_color="#45a049",
            corner_radius=10,
            font=("Segoe UI", 12, "bold"),
            command=self._apply_corner_radius
        ).pack(pady=(5, 15))

    def _on_corner_radius_change(self, value, label):
        """Mettre à jour l'affichage de l'arrondi"""
        radius = int(value)
        label.configure(text=get_text("corner_selected").format(value=radius))
        self.current_corner_radius = radius

    def _apply_corner_radius(self):
        """Appliquer l'arrondi sélectionné"""
        radius = self.current_corner_radius
        self.config['corner_radius'] = radius
        self._save_config()

        # Appliquer le corner radius global (sera utilisé pour les nouveaux widgets)
        set_corner_radius(radius)
        print(f"✓ Arrondi appliqué: {radius}px")
        print(f"Note: Redémarrez l'application pour voir tous les changements")

    def _create_advanced_section(self, parent):
        """Créer la section des paramètres avancés"""
        section_header = ctk.CTkLabel(
            parent,
            text=get_text("advanced_title"),
            font=("Segoe UI", 18, "bold"),
            text_color=ModernColors.ORANGE_PRIMARY
        )
        section_header.pack(pady=(10, 15))

        # Container
        advanced_container = ctk.CTkFrame(parent, fg_color=ModernColors.BG_CARD, corner_radius=15)
        advanced_container.pack(pady=10, padx=50, fill=tk.X)

        # Grid de 2 colonnes pour les toggles
        toggles_grid = ctk.CTkFrame(advanced_container, fg_color="transparent")
        toggles_grid.pack(pady=15, padx=20, fill=tk.X)

        # Animations
        self._create_toggle_setting(
            toggles_grid,
            "animations",
            get_text("animations_label"),
            get_text("animations_on"),
            get_text("animations_off"),
            0, 0
        )

        # Smooth Scroll
        self._create_toggle_setting(
            toggles_grid,
            "smooth_scroll",
            get_text("smooth_scroll_label"),
            get_text("smooth_scroll_on"),
            get_text("smooth_scroll_off"),
            0, 1
        )

        # Notifications
        self._create_toggle_setting(
            toggles_grid,
            "notifications",
            get_text("notifications_label"),
            get_text("notifications_on"),
            get_text("notifications_off"),
            1, 0
        )

        # Auto Update
        self._create_toggle_setting(
            toggles_grid,
            "auto_update",
            get_text("auto_update_label"),
            get_text("auto_update_on"),
            get_text("auto_update_off"),
            1, 1
        )

    def _create_toggle_setting(self, parent, config_key, label, text_on, text_off, row, col):
        """Créer un paramètre toggle"""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.grid(row=row, column=col, padx=15, pady=10, sticky="ew")

        # Label
        ctk.CTkLabel(
            container,
            text=label,
            font=("Segoe UI", 12, "bold"),
            text_color=ModernColors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 5))

        # État actuel
        is_enabled = self.config.get(config_key, True)

        # Bouton toggle
        btn = ctk.CTkButton(
            container,
            text=text_on if is_enabled else text_off,
            width=200,
            height=35,
            fg_color=ModernColors.GREEN_SUCCESS if is_enabled else ModernColors.BG_LIGHT,
            hover_color="#45a049" if is_enabled else ModernColors.BG_HOVER,
            corner_radius=10,
            font=("Segoe UI", 11),
            command=lambda: self._toggle_setting(config_key, btn, text_on, text_off)
        )
        btn.pack(anchor="w")

    def _toggle_setting(self, config_key, button, text_on, text_off):
        """Toggle un paramètre"""
        current = self.config.get(config_key, True)
        new_value = not current
        self.config[config_key] = new_value
        self._save_config()

        # Mettre à jour le bouton
        button.configure(
            text=text_on if new_value else text_off,
            fg_color=ModernColors.GREEN_SUCCESS if new_value else ModernColors.BG_LIGHT,
            hover_color="#45a049" if new_value else ModernColors.BG_HOVER
        )
        print(f"{config_key} = {new_value}")

    def _setup_mousewheel(self):
        """Configurer le scroll avec la molette pour le CTkScrollableFrame"""
        def on_enter(event):
            # Bind le scroll quand la souris entre dans la zone
            self.scroll_frame._parent_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        def on_leave(event):
            # Unbind le scroll quand la souris quitte la zone
            self.scroll_frame._parent_canvas.unbind_all("<MouseWheel>")

        # Bind les événements Enter/Leave
        self.scroll_frame.bind("<Enter>", on_enter)
        self.scroll_frame.bind("<Leave>", on_leave)

    def _on_mousewheel(self, event):
        """Gérer l'événement de la molette"""
        # Scroll vers le haut ou le bas
        self.scroll_frame._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
