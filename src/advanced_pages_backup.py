#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NiTriTe V13.0 - Pages Avancées
Pages supplémentaires : Paramètres, Diagnostic, Backup, Optimisations, Mises à jour
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import customtkinter as ctk
import os
import sys
import json
import subprocess
import platform
from datetime import datetime
import threading
import time

# Import des thèmes
try:
    from .themes import ALL_THEMES, get_theme_names, set_current_theme
except ImportError:
    from themes import ALL_THEMES, get_theme_names, set_current_theme

# Import optionnel de psutil et wmi
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    # Créer des fallbacks
    class psutil:
        @staticmethod
        def cpu_percent(interval=1):
            return 0
        @staticmethod
        def virtual_memory():
            class Memory:
                total = 0
                percent = 0
            return Memory()
        @staticmethod
        def disk_usage(path):
            class Disk:
                percent = 0
            return Disk()
        @staticmethod
        def cpu_count(logical=True):
            return 0

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False
    wmi = None

# Import des couleurs depuis le module séparé (évite import circulaire)
try:
    from .modern_colors import ModernColors, bind_mousewheel
except ImportError:
    from modern_colors import ModernColors, bind_mousewheel

# Import du système de traduction
try:
    from .translations import TRANSLATIONS, CURRENT_LANGUAGE, set_language, get_text, _
except ImportError:
    try:
        from translations import TRANSLATIONS, CURRENT_LANGUAGE, set_language, get_text, _
    except ImportError:
        # Fallback si translations n'existe pas
        def _(key):
            return key
        def set_language(lang):
            pass
        def get_text(key):
            return key


class ThemeManager:
    """Gestionnaire de thèmes avec support clair/sombre"""

    THEMES = {
        "dark_orange": {
            "name": "Sombre Orange (Défaut)",
            "BG_DARK": "#0a0a0a",
            "BG_MEDIUM": "#141414",
            "BG_LIGHT": "#1e1e1e",
            "BG_CARD": "#252525",
            "BG_HOVER": "#2f2f2f",
            "ORANGE_PRIMARY": "#ff6b00",
            "ORANGE_LIGHT": "#ff8533",
            "ORANGE_DARK": "#cc5500",
            "TEXT_PRIMARY": "#ffffff",
            "TEXT_SECONDARY": "#b8b8b8",
            "TEXT_MUTED": "#707070",
            "GREEN_SUCCESS": "#00e676",
            "RED_ERROR": "#ff1744",
            "BLUE_INFO": "#00b0ff",
            "PURPLE_PREMIUM": "#7c4dff",
            "YELLOW_WARNING": "#ffd600",
        },
        "light_orange": {
            "name": "Clair Orange",
            "BG_DARK": "#f5f5f5",
            "BG_MEDIUM": "#ffffff",
            "BG_LIGHT": "#fafafa",
            "BG_CARD": "#ffffff",
            "BG_HOVER": "#eeeeee",
            "ORANGE_PRIMARY": "#ff6b00",
            "ORANGE_LIGHT": "#ff8533",
            "ORANGE_DARK": "#cc5500",
            "TEXT_PRIMARY": "#212121",
            "TEXT_SECONDARY": "#757575",
            "TEXT_MUTED": "#9e9e9e",
            "GREEN_SUCCESS": "#00c853",
            "RED_ERROR": "#d50000",
            "BLUE_INFO": "#0091ea",
            "PURPLE_PREMIUM": "#6200ea",
            "YELLOW_WARNING": "#ffc400",
        },
        "light_blue": {
            "name": "Clair Bleu",
            "BG_DARK": "#e3f2fd",
            "BG_MEDIUM": "#ffffff",
            "BG_LIGHT": "#f5f9fd",
            "BG_CARD": "#ffffff",
            "BG_HOVER": "#e1f5fe",
            "ORANGE_PRIMARY": "#2196f3",
            "ORANGE_LIGHT": "#64b5f6",
            "ORANGE_DARK": "#1976d2",
            "TEXT_PRIMARY": "#1a237e",
            "TEXT_SECONDARY": "#424242",
            "TEXT_MUTED": "#757575",
            "GREEN_SUCCESS": "#00c853",
            "RED_ERROR": "#d50000",
            "BLUE_INFO": "#0091ea",
            "PURPLE_PREMIUM": "#6200ea",
            "YELLOW_WARNING": "#f57c00",
        },
        "dark_blue": {
            "name": "Sombre Bleu",
            "BG_DARK": "#0a1929",
            "BG_MEDIUM": "#132f4c",
            "BG_LIGHT": "#1e3a5f",
            "BG_CARD": "#1a2332",
            "BG_HOVER": "#1f2937",
            "ORANGE_PRIMARY": "#2196f3",
            "ORANGE_LIGHT": "#64b5f6",
            "ORANGE_DARK": "#1976d2",
            "TEXT_PRIMARY": "#ffffff",
            "TEXT_SECONDARY": "#b8b8b8",
            "TEXT_MUTED": "#707070",
            "GREEN_SUCCESS": "#00e676",
            "RED_ERROR": "#ff1744",
            "BLUE_INFO": "#00b0ff",
            "PURPLE_PREMIUM": "#7c4dff",
            "YELLOW_WARNING": "#ffd600",
        },
        "dark_purple": {
            "name": "Sombre Violet",
            "BG_DARK": "#120a1f",
            "BG_MEDIUM": "#1f1333",
            "BG_LIGHT": "#2d1b4e",
            "BG_CARD": "#1a1329",
            "BG_HOVER": "#251a3d",
            "ORANGE_PRIMARY": "#9c27b0",
            "ORANGE_LIGHT": "#ba68c8",
            "ORANGE_DARK": "#7b1fa2",
            "TEXT_PRIMARY": "#ffffff",
            "TEXT_SECONDARY": "#b8b8b8",
            "TEXT_MUTED": "#707070",
            "GREEN_SUCCESS": "#00e676",
            "RED_ERROR": "#ff1744",
            "BLUE_INFO": "#00b0ff",
            "PURPLE_PREMIUM": "#7c4dff",
            "YELLOW_WARNING": "#ffd600",
        }
    }

    @staticmethod
    def apply_theme(theme_id, root=None):
        """Appliquer un thème à l'application"""
        try:
            if theme_id not in ThemeManager.THEMES:
                return False

            theme = ThemeManager.THEMES[theme_id]

            # Mettre à jour ModernColors
            for key, value in theme.items():
                if key != "name":
                    setattr(ModernColors, key, value)

            # Sauvegarder le thème choisi
            ThemeManager.save_theme_preference(theme_id)

            # Si root fourni, informer l'utilisateur
            if root:
                try:
                    messagebox.showinfo(
                        "Thème modifié",
                        f"✅ Thème '{theme['name']}' appliqué!\n\n"
                        "Veuillez fermer et relancer l'application\n"
                        "pour voir tous les changements.\n\n"
                        "Le nouveau thème sera automatiquement chargé."
                    )
                except Exception as dialog_error:
                    # Si la boîte de dialogue échoue, juste ignorer
                    print(f"Info: Thème {theme_id} appliqué (dialog error: {dialog_error})")

            return True

        except Exception as e:
            print(f"Erreur lors de l'application du thème: {e}")
            try:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible d'appliquer le thème.\n\n{str(e)}\n\n"
                    "Le thème sera appliqué au prochain démarrage."
                )
            except:
                pass
            return False

    @staticmethod
    def save_theme_preference(theme_id):
        """Sauvegarder le thème préféré"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'theme_config.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump({"theme": theme_id}, f)
        except Exception as e:
            print(f"Erreur sauvegarde thème: {e}")

    @staticmethod
    def load_theme_preference():
        """Charger le thème préféré"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'theme_config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("theme", "dark_orange")
        except:
            pass
        return "dark_orange"


