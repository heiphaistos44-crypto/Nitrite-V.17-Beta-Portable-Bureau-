"""
Interface GUI pour outils réseau avancés - NiTriTe V13
Scanner réseau, ports, connexions, test vitesse
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import customtkinter as ctk
import threading
import logging
from datetime import datetime
from typing import Dict

try:
    from network_manager import NetworkManager
except ImportError:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    from network_manager import NetworkManager


class NetworkToolsGUI(ctk.CTkFrame):
    """Interface graphique pour outils réseau avancés"""

    def __init__(self, parent_frame, colors=None):
        # Initialiser le Frame parent
        super().__init__(parent_frame, fg_color='#0a0a0a', corner_radius=0)

        self.logger = logging.getLogger(__name__)

        # Couleurs
        self.colors = colors or {
            'bg': '#0a0a0a',
            'fg': '#ffffff',
            'primary': '#ff6b00',
            'secondary': '#1e1e2e',
            'success': '#00e676',
            'warning': '#ffa000',
            'danger': '#ff3d00',
            'text_secondary': '#888888',
            'border': '#333333'
        }

        # Network manager
        self.network_manager = NetworkManager()

        # État
        self.is_scanning = False

        # Interface
        self.create_ui()

        # Charger infos initiales (après un délai pour éviter erreur thread)
        self.after(100, self.load_initial_info)

    def create_ui(self):
        """Crée l'interface utilisateur"""
        # Container principal avec scrollbar (self est déjà le Frame principal)
        main_container = ctk.CTkFrame(self, fg_color=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_container, fg_color=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient=tk.VERTICAL, command=canvas.yview)

        self.scrollable_frame = ctk.CTkFrame(canvas, fg_color=self.colors['bg'])
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Header
        self._create_header()

        # Notebook avec onglets
        self.notebook = ttk.Notebook(self.scrollable_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Onglet 1: Informations
        self.info_tab = ctk.CTkFrame(self.notebook, fg_color=self.colors['bg'])
        self.notebook.add(self.info_tab, text="  📡 Informations  ")
        self._create_info_tab()

        # Onglet 2: Connexions actives
        self.connections_tab = ctk.CTkFrame(self.notebook, fg_color=self.colors['bg'])
        self.notebook.add(self.connections_tab, text="  🔌 Connexions  ")
        self._create_connections_tab()

        # Onglet 3: Scanner réseau
        self.scanner_tab = ctk.CTkFrame(self.notebook, fg_color=self.colors['bg'])
        self.notebook.add(self.scanner_tab, text="  🔍 Scanner Réseau  ")
        self._create_scanner_tab()

        # Onglet 4: Scanner de ports
        self.ports_tab = ctk.CTkFrame(self.notebook, fg_color=self.colors['bg'])
        self.notebook.add(self.ports_tab, text="  🔐 Ports  ")
        self._create_ports_tab()

        # Onglet 5: Test de vitesse
        self.speed_tab = ctk.CTkFrame(self.notebook, fg_color=self.colors['bg'])
        self.notebook.add(self.speed_tab, text="  ⚡ Vitesse  ")
        self._create_speed_tab()

    def _create_header(self):
        """Crée le header"""
        header = ctk.CTkFrame(self.scrollable_frame, fg_color=self.colors['secondary'], height=60)
        header.pack(fill=tk.X, padx=10, pady=10)
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="🌐 Outils Réseau Avancés",
            fg_color=self.colors['secondary'],
            text_color=self.colors['primary'],
            font=('Segoe UI', 16, 'bold')
        )
        title.pack(side=tk.LEFT, padx=20)

    def _create_info_tab(self):
        """Onglet informations réseau"""
        container = ctk.CTkFrame(self.info_tab, fg_color=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # IP locale
        self._create_info_section(container, "💻 Réseau Local")

        self.local_ip_label = self._create_info_row(container, "IP Locale:", "Chargement...")
        self.hostname_label = self._create_info_row(container, "Nom d'hôte:", "Chargement...")

        # IP publique
        ctk.CTkFrame(container, fg_color=self.colors['bg'], height=20).pack()
        self._create_info_section(container, "🌍 Internet")

        self.public_ip_label = self._create_info_row(container, "IP Publique:", "Chargement...")
        self.location_label = self._create_info_row(container, "Localisation:", "Chargement...")
        self.isp_label = self._create_info_row(container, "FAI:", "Chargement...")

        # DNS
        ctk.CTkFrame(container, fg_color=self.colors['bg'], height=20).pack()
        self._create_info_section(container, "🔧 Configuration")

        self.dns_label = self._create_info_row(container, "Serveurs DNS:", "Chargement...")

        # Interfaces
        ctk.CTkFrame(container, fg_color=self.colors['bg'], height=20).pack()
        self._create_info_section(container, "🔌 Interfaces Réseau")

        self.interfaces_text = scrolledtext.ScrolledText(
            container,
            fg_color='#1a1a1a',
            text_color=self.colors['fg'],
            font=('Consolas', 9),
            height=10,
            wrap=tk.WORD
        )
        self.interfaces_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Bouton refresh
        refresh_btn = ctk.CTkButton(
            container,
            text="🔄 Actualiser",
            command=self.load_initial_info,
            fg_color=self.colors['primary'],
            text_color='white',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        refresh_btn.pack(pady=10)

    def _create_connections_tab(self):
        """Onglet connexions actives"""
        container = ctk.CTkFrame(self.connections_tab, fg_color=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header = ctk.CTkFrame(container, fg_color=self.colors['bg'])
        header.pack(fill=tk.X, pady=10)

        ctk.CTkLabel(
            header,
            text="Connexions réseau actives",
            fg_color=self.colors['bg'],
            text_color=self.colors['fg'],
            font=('Segoe UI', 12, 'bold')
        ).pack(side=tk.LEFT)

        self.conn_count_label = ctk.CTkLabel(
            header,
            text="0 connexions",
            fg_color=self.colors['secondary'],
            text_color=self.colors['primary'],
            font=('Segoe UI', 10, 'bold'),
            padx=10,
            pady=5
        )
        self.conn_count_label.pack(side=tk.RIGHT)

        # Filtres
        filter_frame = ctk.CTkFrame(container, fg_color=self.colors['bg'])
        filter_frame.pack(fill=tk.X, pady=10)

        ctk.CTkLabel(
            filter_frame,
            text="Filtre:",
            fg_color=self.colors['bg'],
            text_color=self.colors['text_secondary'],
            font=('Segoe UI', 9)
        ).pack(side=tk.LEFT, padx=5)

        self.conn_filter_var = tk.StringVar(value="all")

        filters = [("Tout", "all"), ("TCP", "tcp"), ("UDP", "udp"), ("ESTABLISHED", "established")]
        for text, value in filters:
            tk.Radiobutton(
                filter_frame,
                text=text,
                variable=self.conn_filter_var,
                value=value,
                fg_color=self.colors['bg'],
                text_color=self.colors['fg'],
                selectcolor=self.colors['secondary'],
                activebackground=self.colors['bg'],
                font=('Segoe UI', 9),
                command=self.refresh_connections
            ).pack(side=tk.LEFT, padx=5)

        # Treeview pour connexions
        tree_frame = ctk.CTkFrame(container, fg_color=self.colors['bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ('Process', 'Protocol', 'Local', 'Remote', 'Status')
        self.connections_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)

        self.connections_tree.heading('Process', text='Processus')
        self.connections_tree.heading('Protocol', text='Protocole')
        self.connections_tree.heading('Local', text='Adresse Locale')
        self.connections_tree.heading('Remote', text='Adresse Distante')
        self.connections_tree.heading('Status', text='État')

        self.connections_tree.column('Process', width=150)
        self.connections_tree.column('Protocol', width=80)
        self.connections_tree.column('Local', width=180)
        self.connections_tree.column('Remote', width=180)
        self.connections_tree.column('Status', width=120)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.connections_tree.yview)
        self.connections_tree.configure(yscrollcommand=scrollbar.set)

        self.connections_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bouton refresh
        ctk.CTkButton(
            container,
            text="🔄 Actualiser Connexions",
            command=self.refresh_connections,
            fg_color=self.colors['success'],
            text_color='white',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        ).pack(pady=10)

    def _create_scanner_tab(self):
        """Onglet scanner réseau"""
        container = ctk.CTkFrame(self.scanner_tab, fg_color=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configuration
        config_frame = ctk.CTkFrame(container, fg_color=self.colors['secondary'], relief=tk.FLAT)
        config_frame.pack(fill=tk.X, pady=10, padx=5)
        config_frame.configure(highlightbackground=self.colors['border'], highlightthickness=1)

        ctk.CTkLabel(
            config_frame,
            text="Configuration du scan",
            fg_color=self.colors['secondary'],
            text_color=self.colors['fg'],
            font=('Segoe UI', 10, 'bold')
        ).pack(pady=10)

        # Réseau à scanner
        input_frame = ctk.CTkFrame(config_frame, fg_color=self.colors['secondary'])
        input_frame.pack(fill=tk.X, padx=20, pady=5)

        ctk.CTkLabel(
            input_frame,
            text="Réseau:",
            fg_color=self.colors['secondary'],
            text_color=self.colors['text_secondary'],
            font=('Segoe UI', 9)
        ).pack(side=tk.LEFT, padx=5)

        self.network_entry = ctk.CTkEntry(
            input_frame,
            fg_color='#1a1a1a',
            text_color=self.colors['fg'],
            font=('Segoe UI', 10),
            insertbackground=self.colors['primary']
        )
        self.network_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.network_entry.insert(0, "192.168.1.0/24")

        ctk.CTkLabel(
            input_frame,
            text="(ex: 192.168.1.0/24)",
            fg_color=self.colors['secondary'],
            text_color=self.colors['text_secondary'],
            font=('Segoe UI', 8)
        ).pack(side=tk.LEFT, padx=5)

        # Bouton scan
        self.scan_btn = ctk.CTkButton(
            config_frame,
            text="🔍 Démarrer le Scan",
            command=self.start_network_scan,
            fg_color=self.colors['primary'],
            text_color='white',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2'
        )
        self.scan_btn.pack(pady=10)

        # Barre de progression
        self.scan_progress = ttk.Progressbar(config_frame, mode='determinate')
        self.scan_progress.pack(fill=tk.X, padx=20, pady=5)

        self.scan_status_label = ctk.CTkLabel(
            config_frame,
            text="Prêt",
            fg_color=self.colors['secondary'],
            text_color=self.colors['text_secondary'],
            font=('Segoe UI', 9)
        )
        self.scan_status_label.pack(pady=5)

        # Résultats
        ctk.CTkLabel(
            container,
            text="Appareils découverts",
            fg_color=self.colors['bg'],
            text_color=self.colors['fg'],
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=10)

        tree_frame = ctk.CTkFrame(container, fg_color=self.colors['bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ('IP', 'Hostname', 'MAC')
        self.scan_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)

        self.scan_tree.heading('IP', text='Adresse IP')
        self.scan_tree.heading('Hostname', text='Nom d\'hôte')
        self.scan_tree.heading('MAC', text='Adresse MAC')

        self.scan_tree.column('IP', width=150)
        self.scan_tree.column('Hostname', width=250)
        self.scan_tree.column('MAC', width=150)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.scan_tree.yview)
        self.scan_tree.configure(yscrollcommand=scrollbar.set)

        self.scan_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _create_ports_tab(self):
        """Onglet scanner de ports"""
        container = ctk.CTkFrame(self.ports_tab, fg_color=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configuration
        config_frame = ctk.CTkFrame(container, fg_color=self.colors['secondary'], relief=tk.FLAT)
        config_frame.pack(fill=tk.X, pady=10, padx=5)
        config_frame.configure(highlightbackground=self.colors['border'], highlightthickness=1)

        ctk.CTkLabel(
            config_frame,
            text="Scanner de Ports",
            fg_color=self.colors['secondary'],
            text_color=self.colors['fg'],
            font=('Segoe UI', 10, 'bold')
        ).pack(pady=10)

        # Host à scanner
        input_frame = ctk.CTkFrame(config_frame, fg_color=self.colors['secondary'])
        input_frame.pack(fill=tk.X, padx=20, pady=5)

        ctk.CTkLabel(
            input_frame,
            text="Hôte:",
            fg_color=self.colors['secondary'],
            text_color=self.colors['text_secondary'],
            font=('Segoe UI', 9)
        ).pack(side=tk.LEFT, padx=5)

        self.port_host_entry = ctk.CTkEntry(
            input_frame,
            fg_color='#1a1a1a',
            text_color=self.colors['fg'],
            font=('Segoe UI', 10),
            insertbackground=self.colors['primary']
        )
        self.port_host_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.port_host_entry.insert(0, "127.0.0.1")

        # Bouton scan
        self.port_scan_btn = ctk.CTkButton(
            config_frame,
            text="🔐 Scanner Ports Communs",
            command=self.start_port_scan,
            fg_color=self.colors['primary'],
            text_color='white',
            font=('Segoe UI', 10, 'bold'),
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2'
        )
        self.port_scan_btn.pack(pady=10)

        # Progression
        self.port_progress = ttk.Progressbar(config_frame, mode='determinate')
        self.port_progress.pack(fill=tk.X, padx=20, pady=5)

        self.port_status_label = ctk.CTkLabel(
            config_frame,
            text="Prêt",
            fg_color=self.colors['secondary'],
            text_color=self.colors['text_secondary'],
            font=('Segoe UI', 9)
        )
        self.port_status_label.pack(pady=5)

        # Résultats
        ctk.CTkLabel(
            container,
            text="Ports ouverts",
            fg_color=self.colors['bg'],
            text_color=self.colors['fg'],
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=10)

        tree_frame = ctk.CTkFrame(container, fg_color=self.colors['bg'])
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ('Port', 'État', 'Service', 'Protocole')
        self.ports_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)

        self.ports_tree.heading('Port', text='Port')
        self.ports_tree.heading('État', text='État')
        self.ports_tree.heading('Service', text='Service')
        self.ports_tree.heading('Protocole', text='Protocole')

        self.ports_tree.column('Port', width=100)
        self.ports_tree.column('État', width=100)
        self.ports_tree.column('Service', width=150)
        self.ports_tree.column('Protocole', width=100)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.ports_tree.yview)
        self.ports_tree.configure(yscrollcommand=scrollbar.set)

        self.ports_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _create_speed_tab(self):
        """Onglet test de vitesse"""
        container = ctk.CTkFrame(self.speed_tab, fg_color=self.colors['bg'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        ctk.CTkLabel(
            container,
            text="Test de Vitesse Internet",
            fg_color=self.colors['bg'],
            text_color=self.colors['primary'],
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=20)

        # Bouton test
        self.speed_test_btn = ctk.CTkButton(
            container,
            text="⚡ Lancer le Test",
            command=self.start_speed_test,
            fg_color=self.colors['success'],
            text_color='white',
            font=('Segoe UI', 12, 'bold'),
            bd=0,
            padx=40,
            pady=15,
            cursor='hand2'
        )
        self.speed_test_btn.pack(pady=20)

        # Status
        self.speed_status_label = ctk.CTkLabel(
            container,
            text="Appuyez sur le bouton pour démarrer",
            fg_color=self.colors['bg'],
            text_color=self.colors['text_secondary'],
            font=('Segoe UI', 10)
        )
        self.speed_status_label.pack(pady=10)

        # Résultats
        results_frame = ctk.CTkFrame(container, fg_color=self.colors['secondary'], relief=tk.FLAT)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=5)
        results_frame.configure(highlightbackground=self.colors['border'], highlightthickness=1)

        # Download
        download_frame = self._create_speed_result_widget(results_frame, "📥 Téléchargement")
        download_frame.pack(fill=tk.X, padx=20, pady=10)
        self.download_speed_label = download_frame.value_label

        # Upload
        upload_frame = self._create_speed_result_widget(results_frame, "📤 Envoi")
        upload_frame.pack(fill=tk.X, padx=20, pady=10)
        self.upload_speed_label = upload_frame.value_label

        # Ping
        ping_frame = self._create_speed_result_widget(results_frame, "🏓 Latence")
        ping_frame.pack(fill=tk.X, padx=20, pady=10)
        self.ping_label = ping_frame.value_label

    def _create_speed_result_widget(self, parent, title):
        """Crée un widget de résultat de vitesse"""
        frame = ctk.CTkFrame(parent, fg_color=self.colors['secondary'])

        ctk.CTkLabel(
            frame,
            text=title,
            fg_color=self.colors['secondary'],
            text_color=self.colors['text_secondary'],
            font=('Segoe UI', 10)
        ).pack(side=tk.LEFT)

        value_label = ctk.CTkLabel(
            frame,
            text="-- --",
            fg_color=self.colors['secondary'],
            text_color=self.colors['primary'],
            font=('Segoe UI', 14, 'bold')
        )
        value_label.pack(side=tk.RIGHT)

        frame.value_label = value_label
        return frame

    def _create_info_section(self, parent, title):
        """Crée un titre de section"""
        ctk.CTkLabel(
            parent,
            text=title,
            fg_color=self.colors['bg'],
            text_color=self.colors['primary'],
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor='w', pady=5)

    def _create_info_row(self, parent, label, value):
        """Crée une ligne d'information"""
        frame = ctk.CTkFrame(parent, fg_color=self.colors['bg'])
        frame.pack(fill=tk.X, pady=3)

        ctk.CTkLabel(
            frame,
            text=label,
            fg_color=self.colors['bg'],
            text_color=self.colors['text_secondary'],
            font=('Segoe UI', 9),
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT)

        value_label = ctk.CTkLabel(
            frame,
            text=value,
            fg_color=self.colors['bg'],
            text_color=self.colors['fg'],
            font=('Segoe UI', 9, 'bold'),
            anchor='w'
        )
        value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        return value_label

    def load_initial_info(self):
        """Charge les informations réseau initiales"""
        threading.Thread(target=self._load_info_thread, daemon=True).start()

    def _load_info_thread(self):
        """Thread de chargement des infos"""
        try:
            import socket

            # Récupérer toutes les données
            local_ip = self.network_manager.get_local_ip()
            hostname = socket.gethostname()
            dns_servers = self.network_manager.get_dns_servers()
            public_info = self.network_manager.get_public_ip()
            interfaces = self.network_manager.get_network_interfaces()

            location = f"{public_info.get('city', '')}, {public_info.get('country_name', '')}"

            # Mettre à jour l'UI dans le thread principal
            def update_ui():
                self.local_ip_label.configure(text=local_ip)
                self.hostname_label.configure(text=hostname)
                self.dns_label.configure(text=", ".join(dns_servers) if dns_servers else "Non disponible")
                self.public_ip_label.configure(text=public_info.get('ip', 'Non disponible'))
                self.location_label.configure(text=location if location != ", " else "Non disponible")
                self.isp_label.configure(text=public_info.get('org', 'Non disponible'))

                self.interfaces_text.delete('1.0', tk.END)
                for iface in interfaces:
                    if iface['is_up'] and iface['addresses']:
                        self.interfaces_text.insert(tk.END, f"📡 {iface['name']}\n", 'title')
                        for addr in iface['addresses']:
                            self.interfaces_text.insert(tk.END, f"   {addr['type']}: {addr['address']}\n")
                        self.interfaces_text.insert(tk.END, "\n")

            self.after(0, update_ui)

        except Exception as e:
            self.logger.error(f"Erreur chargement infos: {e}")
            self.after(0, lambda: messagebox.showerror("Erreur", f"Erreur lors du chargement des informations:\n{e}"))

    def refresh_connections(self):
        """Actualise la liste des connexions"""
        threading.Thread(target=self._refresh_connections_thread, daemon=True).start()

    def _refresh_connections_thread(self):
        """Thread d'actualisation des connexions"""
        try:
            connections = self.network_manager.get_active_connections()

            # Filtrer
            filter_type = self.conn_filter_var.get()
            if filter_type != "all":
                if filter_type in ["tcp", "udp"]:
                    connections = [c for c in connections if c['type'].lower() == filter_type]
                elif filter_type == "established":
                    connections = [c for c in connections if c['status'] == 'ESTABLISHED']

            # Update UI dans le thread principal
            def update_ui():
                self.connections_tree.delete(*self.connections_tree.get_children())

                for conn in connections:
                    self.connections_tree.insert('', tk.END, values=(
                        conn['process'],
                        conn['type'],
                        conn['local_addr'],
                        conn['remote_addr'],
                        conn['status']
                    ))

                self.conn_count_label.configure(text=f"{len(connections)} connexions")

            self.after(0, update_ui)

        except Exception as e:
            self.logger.error(f"Erreur refresh connexions: {e}")

    def start_network_scan(self):
        """Démarre le scan réseau"""
        if self.is_scanning:
            messagebox.showwarning("Scan en cours", "Un scan est déjà en cours")
            return

        network = self.network_entry.get().strip()
        if not network:
            messagebox.showerror("Erreur", "Veuillez entrer un réseau à scanner")
            return

        self.scan_btn.configure(state=tk.DISABLED, text="⏳ Scan en cours...")
        self.scan_tree.delete(*self.scan_tree.get_children())

        threading.Thread(target=self._network_scan_thread, args=(network,), daemon=True).start()

    def _network_scan_thread(self, network):
        """Thread de scan réseau"""
        try:
            self.is_scanning = True

            def progress(current, total, host):
                percent = (current / total) * 100
                self.after(0, lambda: self.scan_progress.configure(value=percent))
                self.after(0, lambda: self.scan_status_label.configure(text=f"Scan en cours... {current}/{total} hosts"))

            results = self.network_manager.scan_network(network, progress_callback=progress)

            # Afficher résultats dans le thread principal
            def update_results():
                for device in results:
                    self.scan_tree.insert('', tk.END, values=(
                        device['ip'],
                        device['hostname'],
                        device['mac']
                    ))
                self.scan_status_label.configure(text=f"Scan terminé - {len(results)} appareils trouvés")

            self.after(0, update_results)

        except Exception as e:
            self.logger.error(f"Erreur scan réseau: {e}")
            self.after(0, lambda: self.scan_status_label.configure(text=f"Erreur: {e}"))
        finally:
            self.is_scanning = False
            def reset_ui():
                self.scan_btn.configure(state=tk.NORMAL, text="🔍 Démarrer le Scan")
                self.scan_progress['value'] = 0
            self.after(0, reset_ui)

    def start_port_scan(self):
        """Démarre le scan de ports"""
        host = self.port_host_entry.get().strip()
        if not host:
            messagebox.showerror("Erreur", "Veuillez entrer un hôte à scanner")
            return

        self.port_scan_btn.configure(state=tk.DISABLED, text="⏳ Scan en cours...")
        self.ports_tree.delete(*self.ports_tree.get_children())

        threading.Thread(target=self._port_scan_thread, args=(host,), daemon=True).start()

    def _port_scan_thread(self, host):
        """Thread de scan de ports"""
        try:
            def progress(current, total, port):
                percent = (current / total) * 100
                self.after(0, lambda: self.port_progress.configure(value=percent))
                self.after(0, lambda: self.port_status_label.configure(text=f"Scan port {port}... {current}/{total}"))

            results = self.network_manager.scan_ports(host, progress_callback=progress)

            # Afficher résultats dans le thread principal
            def update_results():
                for port_info in results:
                    self.ports_tree.insert('', tk.END, values=(
                        port_info['port'],
                        port_info['state'],
                        port_info['service'],
                        port_info['protocol']
                    ))
                self.port_status_label.configure(text=f"Scan terminé - {len(results)} ports ouverts")

            self.after(0, update_results)

        except Exception as e:
            self.logger.error(f"Erreur scan ports: {e}")
            self.after(0, lambda: self.port_status_label.configure(text=f"Erreur: {e}"))
        finally:
            def reset_ui():
                self.port_scan_btn.configure(state=tk.NORMAL, text="🔐 Scanner Ports Communs")
                self.port_progress['value'] = 0
            self.after(0, reset_ui)

    def start_speed_test(self):
        """Démarre le test de vitesse"""
        self.speed_test_btn.configure(state=tk.DISABLED, text="⏳ Test en cours...")
        self.download_speed_label.configure(text="-- --")
        self.upload_speed_label.configure(text="-- --")
        self.ping_label.configure(text="-- --")

        threading.Thread(target=self._speed_test_thread, daemon=True).start()

    def _speed_test_thread(self):
        """Thread de test de vitesse"""
        try:
            def progress(step, message):
                self.after(0, lambda msg=message: self.speed_status_label.configure(text=msg))

            results = self.network_manager.test_internet_speed(progress_callback=progress)

            def update_results():
                if results['success']:
                    self.download_speed_label.configure(text=f"{results['download_mbps']:.1f} Mbps")
                    self.upload_speed_label.configure(text=f"{results['upload_mbps']:.1f} Mbps")
                    self.ping_label.configure(text=f"{results['ping_ms']:.0f} ms")
                    self.speed_status_label.configure(text="✅ Test terminé avec succès")
                else:
                    self.speed_status_label.configure(text=f"❌ Erreur: {results.get('error', 'Inconnue')}")

            self.after(0, update_results)

        except Exception as e:
            self.logger.error(f"Erreur test vitesse: {e}")
            self.after(0, lambda: self.speed_status_label.configure(text=f"❌ Erreur: {e}"))
        finally:
            self.after(0, lambda: self.speed_test_btn.configure(state=tk.NORMAL, text="⚡ Lancer le Test"))


# Test autonome
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    root = tk.Tk()
    root.title("Test Network Tools")
    root.geometry("1000x700")
    root.configure(fg_color='#0a0a0a')

    gui = NetworkToolsGUI(root)

    root.mainloop()