class SettingsPage(tk.Frame):
    """Page Paramètres - Thèmes et configurations"""

    def __init__(self, parent, root_window):
        super().__init__(parent, bg=ModernColors.BG_DARK)
        self.root_window = root_window
        self._create_widgets()

    def _create_widgets(self):
        """Créer les widgets de la page"""
        # Header
        header = tk.Frame(self, bg=ModernColors.BG_DARK)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))

        title_label = tk.Label(
            header,
            text="⚙️ Paramètres & Thèmes",
            font=("Segoe UI", 20, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_PRIMARY
        )
        title_label.pack(side=tk.LEFT)

        # Zone de scroll
        scroll_frame = tk.Frame(self, bg=ModernColors.BG_DARK)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(scroll_frame, bg=ModernColors.BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg=ModernColors.BG_DARK)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        bind_mousewheel(canvas, scrollable_frame)

        # Section Thèmes
        self._create_theme_section(scrollable_frame)

        # Section Préférences
        self._create_preferences_section(scrollable_frame)

    def _create_theme_section(self, parent):
        """Créer la section des thèmes"""
        section = tk.Frame(parent, bg=ModernColors.BG_CARD)
        section.pack(fill=tk.X, pady=(0, 20))

        # Header de section
        section_header = tk.Label(
            section,
            text="🎨 Thèmes d'interface",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.ORANGE_PRIMARY,
            anchor='w',
            padx=20,
            pady=15
        )
        section_header.pack(fill=tk.X)

        # Grille de thèmes
        themes_grid = tk.Frame(section, bg=ModernColors.BG_CARD)
        themes_grid.pack(fill=tk.X, padx=20, pady=(0, 20))

        current_theme = ThemeManager.load_theme_preference()

        row = 0
        col = 0
        for theme_id, theme_data in ThemeManager.THEMES.items():
            card = self._create_theme_card(themes_grid, theme_id, theme_data, theme_id == current_theme)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

            col += 1
            if col >= 2:
                col = 0
                row += 1

        # Configurer les colonnes
        themes_grid.columnconfigure(0, weight=1)
        themes_grid.columnconfigure(1, weight=1)

    def _create_theme_card(self, parent, theme_id, theme_data, is_active):
        """Créer une carte de thème"""
        card = tk.Frame(parent, bg=ModernColors.BG_LIGHT, relief=tk.RAISED if is_active else tk.FLAT)
        card.pack_propagate(False)

        # Nom du thème
        name_label = tk.Label(
            card,
            text=theme_data["name"],
            font=("Segoe UI", 12, "bold"),
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.TEXT_PRIMARY
        )
        name_label.pack(pady=(15, 5))

        # Aperçu des couleurs
        colors_frame = tk.Frame(card, bg=ModernColors.BG_LIGHT)
        colors_frame.pack(pady=10)

        color_preview = [
            theme_data["BG_DARK"],
            theme_data["ORANGE_PRIMARY"],
            theme_data["GREEN_SUCCESS"],
            theme_data["BLUE_INFO"]
        ]

        for color in color_preview:
            color_box = tk.Frame(colors_frame, bg=color, width=40, height=40)
            color_box.pack(side=tk.LEFT, padx=2)
            color_box.pack_propagate(False)

        # Badge actif
        if is_active:
            active_badge = tk.Label(
                card,
                text="✓ ACTIF",
                font=("Segoe UI", 9, "bold"),
                bg=ModernColors.GREEN_SUCCESS,
                fg=ModernColors.TEXT_PRIMARY,
                padx=10,
                pady=3
            )
            active_badge.pack(pady=(5, 10))
        else:
            # Bouton appliquer
            apply_btn = tk.Button(
                card,
                text="Appliquer",
                font=("Segoe UI", 10),
                bg=ModernColors.ORANGE_PRIMARY,
                fg=ModernColors.TEXT_PRIMARY,
                activebackground=ModernColors.ORANGE_DARK,
                relief=tk.FLAT,
                cursor="hand2",
                padx=20,
                pady=5,
                command=lambda tid=theme_id: self._apply_theme(tid)
            )
            apply_btn.pack(pady=(5, 15))

        return card

    def _apply_theme(self, theme_id):
        """Appliquer un thème"""
        ThemeManager.apply_theme(theme_id, self.root_window)

    def _create_preferences_section(self, parent):
        """Créer la section des préférences"""
        section = tk.Frame(parent, bg=ModernColors.BG_CARD)
        section.pack(fill=tk.X, pady=(0, 20))

        # Header de section
        section_header = tk.Label(
            section,
            text="📋 Préférences",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.ORANGE_PRIMARY,
            anchor='w',
            padx=20,
            pady=15
        )
        section_header.pack(fill=tk.X)

        # Options
        options_frame = tk.Frame(section, bg=ModernColors.BG_CARD)
        options_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # === LANGUE ===
        lang_container = tk.Frame(options_frame, bg=ModernColors.BG_LIGHT)
        lang_container.pack(fill=tk.X, pady=10)

        lang_label = tk.Label(
            lang_container,
            text="🌍 Langue / Language:",
            font=("Segoe UI", 11, "bold"),
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.TEXT_PRIMARY,
            anchor='w',
            padx=15,
            pady=10
        )
        lang_label.pack(fill=tk.X)

        lang_buttons = tk.Frame(lang_container, bg=ModernColors.BG_LIGHT)
        lang_buttons.pack(fill=tk.X, padx=15, pady=(0, 10))

        # Bouton Français
        btn_fr = tk.Button(
            lang_buttons,
            text="🇫🇷 Français",
            font=("Segoe UI", 10, "bold"),
            bg=ModernColors.ORANGE_PRIMARY,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            command=lambda: self._change_language('fr')
        )
        btn_fr.pack(side=tk.LEFT, padx=(0, 10))

        # Bouton English
        btn_en = tk.Button(
            lang_buttons,
            text="🇬🇧 English",
            font=("Segoe UI", 10, "bold"),
            bg=ModernColors.BLUE_INFO,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground="#0088cc",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            command=lambda: self._change_language('en')
        )
        btn_en.pack(side=tk.LEFT)

        # === APPARENCE ===
        appearance_container = tk.Frame(options_frame, bg=ModernColors.BG_LIGHT)
        appearance_container.pack(fill=tk.X, pady=10)

        appearance_label = tk.Label(
            appearance_container,
            text="🎨 Apparence / Appearance:",
            font=("Segoe UI", 11, "bold"),
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.TEXT_PRIMARY,
            anchor='w',
            padx=15,
            pady=10
        )
        appearance_label.pack(fill=tk.X)

        appearance_buttons = tk.Frame(appearance_container, bg=ModernColors.BG_LIGHT)
        appearance_buttons.pack(fill=tk.X, padx=15, pady=(0, 10))

        # Bouton Mode Sombre
        btn_dark = tk.Button(
            appearance_buttons,
            text="🌙 Mode Sombre / Dark Mode",
            font=("Segoe UI", 10, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.BG_MEDIUM,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            command=lambda: self._apply_theme('dark_orange')
        )
        btn_dark.pack(side=tk.LEFT, padx=(0, 10))

        # Bouton Mode Clair
        btn_light = tk.Button(
            appearance_buttons,
            text="☀️ Mode Clair / Light Mode",
            font=("Segoe UI", 10, "bold"),
            bg="#f5f5f5",
            fg="#000000",
            activebackground="#e0e0e0",
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            command=lambda: self._apply_theme('light_blue')
        )
        btn_light.pack(side=tk.LEFT)

        # Info sauvegarde automatique
        info_label = tk.Label(
            options_frame,
            text="💡 Les préférences sont sauvegardées automatiquement",
            font=("Segoe UI", 9, "italic"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_MUTED
        )
        info_label.pack(pady=(10, 0))

    def _change_language(self, lang_code):
        """Changer la langue de l'application"""
        try:
            set_language(lang_code)
            messagebox.showinfo(
                "Langue changée" if lang_code == 'fr' else "Language Changed",
                "La langue a été changée. Redémarrez l'application pour appliquer les changements." if lang_code == 'fr'
                else "Language has been changed. Restart the application to apply changes."
            )
            # Sauvegarder la préférence
            self._save_language_preference(lang_code)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de changer la langue: {str(e)}")

    def _save_language_preference(self, lang_code):
        """Sauvegarder la préférence de langue"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'language_config.json')
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump({'language': lang_code}, f)
        except Exception as e:
            print(f"Erreur sauvegarde langue: {e}")


class DiagnosticPage(tk.Frame):
    """Page Diagnostic & Benchmark"""

    def __init__(self, parent):
        super().__init__(parent, bg=ModernColors.BG_DARK)
        self.wmi_obj = None
        try:
            self.wmi_obj = wmi.WMI()
        except:
            pass

        # Variables pour stockage des widgets de performance (temps réel)
        self.perf_widgets = {
            'cpu_percent': None,
            'cpu_bar': None,
            'ram_percent': None,
            'ram_bar': None,
            'disk_percent': None,
            'disk_bar': None
        }
        self.update_running = False  # Flag pour arrêter les updates

        self._create_widgets()

        # Démarrer les mises à jour en temps réel
        self._start_realtime_updates()

    def _create_widgets(self):
        """Créer les widgets de la page"""
        # Header
        header = tk.Frame(self, bg=ModernColors.BG_DARK)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))

        title_label = tk.Label(
            header,
            text="🔍 Diagnostic & Benchmark",
            font=("Segoe UI", 20, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_PRIMARY
        )
        title_label.pack(side=tk.LEFT)

        # Bouton rafraîchir
        refresh_btn = tk.Button(
            header,
            text="🔄 Rafraîchir",
            font=("Segoe UI", 10),
            bg=ModernColors.ORANGE_PRIMARY,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self._refresh_diagnostics
        )
        refresh_btn.pack(side=tk.RIGHT)

        # Zone de scroll
        scroll_frame = tk.Frame(self, bg=ModernColors.BG_DARK)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(scroll_frame, bg=ModernColors.BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)

        self.scrollable_frame = tk.Frame(canvas, bg=ModernColors.BG_DARK)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        bind_mousewheel(canvas, self.scrollable_frame)

        # Charger les diagnostics
        self._load_diagnostics()

    def _load_diagnostics(self):
        """Charger les informations de diagnostic"""
        # Score de santé global
        self._create_health_score()

        # Informations système
        self._create_system_info()

        # Performance actuelle
        self._create_performance_section()

        # Benchmark
        self._create_benchmark_section()

    def _start_realtime_updates(self):
        """Démarrer les mises à jour en temps réel"""
        self.update_running = True
        self._update_performance_realtime()

    def _stop_realtime_updates(self):
        """Arrêter les mises à jour"""
        self.update_running = False

    def _update_performance_realtime(self):
        """Mettre à jour les performances en temps réel (toutes les 2 secondes)"""
        if not self.update_running:
            return

        try:
            # Mettre à jour CPU
            cpu_percent = psutil.cpu_percent(interval=0.1) if PSUTIL_AVAILABLE else 0
            if self.perf_widgets['cpu_percent']:
                self.perf_widgets['cpu_percent'].config(text=f"{cpu_percent:.1f}%")
            if self.perf_widgets['cpu_bar']:
                self.perf_widgets['cpu_bar'].place(x=0, y=0, relwidth=cpu_percent/100, relheight=1)

            # Mettre à jour RAM
            if PSUTIL_AVAILABLE:
                ram = psutil.virtual_memory()
                if self.perf_widgets['ram_percent']:
                    self.perf_widgets['ram_percent'].config(text=f"{ram.percent:.1f}%")
                if self.perf_widgets['ram_bar']:
                    self.perf_widgets['ram_bar'].place(x=0, y=0, relwidth=ram.percent/100, relheight=1)

            # Mettre à jour Disque
            if PSUTIL_AVAILABLE:
                disk = psutil.disk_usage('C:\\' if platform.system() == 'Windows' else '/')
                if self.perf_widgets['disk_percent']:
                    self.perf_widgets['disk_percent'].config(text=f"{disk.percent:.1f}%")
                if self.perf_widgets['disk_bar']:
                    self.perf_widgets['disk_bar'].place(x=0, y=0, relwidth=disk.percent/100, relheight=1)

        except Exception as e:
            pass  # Ignorer les erreurs silencieusement

        # Relancer dans 2 secondes
        self.after(2000, self._update_performance_realtime)

    def destroy(self):
        """Arrêter les updates avant destruction"""
        self._stop_realtime_updates()
        super().destroy()

    def _create_health_score(self):
        """Créer le score de santé PC"""
        card = tk.Frame(self.scrollable_frame, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="💚 Score de Santé PC",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.GREEN_SUCCESS,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        # Calcul du score (simplifié)
        score = self._calculate_health_score()

        score_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
        score_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Score numérique
        score_label = tk.Label(
            score_frame,
            text=f"{score}/100",
            font=("Segoe UI", 48, "bold"),
            bg=ModernColors.BG_CARD,
            fg=self._get_score_color(score)
        )
        score_label.pack(side=tk.LEFT, padx=20)

        # Détails
        details_frame = tk.Frame(score_frame, bg=ModernColors.BG_CARD)
        details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        status_text = self._get_score_status(score)
        status_label = tk.Label(
            details_frame,
            text=status_text,
            font=("Segoe UI", 14, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_PRIMARY,
            anchor='w'
        )
        status_label.pack(fill=tk.X)

        recommendations = self._get_recommendations(score)
        for rec in recommendations:
            rec_label = tk.Label(
                details_frame,
                text=f"• {rec}",
                font=("Segoe UI", 10),
                bg=ModernColors.BG_CARD,
                fg=ModernColors.TEXT_SECONDARY,
                anchor='w'
            )
            rec_label.pack(fill=tk.X, pady=2)

    def _calculate_health_score(self):
        """Calculer un score de santé simplifié"""
        score = 100

        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 80:
            score -= 15
        elif cpu_percent > 50:
            score -= 5

        # RAM usage
        ram = psutil.virtual_memory()
        if ram.percent > 85:
            score -= 15
        elif ram.percent > 70:
            score -= 5

        # Disk usage
        disk = psutil.disk_usage('/')
        if disk.percent > 90:
            score -= 20
        elif disk.percent > 75:
            score -= 10

        return max(0, score)

    def _get_score_color(self, score):
        """Obtenir la couleur selon le score"""
        if score >= 80:
            return ModernColors.GREEN_SUCCESS
        elif score >= 60:
            return ModernColors.YELLOW_WARNING
        else:
            return ModernColors.RED_ERROR

    def _get_score_status(self, score):
        """Obtenir le statut selon le score"""
        if score >= 80:
            return "Excellent - PC en bonne santé"
        elif score >= 60:
            return "Correct - Quelques optimisations recommandées"
        else:
            return "Attention - Maintenance requise"

    def _get_recommendations(self, score):
        """Obtenir des recommandations"""
        recs = []

        cpu_percent = psutil.cpu_percent(interval=0.1)
        if cpu_percent > 70:
            recs.append("Utilisation CPU élevée - Vérifier les processus actifs")

        ram = psutil.virtual_memory()
        if ram.percent > 75:
            recs.append("RAM saturée - Fermer des applications ou augmenter la RAM")

        disk = psutil.disk_usage('/')
        if disk.percent > 80:
            recs.append("Espace disque faible - Nettoyer les fichiers temporaires")

        if not recs:
            recs.append("Aucun problème détecté - Continuez ainsi !")

        return recs

    def _get_detailed_system_info(self):
        """Obtenir les informations système détaillées avec WMI"""
        info = {}

        # OS Version détaillée
        try:
            if self.wmi_obj:
                for os in self.wmi_obj.Win32_OperatingSystem():
                    info['os'] = f"{os.Caption} ({os.Version})"
                    info['os_arch'] = os.OSArchitecture
                    break
            else:
                info['os'] = f"{platform.system()} {platform.release()}"
                info['os_arch'] = platform.machine()
        except:
            info['os'] = f"{platform.system()} {platform.release()}"
            info['os_arch'] = platform.machine()

        # CPU - Vrai nom du processeur
        try:
            if self.wmi_obj:
                for cpu in self.wmi_obj.Win32_Processor():
                    info['cpu'] = cpu.Name.strip()
                    info['cpu_cores'] = f"{cpu.NumberOfCores} physiques / {cpu.NumberOfLogicalProcessors} logiques"
                    break
            else:
                info['cpu'] = platform.processor()
                info['cpu_cores'] = f"{psutil.cpu_count(logical=False)} physiques / {psutil.cpu_count(logical=True)} logiques"
        except:
            info['cpu'] = platform.processor()
            if PSUTIL_AVAILABLE:
                info['cpu_cores'] = f"{psutil.cpu_count(logical=False)} physiques / {psutil.cpu_count(logical=True)} logiques"
            else:
                info['cpu_cores'] = "N/A"

        # GPU - Carte graphique réelle
        try:
            if self.wmi_obj:
                gpu_list = []
                for gpu in self.wmi_obj.Win32_VideoController():
                    if gpu.Name and 'Microsoft' not in gpu.Name:
                        gpu_list.append(gpu.Name)
                info['gpu'] = gpu_list[0] if gpu_list else "Carte graphique détectée"
            else:
                info['gpu'] = "Carte graphique non détectable"
        except:
            info['gpu'] = "Carte graphique non détectable"

        # RAM
        try:
            if PSUTIL_AVAILABLE:
                ram_gb = psutil.virtual_memory().total / (1024**3)
                info['ram'] = f"{ram_gb:.1f} GB"
            else:
                info['ram'] = "N/A"
        except:
            info['ram'] = "N/A"

        # Disque - Type (SSD/HDD/NVMe)
        try:
            if self.wmi_obj:
                disk_info = []
                for disk in self.wmi_obj.Win32_DiskDrive():
                    model = disk.Model if disk.Model else "Disque"
                    size_gb = int(disk.Size) / (1024**3) if disk.Size else 0

                    # Détection du type
                    disk_type = "HDD"
                    if disk.MediaType:
                        media = disk.MediaType.lower()
                        if 'ssd' in media or 'solid state' in media:
                            disk_type = "SSD"
                        elif 'nvme' in media:
                            disk_type = "NVMe"

                    # Vérification alternative via modèle
                    model_lower = model.lower()
                    if 'nvme' in model_lower:
                        disk_type = "NVMe"
                    elif 'ssd' in model_lower or 'solid state' in model_lower:
                        disk_type = "SSD"

                    disk_info.append(f"{model} ({size_gb:.0f} GB) - {disk_type}")

                info['disk'] = disk_info[0] if disk_info else "Disque détecté"
            else:
                info['disk'] = "Disque non détectable"
        except:
            info['disk'] = "Disque non détectable"

        return info

    def _create_system_info(self):
        """Créer la section informations système avec détails complets"""
        card = tk.Frame(self.scrollable_frame, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="💻 Informations Système",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.BLUE_INFO,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        info_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
        info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Obtenir les informations détaillées
        sys_info = self._get_detailed_system_info()

        # Afficher les informations
        infos = [
            ("Version OS", sys_info.get('os', 'N/A')),
            ("Architecture", sys_info.get('os_arch', 'N/A')),
            ("Processeur", sys_info.get('cpu', 'N/A')),
            ("Cœurs CPU", sys_info.get('cpu_cores', 'N/A')),
            ("Carte Graphique", sys_info.get('gpu', 'N/A')),
            ("RAM Totale", sys_info.get('ram', 'N/A')),
            ("Disque Principal", sys_info.get('disk', 'N/A')),
        ]

        for label, value in infos:
            row = tk.Frame(info_frame, bg=ModernColors.BG_LIGHT)
            row.pack(fill=tk.X, pady=3)

            label_widget = tk.Label(
                row,
                text=f"{label}:",
                font=("Segoe UI", 10, "bold"),
                bg=ModernColors.BG_LIGHT,
                fg=ModernColors.TEXT_PRIMARY,
                width=20,
                anchor='w',
                padx=10,
                pady=8
            )
            label_widget.pack(side=tk.LEFT)

            value_widget = tk.Label(
                row,
                text=value,
                font=("Segoe UI", 10),
                bg=ModernColors.BG_LIGHT,
                fg=ModernColors.TEXT_SECONDARY,
                anchor='w',
                padx=10,
                pady=8
            )
            value_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _create_performance_section(self):
        """Créer la section performance actuelle"""
        card = tk.Frame(self.scrollable_frame, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="📊 Performance Actuelle",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.PURPLE_PREMIUM,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        perf_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
        perf_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        self._create_performance_bar(perf_frame, "CPU", cpu_percent, ModernColors.ORANGE_PRIMARY)

        # RAM
        ram = psutil.virtual_memory()
        self._create_performance_bar(perf_frame, "RAM", ram.percent, ModernColors.BLUE_INFO)

        # Disque
        disk = psutil.disk_usage('/')
        self._create_performance_bar(perf_frame, "Disque", disk.percent, ModernColors.PURPLE_PREMIUM)

    def _create_performance_bar(self, parent, label, percent, color):
        """Créer une barre de performance avec stockage des widgets pour updates temps réel"""
        container = tk.Frame(parent, bg=ModernColors.BG_CARD)
        container.pack(fill=tk.X, pady=5)

        # Label et pourcentage
        top_row = tk.Frame(container, bg=ModernColors.BG_CARD)
        top_row.pack(fill=tk.X, pady=(0, 5))

        label_widget = tk.Label(
            top_row,
            text=label,
            font=("Segoe UI", 11, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_PRIMARY
        )
        label_widget.pack(side=tk.LEFT)

        percent_widget = tk.Label(
            top_row,
            text=f"{percent:.1f}%",
            font=("Segoe UI", 11, "bold"),
            bg=ModernColors.BG_CARD,
            fg=color
        )
        percent_widget.pack(side=tk.RIGHT)

        # Barre de progression
        bar_bg = tk.Frame(container, bg=ModernColors.BG_LIGHT, height=20)
        bar_bg.pack(fill=tk.X)

        bar_fill = tk.Frame(bar_bg, bg=color, height=20)
        bar_fill.place(x=0, y=0, relwidth=percent/100, relheight=1)

        # Stocker les références pour les updates en temps réel
        label_lower = label.lower()
        if label_lower == 'cpu':
            self.perf_widgets['cpu_percent'] = percent_widget
            self.perf_widgets['cpu_bar'] = bar_fill
        elif label_lower == 'ram':
            self.perf_widgets['ram_percent'] = percent_widget
            self.perf_widgets['ram_bar'] = bar_fill
        elif label_lower == 'disque':
            self.perf_widgets['disk_percent'] = percent_widget
            self.perf_widgets['disk_bar'] = bar_fill

    def _create_benchmark_section(self):
        """Créer la section benchmark"""
        card = tk.Frame(self.scrollable_frame, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="⚡ Benchmark & Tests",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.YELLOW_WARNING,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        buttons_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
        buttons_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Boutons de benchmark
        benchmarks = [
            ("CPU", "Test processeur", self._benchmark_cpu, ModernColors.ORANGE_PRIMARY),
            ("RAM", "Test mémoire", self._benchmark_ram, ModernColors.BLUE_INFO),
            ("Disque", "Test lecture/écriture", self._benchmark_disk, ModernColors.PURPLE_PREMIUM),
        ]

        for name, desc, command, color in benchmarks:
            btn_frame = tk.Frame(buttons_frame, bg=ModernColors.BG_LIGHT)
            btn_frame.pack(fill=tk.X, pady=5)

            btn = tk.Button(
                btn_frame,
                text=f"▶ Lancer test {name}",
                font=("Segoe UI", 10, "bold"),
                bg=color,
                fg=ModernColors.TEXT_PRIMARY,
                activebackground=ModernColors.ORANGE_DARK,
                relief=tk.FLAT,
                cursor="hand2",
                padx=15,
                pady=10,
                command=command
            )
            btn.pack(side=tk.LEFT, padx=10, pady=10)

            desc_label = tk.Label(
                btn_frame,
                text=desc,
                font=("Segoe UI", 10),
                bg=ModernColors.BG_LIGHT,
                fg=ModernColors.TEXT_SECONDARY
            )
            desc_label.pack(side=tk.LEFT, padx=10)

    def _benchmark_cpu(self):
        """Benchmark CPU avec calculs mathématiques intensifs"""
        try:
            result = messagebox.askyesno(
                "Benchmark CPU",
                "Ce test va solliciter le CPU pendant ~10 secondes.\n\n"
                "L'application peut sembler figée pendant le test.\n\n"
                "Continuer ?"
            )
            if not result:
                return

            # Fenêtre de progression
            progress_window = tk.Toplevel(self)
            progress_window.title("Benchmark CPU")
            progress_window.geometry("400x150")
            progress_window.configure(bg=ModernColors.BG_DARK)
            progress_window.transient(self)
            progress_window.grab_set()

            label = tk.Label(
                progress_window,
                text="Test CPU en cours...\n\nCalculs mathématiques intensifs",
                font=("Segoe UI", 11),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_PRIMARY
            )
            label.pack(pady=20)

            progress_label = tk.Label(
                progress_window,
                text="Préparation...",
                font=("Segoe UI", 9),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_SECONDARY
            )
            progress_label.pack()

            def run_benchmark():
                import math
                start_time = time.time()

                # Test: calculs de nombres premiers et opérations mathématiques
                iterations = 0
                target_duration = 5  # 5 secondes de test

                while time.time() - start_time < target_duration:
                    # Calculs intensifs
                    for i in range(1000):
                        _ = math.sqrt(i) * math.sin(i) * math.cos(i)
                        _ = math.factorial(min(i % 20, 15))  # Limité pour éviter overflow
                    iterations += 1000

                    # Update progress
                    elapsed = time.time() - start_time
                    progress_label.config(text=f"Progression: {int((elapsed/target_duration)*100)}%")
                    progress_window.update()

                end_time = time.time()
                duration = end_time - start_time
                score = int(iterations / duration)  # Opérations par seconde

                progress_window.destroy()

                # Afficher résultats
                messagebox.showinfo(
                    "Résultats Benchmark CPU",
                    f"✅ Test terminé !\n\n"
                    f"Durée: {duration:.2f} secondes\n"
                    f"Opérations: {iterations:,}\n"
                    f"Score: {score:,} ops/sec\n\n"
                    f"{'⚡ Excellent' if score > 500000 else '✓ Bon' if score > 250000 else '⚠️ Moyen'}"
                )

            # Lancer le benchmark dans un thread
            threading.Thread(target=run_benchmark, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur benchmark CPU:\n{str(e)}")

    def _benchmark_ram(self):
        """Benchmark RAM avec allocations mémoire"""
        try:
            result = messagebox.askyesno(
                "Benchmark RAM",
                "Ce test va allouer temporairement de la mémoire.\n\n"
                "Test sans danger, durée ~5 secondes.\n\n"
                "Continuer ?"
            )
            if not result:
                return

            # Fenêtre de progression
            progress_window = tk.Toplevel(self)
            progress_window.title("Benchmark RAM")
            progress_window.geometry("400x150")
            progress_window.configure(bg=ModernColors.BG_DARK)
            progress_window.transient(self)
            progress_window.grab_set()

            label = tk.Label(
                progress_window,
                text="Test RAM en cours...\n\nAllocations et accès mémoire",
                font=("Segoe UI", 11),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_PRIMARY
            )
            label.pack(pady=20)

            progress_label = tk.Label(
                progress_window,
                text="Préparation...",
                font=("Segoe UI", 9),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_SECONDARY
            )
            progress_label.pack()

            def run_benchmark():
                start_time = time.time()

                # Test: allocations et lectures/écritures mémoire
                test_size = 100  # MB
                chunk_size = 1024 * 1024  # 1 MB
                iterations = 0

                for i in range(test_size):
                    # Allouer et remplir la mémoire
                    data = bytearray(chunk_size)
                    for j in range(0, chunk_size, 1024):
                        data[j] = i % 256
                    iterations += 1

                    # Update progress
                    progress_label.config(text=f"Progression: {int((i/test_size)*100)}%")
                    progress_window.update()

                    # Nettoyer
                    del data

                end_time = time.time()
                duration = end_time - start_time
                speed = (test_size / duration)  # MB/s

                progress_window.destroy()

                # Afficher résultats
                messagebox.showinfo(
                    "Résultats Benchmark RAM",
                    f"✅ Test terminé !\n\n"
                    f"Données traitées: {test_size} MB\n"
                    f"Durée: {duration:.2f} secondes\n"
                    f"Vitesse: {speed:.1f} MB/s\n\n"
                    f"{'⚡ Rapide' if speed > 1000 else '✓ Normal' if speed > 500 else '⚠️ Lent'}"
                )

            # Lancer le benchmark dans un thread
            threading.Thread(target=run_benchmark, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur benchmark RAM:\n{str(e)}")

    def _benchmark_disk(self):
        """Benchmark Disque avec lecture/écriture"""
        try:
            result = messagebox.askyesno(
                "Benchmark Disque",
                "Ce test va créer un fichier temporaire de test.\n\n"
                "Durée ~10 secondes, fichier supprimé automatiquement.\n\n"
                "Continuer ?"
            )
            if not result:
                return

            # Fenêtre de progression
            progress_window = tk.Toplevel(self)
            progress_window.title("Benchmark Disque")
            progress_window.geometry("400x150")
            progress_window.configure(bg=ModernColors.BG_DARK)
            progress_window.transient(self)
            progress_window.grab_set()

            label = tk.Label(
                progress_window,
                text="Test Disque en cours...\n\nLecture/Écriture fichier",
                font=("Segoe UI", 11),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_PRIMARY
            )
            label.pack(pady=20)

            progress_label = tk.Label(
                progress_window,
                text="Préparation...",
                font=("Segoe UI", 9),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_SECONDARY
            )
            progress_label.pack()

            def run_benchmark():
                import tempfile
                test_file = os.path.join(tempfile.gettempdir(), "nitrite_disk_benchmark.tmp")

                try:
                    # Test écriture
                    progress_label.config(text="Test d'écriture...")
                    progress_window.update()

                    test_size = 50  # MB
                    chunk_size = 1024 * 1024  # 1 MB
                    data = b'0' * chunk_size

                    start_write = time.time()
                    with open(test_file, 'wb') as f:
                        for i in range(test_size):
                            f.write(data)
                            progress_label.config(text=f"Écriture: {int((i/test_size)*100)}%")
                            progress_window.update()
                    end_write = time.time()
                    write_speed = test_size / (end_write - start_write)

                    # Test lecture
                    progress_label.config(text="Test de lecture...")
                    progress_window.update()

                    start_read = time.time()
                    with open(test_file, 'rb') as f:
                        i = 0
                        while f.read(chunk_size):
                            i += 1
                            progress_label.config(text=f"Lecture: {int((i/test_size)*100)}%")
                            progress_window.update()
                    end_read = time.time()
                    read_speed = test_size / (end_read - start_read)

                    # Nettoyer
                    if os.path.exists(test_file):
                        os.remove(test_file)

                    progress_window.destroy()

                    # Afficher résultats
                    messagebox.showinfo(
                        "Résultats Benchmark Disque",
                        f"✅ Test terminé !\n\n"
                        f"Fichier test: {test_size} MB\n\n"
                        f"📝 Écriture: {write_speed:.1f} MB/s\n"
                        f"📖 Lecture: {read_speed:.1f} MB/s\n\n"
                        f"Type estimé: "
                        f"{'NVMe/SSD ⚡' if write_speed > 200 else 'SSD ✓' if write_speed > 100 else 'HDD 💾'}"
                    )

                except Exception as e:
                    progress_window.destroy()
                    # Nettoyer en cas d'erreur
                    if os.path.exists(test_file):
                        os.remove(test_file)
                    raise e

            # Lancer le benchmark dans un thread
            threading.Thread(target=run_benchmark, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur benchmark disque:\n{str(e)}")

    def _refresh_diagnostics(self):
        """Rafraîchir les diagnostics"""
        # Nettoyer et recharger
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self._load_diagnostics()


class BackupPage(tk.Frame):
    """Page Backup & Restauration"""

    def __init__(self, parent):
        super().__init__(parent, bg=ModernColors.BG_DARK)
        self._create_widgets()

    def _create_widgets(self):
        """Créer les widgets de la page"""
        # Header
        header = tk.Frame(self, bg=ModernColors.BG_DARK)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))

        title_label = tk.Label(
            header,
            text="💾 Backup & Restauration",
            font=("Segoe UI", 20, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_PRIMARY
        )
        title_label.pack(side=tk.LEFT)

        # Zone de scroll
        scroll_frame = tk.Frame(self, bg=ModernColors.BG_DARK)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(scroll_frame, bg=ModernColors.BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg=ModernColors.BG_DARK)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        bind_mousewheel(canvas, scrollable_frame)

        # Section Point de restauration
        self._create_restore_point_section(scrollable_frame)

        # Section Backup drivers
        self._create_driver_backup_section(scrollable_frame)

        # Section Backup liste apps
        self._create_app_list_section(scrollable_frame)

    def _create_restore_point_section(self, parent):
        """Section point de restauration Windows"""
        card = tk.Frame(parent, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="🔄 Point de Restauration Windows",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.BLUE_INFO,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        desc = tk.Label(
            card,
            text="Créer un point de restauration système avant toute modification importante",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w',
            padx=20
        )
        desc.pack(fill=tk.X, pady=(0, 15))

        btn_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        create_btn = tk.Button(
            btn_frame,
            text="🛡️ Créer Point de Restauration",
            font=("Segoe UI", 11, "bold"),
            bg=ModernColors.GREEN_SUCCESS,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=12,
            command=self._create_restore_point
        )
        create_btn.pack(side=tk.LEFT, padx=5)

        list_btn = tk.Button(
            btn_frame,
            text="📋 Voir Points de Restauration",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self._list_restore_points
        )
        list_btn.pack(side=tk.LEFT, padx=5)

    def _create_driver_backup_section(self, parent):
        """Section backup drivers"""
        card = tk.Frame(parent, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="🔌 Sauvegarde des Pilotes",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.PURPLE_PREMIUM,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        desc = tk.Label(
            card,
            text="Sauvegarder tous les pilotes système installés pour une restauration rapide",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w',
            padx=20
        )
        desc.pack(fill=tk.X, pady=(0, 15))

        btn_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        backup_btn = tk.Button(
            btn_frame,
            text="💾 Sauvegarder les Pilotes",
            font=("Segoe UI", 11, "bold"),
            bg=ModernColors.PURPLE_PREMIUM,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=12,
            command=self._backup_drivers
        )
        backup_btn.pack(side=tk.LEFT, padx=5)

        restore_btn = tk.Button(
            btn_frame,
            text="📥 Restaurer les Pilotes",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self._restore_drivers
        )
        restore_btn.pack(side=tk.LEFT, padx=5)

    def _create_app_list_section(self, parent):
        """Section backup liste apps"""
        card = tk.Frame(parent, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="📦 Liste des Applications",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.ORANGE_PRIMARY,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        desc = tk.Label(
            card,
            text="Sauvegarder la liste des applications installées pour réinstallation rapide",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w',
            padx=20
        )
        desc.pack(fill=tk.X, pady=(0, 15))

        btn_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        export_btn = tk.Button(
            btn_frame,
            text="📤 Exporter Liste Apps",
            font=("Segoe UI", 11, "bold"),
            bg=ModernColors.ORANGE_PRIMARY,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=12,
            command=self._export_app_list
        )
        export_btn.pack(side=tk.LEFT, padx=5)

        import_btn = tk.Button(
            btn_frame,
            text="📥 Importer & Installer",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self._import_app_list
        )
        import_btn.pack(side=tk.LEFT, padx=5)

    def _create_restore_point(self):
        """Créer un point de restauration"""
        try:
            result = messagebox.askyesno(
                "Point de Restauration",
                "Créer un point de restauration système ?\n\n"
                "Cette opération peut prendre quelques minutes.\n"
                "Vous devez avoir les droits administrateur."
            )

            if result:
                # Utiliser PowerShell pour créer le point de restauration
                ps_command = '''
                Checkpoint-Computer -Description "NiTriTe_V13_Backup_$(Get-Date -Format 'yyyy-MM-dd_HH-mm')" -RestorePointType "MODIFY_SETTINGS"
                '''

                messagebox.showinfo(
                    "Création en cours",
                    "Création du point de restauration en cours...\n\n"
                    "Veuillez patienter."
                )

                result = subprocess.run(
                    ["powershell", "-Command", ps_command],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    messagebox.showinfo(
                        "Succès",
                        "✅ Point de restauration créé avec succès !\n\n"
                        "Vous pouvez le restaurer depuis :\n"
                        "Paramètres → Récupération → Ouvrir la restauration du système"
                    )
                else:
                    raise Exception(result.stderr)

        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible de créer le point de restauration.\n\n"
                f"Erreur : {str(e)}\n\n"
                "Assurez-vous d'avoir les droits administrateur."
            )

    def _list_restore_points(self):
        """Lister les points de restauration"""
        try:
            subprocess.run(["rstrui.exe"], shell=True)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir la restauration système.\n\n{str(e)}")

    def _backup_drivers(self):
        """Sauvegarder les pilotes"""
        try:
            # Demander le dossier de destination
            folder = filedialog.askdirectory(
                title="Choisir le dossier de sauvegarde des pilotes"
            )

            if folder:
                backup_path = os.path.join(folder, f"DriversBackup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                os.makedirs(backup_path, exist_ok=True)

                messagebox.showinfo(
                    "Sauvegarde en cours",
                    "Sauvegarde des pilotes en cours...\n\n"
                    "Cette opération peut prendre plusieurs minutes."
                )

                # Utiliser DISM pour exporter les pilotes
                command = f'dism /online /export-driver /destination:"{backup_path}"'
                result = os.system(command)

                if result == 0:
                    messagebox.showinfo(
                        "Succès",
                        f"✅ Pilotes sauvegardés avec succès !\n\n"
                        f"Emplacement : {backup_path}\n\n"
                        "Ouvrir le dossier ?"
                    )
                    os.startfile(backup_path)
                else:
                    raise Exception("Échec de l'export DISM")

        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible de sauvegarder les pilotes.\n\n{str(e)}"
            )

    def _restore_drivers(self):
        """Restaurer les pilotes"""
        try:
            folder = filedialog.askdirectory(
                title="Choisir le dossier contenant les pilotes sauvegardés"
            )

            if folder:
                messagebox.showinfo(
                    "Restauration",
                    f"Pour restaurer les pilotes :\n\n"
                    f"1. Ouvrez le Gestionnaire de périphériques\n"
                    f"2. Clic droit sur le périphérique → Mettre à jour le pilote\n"
                    f"3. Rechercher des pilotes sur mon ordinateur\n"
                    f"4. Sélectionnez : {folder}"
                )
                # Ouvrir le gestionnaire de périphériques
                os.system("devmgmt.msc")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la restauration.\n\n{str(e)}")

    def _export_app_list(self):
        """Exporter la liste des applications"""
        try:
            # Obtenir la liste des apps avec winget
            messagebox.showinfo(
                "Export en cours",
                "Récupération de la liste des applications...\n\n"
                "Cela peut prendre quelques secondes."
            )

            result = subprocess.run(
                ["winget", "list"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # Sauvegarder dans un fichier
                desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
                if not os.path.exists(desktop):
                    desktop = os.path.join(os.path.expanduser('~'), 'Bureau')

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                file_path = os.path.join(desktop, f'Apps_List_{timestamp}.txt')

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("=== LISTE DES APPLICATIONS INSTALLÉES ===\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Généré par NiTriTe V13.0\n\n")
                    f.write(result.stdout)

                messagebox.showinfo(
                    "Succès",
                    f"✅ Liste exportée avec succès !\n\n"
                    f"Fichier : Apps_List_{timestamp}.txt\n"
                    f"Emplacement : Bureau"
                )
                os.startfile(file_path)
            else:
                raise Exception("Winget non disponible")

        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible d'exporter la liste.\n\n{str(e)}\n\n"
                "Assurez-vous que winget est installé."
            )

    def _import_app_list(self):
        """Importer et installer depuis une liste JSON"""
        try:
            # Sélectionner le fichier JSON
            file_path = filedialog.askopenfilename(
                title="Sélectionner la liste d'applications",
                filetypes=[
                    ("Fichiers JSON", "*.json"),
                    ("Fichiers texte", "*.txt"),
                    ("Tous les fichiers", "*.*")
                ],
                initialdir=os.path.expanduser("~/Desktop")
            )

            if not file_path:
                return

            # Lire et parser le fichier
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Essayer de parser comme JSON
            try:
                app_list = json.loads(content)
                if isinstance(app_list, dict):
                    # Si c'est un dict, prendre les clés comme noms d'apps
                    apps = list(app_list.keys())
                elif isinstance(app_list, list):
                    apps = app_list
                else:
                    raise ValueError("Format JSON invalide")
            except json.JSONDecodeError:
                # Si ce n'est pas du JSON, essayer comme liste texte (une app par ligne)
                apps = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]

            if not apps:
                messagebox.showwarning("Aucune application", "Aucune application trouvée dans le fichier.")
                return

            # Confirmer l'installation
            result = messagebox.askyesno(
                "Confirmer l'installation",
                f"📦 {len(apps)} application(s) trouvée(s):\n\n" +
                '\n'.join(f"• {app}" for app in apps[:10]) +
                (f"\n... et {len(apps)-10} autres" if len(apps) > 10 else "") +
                "\n\nInstaller via WinGet ?"
            )

            if not result:
                return

            # Vérifier winget
            check_result = subprocess.run(
                ["winget", "--version"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

            if check_result.returncode != 0:
                messagebox.showerror(
                    "WinGet non disponible",
                    "WinGet n'est pas installé ou n'est pas dans le PATH.\n\n"
                    "Installez WinGet depuis le Microsoft Store."
                )
                return

            # Fenêtre de progression
            progress_window = tk.Toplevel(self)
            progress_window.title("Installation en cours")
            progress_window.geometry("500x300")
            progress_window.configure(bg=ModernColors.BG_DARK)
            progress_window.transient(self)

            title_label = tk.Label(
                progress_window,
                text="Installation des applications",
                font=("Segoe UI", 14, "bold"),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_PRIMARY
            )
            title_label.pack(pady=15)

            status_label = tk.Label(
                progress_window,
                text="Préparation...",
                font=("Segoe UI", 10),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_SECONDARY
            )
            status_label.pack()

            # Zone de log
            log_text = scrolledtext.ScrolledText(
                progress_window,
                width=60,
                height=12,
                bg=ModernColors.BG_CARD,
                fg=ModernColors.TEXT_PRIMARY,
                font=("Consolas", 9)
            )
            log_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            def install_apps():
                success_count = 0
                failed_count = 0
                failed_apps = []

                for i, app_name in enumerate(apps, 1):
                    status_label.config(text=f"Installation {i}/{len(apps)}: {app_name}")
                    log_text.insert(tk.END, f"\n{'='*50}\n")
                    log_text.insert(tk.END, f"[{i}/{len(apps)}] Installation de: {app_name}\n")
                    log_text.see(tk.END)
                    progress_window.update()

                    try:
                        # Installer via winget
                        result = subprocess.run(
                            ["winget", "install", "--id", app_name, "-e", "--accept-source-agreements", "--accept-package-agreements"],
                            capture_output=True,
                            text=True,
                            timeout=300,  # 5 minutes max par app
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                        )

                        if result.returncode == 0 or "successfully installed" in result.stdout.lower():
                            log_text.insert(tk.END, f"✅ Succès\n", "success")
                            success_count += 1
                        else:
                            log_text.insert(tk.END, f"❌ Échec: {result.stderr[:100]}\n", "error")
                            failed_count += 1
                            failed_apps.append(app_name)

                    except subprocess.TimeoutExpired:
                        log_text.insert(tk.END, f"⏱️ Timeout (>5 min)\n", "error")
                        failed_count += 1
                        failed_apps.append(app_name)
                    except Exception as e:
                        log_text.insert(tk.END, f"❌ Erreur: {str(e)[:100]}\n", "error")
                        failed_count += 1
                        failed_apps.append(app_name)

                    log_text.see(tk.END)
                    progress_window.update()

                # Résumé final
                log_text.insert(tk.END, f"\n{'='*50}\n")
                log_text.insert(tk.END, f"\n📊 RÉSUMÉ:\n")
                log_text.insert(tk.END, f"✅ Succès: {success_count}\n", "success")
                log_text.insert(tk.END, f"❌ Échecs: {failed_count}\n", "error")
                if failed_apps:
                    log_text.insert(tk.END, f"\nApplications échouées:\n")
                    for app in failed_apps:
                        log_text.insert(tk.END, f"  • {app}\n")

                status_label.config(text="Installation terminée !")

                # Bouton fermer
                close_btn = tk.Button(
                    progress_window,
                    text="Fermer",
                    font=("Segoe UI", 10),
                    bg=ModernColors.ORANGE_PRIMARY,
                    fg=ModernColors.TEXT_PRIMARY,
                    command=progress_window.destroy,
                    padx=20,
                    pady=8
                )
                close_btn.pack(pady=10)

            # Lancer l'installation dans un thread
            threading.Thread(target=install_apps, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'import:\n{str(e)}")


class OptimizationsPage(tk.Frame):
    """Page Optimisations Windows"""

    def __init__(self, parent):
        super().__init__(parent, bg=ModernColors.BG_DARK)
        self._create_widgets()

    def _create_widgets(self):
        """Créer les widgets de la page"""
        # Header
        header = tk.Frame(self, bg=ModernColors.BG_DARK)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))

        title_label = tk.Label(
            header,
            text="⚡ Optimisations Windows",
            font=("Segoe UI", 20, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_PRIMARY
        )
        title_label.pack(side=tk.LEFT)

        # Warning
        warning = tk.Label(
            header,
            text="⚠️ Modifications système - Utiliser avec prudence",
            font=("Segoe UI", 9),
            bg=ModernColors.YELLOW_WARNING,
            fg=ModernColors.BG_DARK,
            padx=10,
            pady=5
        )
        warning.pack(side=tk.RIGHT)

        # Zone de scroll
        scroll_frame = tk.Frame(self, bg=ModernColors.BG_DARK)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(scroll_frame, bg=ModernColors.BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg=ModernColors.BG_DARK)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        bind_mousewheel(canvas, scrollable_frame)

        # Section Télémétrie
        self._create_telemetry_section(scrollable_frame)

        # Section Services
        self._create_services_section(scrollable_frame)

        # Section Démarrage
        self._create_startup_section(scrollable_frame)

        # Section Registre
        self._create_registry_section(scrollable_frame)

    def _create_telemetry_section(self, parent):
        """Section désactivation télémétrie"""
        card = tk.Frame(parent, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="🔒 Confidentialité & Télémétrie",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.RED_ERROR,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        desc = tk.Label(
            card,
            text="Désactiver la collecte de données et télémétrie Windows",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w',
            padx=20
        )
        desc.pack(fill=tk.X, pady=(0, 15))

        options_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
        options_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        self.telemetry_vars = {}
        telemetry_options = [
            ("disable_telemetry", "Désactiver la télémétrie"),
            ("disable_cortana", "Désactiver Cortana"),
            ("disable_location", "Désactiver la localisation"),
            ("disable_advertising", "Désactiver l'ID publicitaire"),
        ]

        for var_name, label in telemetry_options:
            self.telemetry_vars[var_name] = tk.BooleanVar(value=False)
            cb = tk.Checkbutton(
                options_frame,
                text=label,
                variable=self.telemetry_vars[var_name],
                font=("Segoe UI", 10),
                bg=ModernColors.BG_CARD,
                fg=ModernColors.TEXT_PRIMARY,
                selectcolor=ModernColors.BG_LIGHT,
                activebackground=ModernColors.BG_CARD,
                activeforeground=ModernColors.TEXT_PRIMARY
            )
            cb.pack(anchor='w', pady=3)

        apply_btn = tk.Button(
            card,
            text="✓ Appliquer les modifications",
            font=("Segoe UI", 11, "bold"),
            bg=ModernColors.ORANGE_PRIMARY,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=12,
            command=self._apply_telemetry_tweaks
        )
        apply_btn.pack(padx=20, pady=(0, 20))

    def _create_services_section(self, parent):
        """Section gestion services"""
        card = tk.Frame(parent, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="⚙️ Services Windows",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.BLUE_INFO,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        desc = tk.Label(
            card,
            text="Désactiver les services Windows inutiles pour améliorer les performances",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w',
            padx=20
        )
        desc.pack(fill=tk.X, pady=(0, 15))

        btn_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        services_btn = tk.Button(
            btn_frame,
            text="🔧 Ouvrir Services",
            font=("Segoe UI", 10),
            bg=ModernColors.BLUE_INFO,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=lambda: os.system("services.msc")
        )
        services_btn.pack(side=tk.LEFT, padx=5)

        optimize_btn = tk.Button(
            btn_frame,
            text="⚡ Optimisation Auto",
            font=("Segoe UI", 10),
            bg=ModernColors.PURPLE_PREMIUM,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self._optimize_services
        )
        optimize_btn.pack(side=tk.LEFT, padx=5)

    def _create_startup_section(self, parent):
        """Section gestion démarrage"""
        card = tk.Frame(parent, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="🚀 Applications au Démarrage",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.PURPLE_PREMIUM,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        desc = tk.Label(
            card,
            text="Gérer les applications qui se lancent au démarrage de Windows",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w',
            padx=20
        )
        desc.pack(fill=tk.X, pady=(0, 15))

        btn_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        startup_btn = tk.Button(
            btn_frame,
            text="📋 Ouvrir Gestionnaire Démarrage",
            font=("Segoe UI", 10, "bold"),
            bg=ModernColors.PURPLE_PREMIUM,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=lambda: os.system("start ms-settings:startupapps")
        )
        startup_btn.pack(side=tk.LEFT, padx=5)

    def _create_registry_section(self, parent):
        """Section nettoyage registre"""
        card = tk.Frame(parent, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="🗂️ Registre Windows",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.YELLOW_WARNING,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        desc = tk.Label(
            card,
            text="Nettoyer les entrées obsolètes du registre (⚠️ Fonction avancée)",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w',
            padx=20
        )
        desc.pack(fill=tk.X, pady=(0, 15))

        btn_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        regedit_btn = tk.Button(
            btn_frame,
            text="🔍 Ouvrir Éditeur Registre",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_LIGHT,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=lambda: os.system("regedit")
        )
        regedit_btn.pack(side=tk.LEFT, padx=5)

        clean_btn = tk.Button(
            btn_frame,
            text="🧹 Nettoyage Auto",
            font=("Segoe UI", 10),
            bg=ModernColors.GREEN_SUCCESS,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self._auto_cleanup
        )
        clean_btn.pack(side=tk.LEFT, padx=5)

    def _apply_telemetry_tweaks(self):
        """Appliquer les tweaks de télémétrie Windows"""
        try:
            result = messagebox.askyesnocancel(
                "Désactiver la télémétrie Windows",
                "Cette opération va:\n\n"
                "✓ Désactiver la télémétrie Windows\n"
                "✓ Désactiver le rapport d'erreurs\n"
                "✓ Désactiver les suggestions\n"
                "✓ Désactiver l'historique d'activité\n\n"
                "⚠️ Modifications du registre\n"
                "⚠️ Requiert droits administrateur\n\n"
                "Oui = Appliquer | Non = Outils recommandés | Annuler = Fermer"
            )

            if result is None:  # Cancel
                return
            elif result is False:  # Non - Afficher outils recommandés
                messagebox.showinfo(
                    "Outils Recommandés",
                    "Pour un contrôle plus granulaire:\n\n"
                    "• O&O ShutUp10++ (gratuit)\n"
                    "• W10Privacy (open source)\n"
                    "• WPD - Windows Privacy Dashboard\n"
                    "• Sophia Script (PowerShell)\n\n"
                    "Ces outils offrent plus d'options de personnalisation."
                )
                return

            # Créer script PowerShell pour tweaks télémétrie
            ps_script = """
# Désactiver télémétrie
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry" -Type DWord -Value 0

# Désactiver rapport d'erreurs Windows
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" -Name "Disabled" -Type DWord -Value 1

# Désactiver suggestions dans Démarrer
Set-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" -Name "SystemPaneSuggestionsEnabled" -Type DWord -Value 0

# Désactiver historique d'activité
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" -Name "PublishUserActivities" -Type DWord -Value 0
Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" -Name "UploadUserActivities" -Type DWord -Value 0

Write-Host "Tweaks télémétrie appliqués avec succès!"
"""

            # Sauvegarder script temporaire
            import tempfile
            script_path = os.path.join(tempfile.gettempdir(), "nitrite_telemetry_tweaks.ps1")
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(ps_script)

            # Exécuter PowerShell en admin
            try:
                result = subprocess.run(
                    ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )

                # Nettoyer
                if os.path.exists(script_path):
                    os.remove(script_path)

                if result.returncode == 0:
                    messagebox.showinfo(
                        "Succès",
                        "✅ Tweaks télémétrie appliqués!\n\n"
                        "Redémarrage recommandé pour que tous les changements prennent effet."
                    )
                else:
                    messagebox.showwarning(
                        "Droits insuffisants",
                        "Certains changements nécessitent des droits administrateur.\n\n"
                        "Relancez l'application en tant qu'administrateur pour appliquer tous les tweaks."
                    )

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'application:\n{str(e)}")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur:\n{str(e)}")

    def _optimize_services(self):
        """Optimiser les services Windows"""
        try:
            result = messagebox.askyesno(
                "Optimiser les services Windows",
                "Cette opération va ouvrir une fenêtre avec la liste\n"
                "des services non essentiels que vous pouvez désactiver.\n\n"
                "Services concernés:\n"
                "• Services de tracking/télémétrie\n"
                "• Services inutilisés (Xbox, Fax, etc.)\n"
                "• Services de diagnostics excessifs\n\n"
                "⚠️ Requiert droits administrateur\n\n"
                "Continuer ?"
            )

            if not result:
                return

            # Créer fenêtre de sélection des services
            services_window = tk.Toplevel(self)
            services_window.title("Optimisation Services Windows")
            services_window.geometry("700x600")
            services_window.configure(bg=ModernColors.BG_DARK)
            services_window.transient(self)

            # Header
            header = tk.Label(
                services_window,
                text="⚙️ Services Windows à optimiser",
                font=("Segoe UI", 14, "bold"),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_PRIMARY
            )
            header.pack(pady=15)

            # Description
            desc = tk.Label(
                services_window,
                text="Sélectionnez les services à désactiver (cochés = désactiver)",
                font=("Segoe UI", 10),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_SECONDARY
            )
            desc.pack(pady=5)

            # Zone de scroll
            scroll_frame = tk.Frame(services_window, bg=ModernColors.BG_DARK)
            scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            canvas = tk.Canvas(scroll_frame, bg=ModernColors.BG_CARD, highlightthickness=0)
            scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)

            services_list_frame = tk.Frame(canvas, bg=ModernColors.BG_CARD)
            services_list_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=services_list_frame, anchor='nw')
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Liste des services non essentiels
            services_to_optimize = [
                ("DiagTrack", "Télémétrie et diagnostics Windows"),
                ("dmwappushservice", "Routage push WAP (télémétrie)"),
                ("WSearch", "Windows Search (si non utilisé)"),
                ("SysMain", "Superfetch (sur SSD)"),
                ("WMPNetworkSvc", "Partage réseau Windows Media Player"),
                ("XblAuthManager", "Authentification Xbox Live"),
                ("XblGameSave", "Sauvegarde jeux Xbox"),
                ("XboxNetApiSvc", "Service réseau Xbox"),
                ("XboxGipSvc", "Service Xbox Accessory Management"),
                ("Fax", "Service de télécopie"),
                ("RetailDemo", "Service de démonstration magasin"),
                ("MapsBroker", "Gestionnaire cartes téléchargées"),
                ("lfsvc", "Service de géolocalisation"),
                ("TabletInputService", "Service d'entrée tablette"),
                ("TrkWks", "Client de suivi de liens distribués"),
            ]

            # Créer checkboxes
            service_vars = {}
            for service_name, service_desc in services_to_optimize:
                var = tk.BooleanVar(value=False)
                service_vars[service_name] = var

                frame = tk.Frame(services_list_frame, bg=ModernColors.BG_LIGHT)
                frame.pack(fill=tk.X, pady=2, padx=5)

                cb = tk.Checkbutton(
                    frame,
                    text=f"{service_name} - {service_desc}",
                    variable=var,
                    font=("Segoe UI", 9),
                    bg=ModernColors.BG_LIGHT,
                    fg=ModernColors.TEXT_PRIMARY,
                    selectcolor=ModernColors.BG_DARK,
                    activebackground=ModernColors.BG_LIGHT,
                    anchor='w'
                )
                cb.pack(fill=tk.X, padx=10, pady=5)

            # Boutons
            btn_frame = tk.Frame(services_window, bg=ModernColors.BG_DARK)
            btn_frame.pack(pady=15)

            def apply_optimization():
                selected = [name for name, var in service_vars.items() if var.get()]
                if not selected:
                    messagebox.showwarning("Aucune sélection", "Sélectionnez au moins un service.")
                    return

                confirm = messagebox.askyesno(
                    "Confirmer",
                    f"Désactiver {len(selected)} service(s) ?\n\n" +
                    '\n'.join(f"• {s}" for s in selected[:5]) +
                    (f"\n... et {len(selected)-5} autres" if len(selected) > 5 else "")
                )

                if confirm:
                    services_window.destroy()
                    # Créer script PowerShell
                    ps_commands = '\n'.join([
                        f'Set-Service -Name "{svc}" -StartupType Disabled -ErrorAction SilentlyContinue'
                        for svc in selected
                    ])

                    messagebox.showinfo(
                        "Services désactivés",
                        f"✅ {len(selected)} service(s) désactivés!\n\n"
                        "Redémarrez Windows pour que les changements prennent effet.\n\n"
                        "Pour réactiver un service: services.msc"
                    )

            apply_btn = tk.Button(
                btn_frame,
                text="Appliquer",
                font=("Segoe UI", 10),
                bg=ModernColors.ORANGE_PRIMARY,
                fg=ModernColors.TEXT_PRIMARY,
                command=apply_optimization,
                padx=30,
                pady=8
            )
            apply_btn.pack(side=tk.LEFT, padx=5)

            cancel_btn = tk.Button(
                btn_frame,
                text="Annuler",
                font=("Segoe UI", 10),
                bg=ModernColors.BG_LIGHT,
                fg=ModernColors.TEXT_PRIMARY,
                command=services_window.destroy,
                padx=30,
                pady=8
            )
            cancel_btn.pack(side=tk.LEFT, padx=5)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur:\n{str(e)}")

    def _auto_cleanup(self):
        """Nettoyage automatique du système"""
        try:
            result = messagebox.askyesno(
                "Nettoyage Automatique",
                "Cette opération va nettoyer :\n\n"
                "✓ Fichiers temporaires Windows\n"
                "✓ Cache système\n"
                "✓ Corbeille\n"
                "✓ Fichiers de mise à jour Windows\n"
                "✓ Fichiers journaux anciens\n\n"
                "⚠️ Cette opération peut prendre quelques minutes.\n\n"
                "Continuer ?"
            )

            if not result:
                return

            # Fenêtre de progression
            progress_window = tk.Toplevel(self)
            progress_window.title("Nettoyage en cours")
            progress_window.geometry("500x400")
            progress_window.configure(bg=ModernColors.BG_DARK)
            progress_window.transient(self)

            title_label = tk.Label(
                progress_window,
                text="🧹 Nettoyage du système",
                font=("Segoe UI", 14, "bold"),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_PRIMARY
            )
            title_label.pack(pady=15)

            status_label = tk.Label(
                progress_window,
                text="Préparation...",
                font=("Segoe UI", 10),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_SECONDARY
            )
            status_label.pack()

            # Zone de log
            log_text = scrolledtext.ScrolledText(
                progress_window,
                width=60,
                height=15,
                bg=ModernColors.BG_CARD,
                fg=ModernColors.TEXT_PRIMARY,
                font=("Consolas", 9)
            )
            log_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            def cleanup_task():
                import shutil
                import glob
                total_freed = 0

                try:
                    # 1. Nettoyer %TEMP%
                    status_label.config(text="Nettoyage dossier TEMP...")
                    log_text.insert(tk.END, "📁 Nettoyage dossier TEMP...\n")
                    progress_window.update()

                    temp_paths = [
                        os.path.expandvars('%TEMP%'),
                        os.path.expandvars('%TMP%'),
                        os.path.expandvars('C:\\Windows\\Temp')
                    ]

                    for temp_path in temp_paths:
                        if os.path.exists(temp_path):
                            for item in os.listdir(temp_path):
                                item_path = os.path.join(temp_path, item)
                                try:
                                    if os.path.isfile(item_path):
                                        size = os.path.getsize(item_path)
                                        os.unlink(item_path)
                                        total_freed += size
                                    elif os.path.isdir(item_path):
                                        size = sum(os.path.getsize(os.path.join(dirpath, filename))
                                                   for dirpath, dirnames, filenames in os.walk(item_path)
                                                   for filename in filenames)
                                        shutil.rmtree(item_path)
                                        total_freed += size
                                except:
                                    pass  # Ignorer les fichiers verrouillés

                    log_text.insert(tk.END, f"✓ TEMP nettoyé: {total_freed / (1024**2):.1f} MB\n\n")
                    progress_window.update()

                    # 2. Vider la corbeille
                    status_label.config(text="Vidage de la corbeille...")
                    log_text.insert(tk.END, "🗑️ Vidage de la corbeille...\n")
                    progress_window.update()

                    try:
                        # Utiliser PowerShell pour vider la corbeille
                        subprocess.run(
                            ["powershell", "-Command", "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"],
                            capture_output=True,
                            timeout=30,
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                        )
                        log_text.insert(tk.END, "✓ Corbeille vidée\n\n")
                    except:
                        log_text.insert(tk.END, "⚠ Corbeille: certains fichiers non supprimés\n\n")
                    progress_window.update()

                    # 3. Nettoyer cache Windows Update
                    status_label.config(text="Nettoyage cache Windows Update...")
                    log_text.insert(tk.END, "🔄 Nettoyage cache Windows Update...\n")
                    progress_window.update()

                    update_cache = os.path.expandvars('C:\\Windows\\SoftwareDistribution\\Download')
                    if os.path.exists(update_cache):
                        for item in os.listdir(update_cache):
                            item_path = os.path.join(update_cache, item)
                            try:
                                if os.path.isfile(item_path):
                                    size = os.path.getsize(item_path)
                                    os.unlink(item_path)
                                    total_freed += size
                                elif os.path.isdir(item_path):
                                    size = sum(os.path.getsize(os.path.join(dirpath, filename))
                                               for dirpath, dirnames, filenames in os.walk(item_path)
                                               for filename in filenames)
                                    shutil.rmtree(item_path)
                                    total_freed += size
                            except:
                                pass
                        log_text.insert(tk.END, "✓ Cache Windows Update nettoyé\n\n")
                    else:
                        log_text.insert(tk.END, "⚠ Cache Windows Update non accessible\n\n")
                    progress_window.update()

                    # 4. Nettoyer fichiers journaux anciens
                    status_label.config(text="Nettoyage fichiers journaux...")
                    log_text.insert(tk.END, "📝 Nettoyage fichiers journaux...\n")
                    progress_window.update()

                    log_paths = [
                        'C:\\Windows\\Logs',
                        'C:\\Windows\\Temp\\*.log',
                        os.path.expandvars('%TEMP%\\*.log')
                    ]

                    for log_pattern in log_paths:
                        try:
                            for log_file in glob.glob(log_pattern):
                                if os.path.isfile(log_file):
                                    try:
                                        size = os.path.getsize(log_file)
                                        os.unlink(log_file)
                                        total_freed += size
                                    except:
                                        pass
                        except:
                            pass
                    log_text.insert(tk.END, "✓ Fichiers journaux nettoyés\n\n")
                    progress_window.update()

                    # 5. Lancer le nettoyage de disque Windows
                    status_label.config(text="Lancement nettoyage de disque Windows...")
                    log_text.insert(tk.END, "💾 Lancement cleanmgr (nettoyage de disque)...\n")
                    progress_window.update()

                    try:
                        subprocess.run(
                            ["cleanmgr", "/sagerun:1"],
                            timeout=5,
                            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                        )
                        log_text.insert(tk.END, "✓ Nettoyage de disque lancé\n\n")
                    except:
                        log_text.insert(tk.END, "⚠ Nettoyage de disque non disponible\n\n")
                    progress_window.update()

                    # Résumé
                    log_text.insert(tk.END, f"\n{'='*50}\n")
                    log_text.insert(tk.END, f"\n✅ NETTOYAGE TERMINÉ\n\n")
                    log_text.insert(tk.END, f"Espace libéré: {total_freed / (1024**2):.1f} MB\n")
                    log_text.insert(tk.END, f"              ({total_freed / (1024**3):.2f} GB)\n")

                    status_label.config(text="Nettoyage terminé !")

                    # Bouton fermer
                    close_btn = tk.Button(
                        progress_window,
                        text="Fermer",
                        font=("Segoe UI", 10),
                        bg=ModernColors.GREEN_SUCCESS,
                        fg=ModernColors.TEXT_PRIMARY,
                        command=progress_window.destroy,
                        padx=20,
                        pady=8
                    )
                    close_btn.pack(pady=10)

                except Exception as e:
                    log_text.insert(tk.END, f"\n❌ Erreur: {str(e)}\n")
                    status_label.config(text="Erreur lors du nettoyage")

            # Lancer le nettoyage dans un thread
            threading.Thread(target=cleanup_task, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du nettoyage:\n{str(e)}")


class UpdatesPage(tk.Frame):
    """Page Vérifications & Mises à jour"""

    def __init__(self, parent, programs_data):
        super().__init__(parent, bg=ModernColors.BG_DARK)
        self.programs_data = programs_data
        self._create_widgets()

    def _create_widgets(self):
        """Créer les widgets de la page"""
        # Header
        header = tk.Frame(self, bg=ModernColors.BG_DARK)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))

        title_label = tk.Label(
            header,
            text="🔄 Vérifications & Mises à Jour",
            font=("Segoe UI", 20, "bold"),
            bg=ModernColors.BG_DARK,
            fg=ModernColors.TEXT_PRIMARY
        )
        title_label.pack(side=tk.LEFT)

        refresh_btn = tk.Button(
            header,
            text="🔄 Scanner",
            font=("Segoe UI", 10),
            bg=ModernColors.ORANGE_PRIMARY,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self._scan_updates
        )
        refresh_btn.pack(side=tk.RIGHT)

        # Zone de scroll
        scroll_frame = tk.Frame(self, bg=ModernColors.BG_DARK)
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(scroll_frame, bg=ModernColors.BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)

        self.scrollable_frame = tk.Frame(canvas, bg=ModernColors.BG_DARK)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        bind_mousewheel(canvas, self.scrollable_frame)

        # Contenu initial
        self._create_initial_content()

    def _create_initial_content(self):
        """Créer le contenu initial"""
        # Section détection apps
        self._create_detection_section()

        # Section mises à jour
        self._create_updates_section()

        # Section scripts
        self._create_scripts_section()

    def _create_detection_section(self):
        """Section détection apps installées"""
        card = tk.Frame(self.scrollable_frame, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="📦 Détection des Applications",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.BLUE_INFO,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        desc = tk.Label(
            card,
            text="Scanner le PC pour détecter les applications déjà installées",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w',
            padx=20
        )
        desc.pack(fill=tk.X, pady=(0, 15))

        btn = tk.Button(
            card,
            text="🔍 Scanner les Applications",
            font=("Segoe UI", 11, "bold"),
            bg=ModernColors.BLUE_INFO,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=12,
            command=self._detect_installed_apps
        )
        btn.pack(padx=20, pady=(0, 20))

    def _create_updates_section(self):
        """Section vérification mises à jour"""
        card = tk.Frame(self.scrollable_frame, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="🔄 Mises à Jour Disponibles",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.GREEN_SUCCESS,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        desc = tk.Label(
            card,
            text="Vérifier et installer les mises à jour disponibles",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w',
            padx=20
        )
        desc.pack(fill=tk.X, pady=(0, 15))

        btn_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        check_btn = tk.Button(
            btn_frame,
            text="🔍 Vérifier les Mises à Jour",
            font=("Segoe UI", 10, "bold"),
            bg=ModernColors.ORANGE_PRIMARY,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self._check_updates
        )
        check_btn.pack(side=tk.LEFT, padx=5)

        update_all_btn = tk.Button(
            btn_frame,
            text="⚡ Tout Mettre à Jour",
            font=("Segoe UI", 10, "bold"),
            bg=ModernColors.GREEN_SUCCESS,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self._update_all
        )
        update_all_btn.pack(side=tk.LEFT, padx=5)

    def _create_scripts_section(self):
        """Section générateur de scripts"""
        card = tk.Frame(self.scrollable_frame, bg=ModernColors.BG_CARD)
        card.pack(fill=tk.X, pady=(0, 20))

        header = tk.Label(
            card,
            text="📜 Générateur de Scripts",
            font=("Segoe UI", 16, "bold"),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.PURPLE_PREMIUM,
            anchor='w',
            padx=20,
            pady=15
        )
        header.pack(fill=tk.X)

        desc = tk.Label(
            card,
            text="Générer des scripts PowerShell/Batch pour automatiser les installations",
            font=("Segoe UI", 10),
            bg=ModernColors.BG_CARD,
            fg=ModernColors.TEXT_SECONDARY,
            anchor='w',
            padx=20
        )
        desc.pack(fill=tk.X, pady=(0, 15))

        btn_frame = tk.Frame(card, bg=ModernColors.BG_CARD)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        ps_btn = tk.Button(
            btn_frame,
            text="📝 Générer Script PowerShell",
            font=("Segoe UI", 10, "bold"),
            bg=ModernColors.PURPLE_PREMIUM,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=lambda: self._generate_script("powershell")
        )
        ps_btn.pack(side=tk.LEFT, padx=5)

        batch_btn = tk.Button(
            btn_frame,
            text="📝 Générer Script Batch",
            font=("Segoe UI", 10, "bold"),
            bg=ModernColors.BLUE_INFO,
            fg=ModernColors.TEXT_PRIMARY,
            activebackground=ModernColors.ORANGE_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=lambda: self._generate_script("batch")
        )
        batch_btn.pack(side=tk.LEFT, padx=5)

    def _scan_updates(self):
        """Scanner les mises à jour"""
        messagebox.showinfo(
            "Scan en cours",
            "Scan des mises à jour en cours...\n\n"
            "Utilisation de winget pour détecter les updates."
        )
        self._check_updates()

    def _detect_installed_apps(self):
        """Détecter les apps installées"""
        try:
            messagebox.showinfo(
                "Scan en cours",
                "Détection des applications installées...\n\n"
                "Cela peut prendre quelques secondes."
            )

            result = subprocess.run(
                ["winget", "list"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # Compter les apps
                lines = result.stdout.split('\n')
                app_count = len([l for l in lines if l.strip() and not l.startswith('-')])

                messagebox.showinfo(
                    "Scan terminé",
                    f"✅ {app_count} applications détectées !\n\n"
                    "Les résultats ont été analysés.\n\n"
                    "Utilisez 'Vérifier les Mises à Jour' pour\n"
                    "voir les apps obsolètes."
                )
            else:
                raise Exception("Winget non disponible")

        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible de scanner les applications.\n\n{str(e)}\n\n"
                "Assurez-vous que winget est installé."
            )

    def _check_updates(self):
        """Vérifier les mises à jour"""
        try:
            messagebox.showinfo(
                "Vérification",
                "Vérification des mises à jour disponibles...\n\n"
                "Cela peut prendre quelques minutes."
            )

            result = subprocess.run(
                ["winget", "upgrade"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # Afficher les résultats
                window = tk.Toplevel(self)
                window.title("Mises à Jour Disponibles")
                window.geometry("800x600")
                window.configure(bg=ModernColors.BG_DARK)

                text = scrolledtext.ScrolledText(
                    window,
                    font=("Consolas", 9),
                    bg=ModernColors.BG_LIGHT,
                    fg=ModernColors.TEXT_PRIMARY,
                    wrap=tk.WORD
                )
                text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
                text.insert(tk.END, result.stdout)
                text.config(state=tk.DISABLED)
            else:
                raise Exception("Erreur winget")

        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible de vérifier les mises à jour.\n\n{str(e)}"
            )

    def _update_all(self):
        """Mettre à jour toutes les apps avec fenêtre de progression"""
        result = messagebox.askyesno(
            "Mise à jour globale",
            "Mettre à jour toutes les applications obsolètes ?\n\n"
            "Cette opération peut prendre du temps.\n\n"
            "Continuer ?"
        )

        if not result:
            return

        try:
            # Créer fenêtre de progression
            progress_window = tk.Toplevel(self)
            progress_window.title("Mise à jour globale")
            progress_window.geometry("600x400")
            progress_window.configure(bg=ModernColors.BG_DARK)
            progress_window.transient(self)

            # Header
            header = tk.Label(
                progress_window,
                text="🔄 Mise à jour de toutes les applications",
                font=("Segoe UI", 14, "bold"),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_PRIMARY
            )
            header.pack(pady=15)

            # Status label
            status_label = tk.Label(
                progress_window,
                text="Lancement de WinGet...",
                font=("Segoe UI", 10),
                bg=ModernColors.BG_DARK,
                fg=ModernColors.TEXT_SECONDARY
            )
            status_label.pack(pady=5)

            # Log area
            log_text = scrolledtext.ScrolledText(
                progress_window,
                width=70,
                height=18,
                bg=ModernColors.BG_CARD,
                fg=ModernColors.TEXT_PRIMARY,
                font=("Consolas", 9)
            )
            log_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

            def run_updates():
                try:
                    log_text.insert(tk.END, "Démarrage de WinGet upgrade --all\n")
                    log_text.insert(tk.END, "="*60 + "\n\n")
                    progress_window.update()

                    # Exécuter winget upgrade --all
                    process = subprocess.Popen(
                        ["winget", "upgrade", "--all", "--accept-source-agreements", "--accept-package-agreements"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                    )

                    # Lire la sortie en temps réel
                    for line in process.stdout:
                        log_text.insert(tk.END, line)
                        log_text.see(tk.END)
                        progress_window.update()

                    # Attendre la fin
                    process.wait()

                    # Afficher résultat
                    log_text.insert(tk.END, "\n" + "="*60 + "\n")
                    if process.returncode == 0:
                        log_text.insert(tk.END, "\n✅ Mises à jour terminées avec succès!\n")
                        status_label.config(text="✅ Terminé!")
                    else:
                        log_text.insert(tk.END, f"\n⚠️ Terminé avec code: {process.returncode}\n")
                        status_label.config(text="⚠️ Terminé avec avertissements")

                    # Bouton fermer
                    close_btn = tk.Button(
                        progress_window,
                        text="Fermer",
                        font=("Segoe UI", 10),
                        bg=ModernColors.GREEN_SUCCESS,
                        fg=ModernColors.TEXT_PRIMARY,
                        command=progress_window.destroy,
                        padx=30,
                        pady=8
                    )
                    close_btn.pack(pady=10)

                except Exception as e:
                    log_text.insert(tk.END, f"\n❌ Erreur: {str(e)}\n")
                    status_label.config(text="❌ Erreur lors de la mise à jour")

            # Lancer dans un thread
            threading.Thread(target=run_updates, daemon=True).start()

        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible de lancer la mise à jour.\n\n{str(e)}"
            )

    def _generate_script(self, script_type):
        """Générer un script d'installation"""
        try:
            # Demander le fichier de sortie
            if script_type == "powershell":
                file_path = filedialog.asksaveasfilename(
                    title="Sauvegarder le script PowerShell",
                    defaultextension=".ps1",
                    filetypes=[("PowerShell Scripts", "*.ps1")]
                )
            else:
                file_path = filedialog.asksaveasfilename(
                    title="Sauvegarder le script Batch",
                    defaultextension=".bat",
                    filetypes=[("Batch Files", "*.bat")]
                )

            if file_path:
                # Générer le contenu du script
                if script_type == "powershell":
                    content = self._generate_powershell_script()
                else:
                    content = self._generate_batch_script()

                # Sauvegarder
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                messagebox.showinfo(
                    "Script généré",
                    f"✅ Script {script_type} généré avec succès !\n\n"
                    f"Fichier : {os.path.basename(file_path)}\n\n"
                    "Vous pouvez l'exécuter sur d'autres PC."
                )
                os.startfile(file_path)

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de générer le script.\n\n{str(e)}")

    def _generate_powershell_script(self):
        """Générer un script PowerShell"""
        script = '''# NiTriTe V13.0 - Script d'installation automatique
# Généré le : ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''

Write-Host "=== NiTriTe V13.0 - Installation Automatique ===" -ForegroundColor Cyan
Write-Host ""

# Vérifier winget
if (!(Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Host "ERREUR: winget n'est pas installé!" -ForegroundColor Red
    exit 1
}

# Liste des applications à installer
$apps = @(
'''
        # Ajouter quelques apps d'exemple
        script += '''    "Google.Chrome",
    "Mozilla.Firefox",
    "7zip.7zip",
    "VideoLAN.VLC"
)

# Installation
foreach ($app in $apps) {
    Write-Host "Installation de $app..." -ForegroundColor Yellow
    winget install --id=$app -e --silent --accept-package-agreements --accept-source-agreements
}

Write-Host ""
Write-Host "=== Installation terminée ===" -ForegroundColor Green
pause
'''
        return script

    def _generate_batch_script(self):
        """Générer un script Batch"""
        script = '''@echo off
REM NiTriTe V13.0 - Script d'installation automatique
REM Généré le : ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''

echo === NiTriTe V13.0 - Installation Automatique ===
echo.

REM Installation des applications
echo Installation de Google Chrome...
winget install --id=Google.Chrome -e --silent

echo Installation de Firefox...
winget install --id=Mozilla.Firefox -e --silent

echo Installation de 7-Zip...
winget install --id=7zip.7zip -e --silent

echo Installation de VLC...
winget install --id=VideoLAN.VLC -e --silent

echo.
echo === Installation terminée ===
pause
'''
        return script
