#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pages Complètes CORRIGÉES - NiTriTe V17
Updates, Backup, Diagnostic, Optimizations avec vraies commandes
"""

import customtkinter as ctk
import tkinter as tk
import subprocess
import platform
import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from v14_mvp.design_system import DesignTokens
from v14_mvp.components import ModernCard, ModernButton, ModernStatsCard

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️ psutil non disponible - installation: pip install psutil")


class UpdatesPage(ctk.CTkFrame):
    """Page Mises à jour avec vraies commandes WinGet"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color=DesignTokens.BG_PRIMARY)
        
        self._create_header()
        self._create_terminal()
        self._create_content()
    
    def _create_header(self):
        """Header"""
        header = ModernCard(self)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        container = ctk.CTkFrame(header, fg_color="transparent")
        container.pack(fill=tk.X, padx=20, pady=15)
        
        title = ctk.CTkLabel(
            container,
            text="🔄 Mises à Jour",
            font=(DesignTokens.FONT_FAMILY, 24, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(side=tk.LEFT)
        
        # Actions
        actions = ctk.CTkFrame(container, fg_color="transparent")
        actions.pack(side=tk.RIGHT)
        
        ModernButton(
            actions,
            text="🔍 Rechercher",
            variant="filled",
            command=self._check_updates
        ).pack(side=tk.LEFT, padx=5)
        
        ModernButton(
            actions,
            text="⬇️ Tout Mettre à Jour",
            variant="outlined",
            command=self._update_all
        ).pack(side=tk.LEFT, padx=5)
    
    def _create_terminal(self):
        """Terminal intégré"""
        terminal_card = ModernCard(self)
        terminal_card.pack(fill=tk.X, padx=20, pady=10)
        
        term_title = ctk.CTkLabel(
            terminal_card,
            text="💻 Terminal",
            font=(DesignTokens.FONT_FAMILY, 16, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        term_title.pack(fill=tk.X, padx=20, pady=(15, 5))
        
        # Zone de sortie
        self.terminal_output = ctk.CTkTextbox(
            terminal_card,
            height=150,
            font=("Consolas", 10),
            fg_color="#1E1E1E",
            text_color="#D4D4D4",
            wrap="word"
        )
        self.terminal_output.pack(fill=tk.X, padx=20, pady=(0, 15))
        self.terminal_output.insert("1.0", "🔄 Terminal prêt. Cliquez sur un bouton pour exécuter une commande.\n")
        self.terminal_output.configure(state="disabled")
    
    def _log_to_terminal(self, message):
        """Ajouter message au terminal"""
        self.terminal_output.configure(state="normal")
        self.terminal_output.insert("end", f"{message}\n")
        self.terminal_output.see("end")
        self.terminal_output.configure(state="disabled")
    
    def _create_content(self):
        """Contenu"""
        # Stats
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.stats_installed = ModernStatsCard(
            stats_frame,
            "Installées",
            "...",
            "📦",
            DesignTokens.INFO
        )
        self.stats_installed.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.stats_uptodate = ModernStatsCard(
            stats_frame,
            "À jour",
            "...",
            "✅",
            DesignTokens.SUCCESS
        )
        self.stats_uptodate.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.stats_updates = ModernStatsCard(
            stats_frame,
            "Mises à jour",
            "...",
            "🔄",
            DesignTokens.WARNING
        )
        self.stats_updates.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Liste mises à jour
        card = ModernCard(self)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        header = ctk.CTkLabel(
            card,
            text="📋 Mises à jour disponibles",
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        header.pack(fill=tk.X, padx=20, pady=15)
        
        self.updates_scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        self.updates_scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Message initial
        initial_msg = ctk.CTkLabel(
            self.updates_scroll,
            text="Cliquez sur '🔍 Rechercher' pour scanner les mises à jour disponibles",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        initial_msg.pack(pady=20)
    
    def _check_updates(self):
        """Rechercher mises à jour avec WinGet"""
        self._log_to_terminal("🔍 Recherche des mises à jour...")
        
        # Clear liste
        for widget in self.updates_scroll.winfo_children():
            widget.destroy()
        
        try:
            # Commande winget upgrade --list
            result = subprocess.run(
                ["winget", "upgrade"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode == 0:
                output = result.stdout
                self._log_to_terminal(f"✅ Scan terminé\n{output[:500]}...")
                
                # Parser output (simplifié)
                lines = output.split('\n')
                updates_count = 0
                for line in lines:
                    if '→' in line or 'Available' in line:
                        updates_count += 1
                
                self.stats_updates.update_value(str(updates_count))
                self._log_to_terminal(f"📊 {updates_count} mises à jour trouvées")
                
                # Afficher message
                msg = ctk.CTkLabel(
                    self.updates_scroll,
                    text=f"✅ {updates_count} mises à jour disponibles\nUtilisez 'Tout Mettre à Jour' ou exécutez:\nwinget upgrade --all",
                    font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
                    text_color=DesignTokens.TEXT_PRIMARY
                )
                msg.pack(pady=20)
            else:
                self._log_to_terminal(f"❌ Erreur: {result.stderr}")
                
        except FileNotFoundError:
            self._log_to_terminal("❌ WinGet non trouvé. Installez depuis Microsoft Store.")
        except Exception as e:
            self._log_to_terminal(f"❌ Erreur: {e}")
    
    def _update_all(self):
        """Mettre à jour toutes les apps"""
        self._log_to_terminal("⬇️ Lancement mise à jour globale...")
        
        try:
            # Ouvrir PowerShell avec commande winget
            subprocess.Popen(
                'start powershell -Command "winget upgrade --all"',
                shell=True
            )
            self._log_to_terminal("✅ PowerShell lancé avec winget upgrade --all")
        except Exception as e:
            self._log_to_terminal(f"❌ Erreur: {e}")


class BackupPage(ctk.CTkFrame):
    """Page Sauvegarde avec vraies fonctions"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color=DesignTokens.BG_PRIMARY)
        
        self.backup_dir = Path.home() / "Documents" / "NiTriTe_Backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        self._create_header()
        self._create_content()
    
    def _create_header(self):
        """Header"""
        header = ModernCard(self)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        container = ctk.CTkFrame(header, fg_color="transparent")
        container.pack(fill=tk.X, padx=20, pady=15)
        
        title = ctk.CTkLabel(
            container,
            text="💾 Sauvegarde",
            font=(DesignTokens.FONT_FAMILY, 24, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(side=tk.LEFT)
        
        location = ctk.CTkLabel(
            container,
            text=f"📁 {self.backup_dir}",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color=DesignTokens.TEXT_SECONDARY
        )
        location.pack(side=tk.RIGHT)
    
    def _create_content(self):
        """Contenu"""
        scroll = ctk.CTkScrollableFrame(self, fg_color=DesignTokens.BG_PRIMARY)
        scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self._create_backup_section(scroll)
        self._create_restore_section(scroll)
        self._create_backups_list_section(scroll)
    
    def _create_backup_section(self, parent):
        """Section création sauvegarde"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        title = ctk.CTkLabel(
            card,
            text="📦 Créer une Sauvegarde",
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        title.pack(fill=tk.X, padx=20, pady=15)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Options
        self.backup_options = {}
        options = [
            ("apps", "💾 Liste des applications installées", True),
            ("drivers", "🔧 Liste des drivers système", True),
            ("settings", "⚙️ Paramètres NiTriTe", True),
        ]
        
        for key, text, default in options:
            var = tk.BooleanVar(value=default)
            self.backup_options[key] = var
            check = ctk.CTkCheckBox(
                content,
                text=text,
                variable=var,
                font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
                fg_color=DesignTokens.ACCENT_PRIMARY
            )
            check.pack(anchor="w", pady=5)
        
        # Bouton
        ModernButton(
            content,
            text="💾 Créer Sauvegarde",
            variant="filled",
            command=self._create_backup
        ).pack(pady=15)
    
    def _create_restore_section(self, parent):
        """Section restauration"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        title = ctk.CTkLabel(
            card,
            text="♻️ Restaurer une Sauvegarde",
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        title.pack(fill=tk.X, padx=20, pady=15)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        desc = ctk.CTkLabel(
            content,
            text="Sélectionnez une sauvegarde ci-dessous pour la restaurer",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color=DesignTokens.TEXT_SECONDARY,
            anchor="w"
        )
        desc.pack(anchor="w", pady=10)
    
    def _create_backups_list_section(self, parent):
        """Liste des sauvegardes"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        title = ctk.CTkLabel(
            card,
            text="📋 Sauvegardes Disponibles",
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        title.pack(fill=tk.X, padx=20, pady=15)
        
        self.backups_container = ctk.CTkFrame(card, fg_color="transparent")
        self.backups_container.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self._refresh_backups_list()
    
    def _refresh_backups_list(self):
        """Rafraîchir liste des sauvegardes"""
        # Clear
        for widget in self.backups_container.winfo_children():
            widget.destroy()
        
        # Lister fichiers backup
        backups = sorted(self.backup_dir.glob("backup_*.json"), reverse=True)
        
        if not backups:
            msg = ctk.CTkLabel(
                self.backups_container,
                text="Aucune sauvegarde disponible",
                font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
                text_color=DesignTokens.TEXT_SECONDARY
            )
            msg.pack(pady=10)
            return
        
        for backup_file in backups[:10]:  # Max 10
            try:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                name = backup_file.stem
                info = f"{data.get('apps_count', 0)} apps"
                size = f"{backup_file.stat().st_size / 1024:.1f} KB"
                
                self._create_backup_row(self.backups_container, name, info, size, backup_file)
            except:
                continue
    
    def _create_backup_row(self, parent, name, info, size, filepath):
        """Ligne de sauvegarde"""
        row = ctk.CTkFrame(
            parent,
            fg_color=DesignTokens.BG_ELEVATED,
            corner_radius=DesignTokens.RADIUS_MD
        )
        row.pack(fill=tk.X, pady=5)
        
        container = ctk.CTkFrame(row, fg_color="transparent")
        container.pack(fill=tk.X, padx=15, pady=12)
        
        left = ctk.CTkFrame(container, fg_color="transparent")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        name_label = ctk.CTkLabel(
            left,
            text=name,
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        info_label = ctk.CTkLabel(
            left,
            text=f"{info} • {size}",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color=DesignTokens.TEXT_TERTIARY,
            anchor="w"
        )
        info_label.pack(anchor="w")
        
        buttons = ctk.CTkFrame(container, fg_color="transparent")
        buttons.pack(side=tk.RIGHT)
        
        ModernButton(
            buttons,
            text="♻️ Restaurer",
            variant="filled",
            size="sm",
            command=lambda: self._restore_backup(filepath)
        ).pack(side=tk.LEFT, padx=3)
        
        ModernButton(
            buttons,
            text="🗑️",
            variant="text",
            size="sm",
            command=lambda: self._delete_backup(filepath)
        ).pack(side=tk.LEFT, padx=3)
    
    def _create_backup(self):
        """Créer sauvegarde"""
        print("💾 Création de la sauvegarde...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"backup_{timestamp}.json"
        
        backup_data = {
            "timestamp": timestamp,
            "date": datetime.now().isoformat(),
            "apps_count": 0,
            "apps": []
        }
        
        # Sauvegarder liste apps installées si demandé
        if self.backup_options["apps"].get():
            try:
                result = subprocess.run(
                    ["winget", "list"],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                )
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    backup_data["apps"] = [line.strip() for line in lines if line.strip()]
                    backup_data["apps_count"] = len(backup_data["apps"])
            except:
                pass
        
        # Sauvegarder
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Sauvegarde créée: {backup_file}")
            self._refresh_backups_list()
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _restore_backup(self, filepath):
        """Restaurer sauvegarde"""
        print(f"♻️ Restauration de {filepath.name}...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Backup chargé: {data.get('apps_count', 0)} apps")
            # TODO: Implémenter restauration réelle
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _delete_backup(self, filepath):
        """Supprimer sauvegarde"""
        try:
            filepath.unlink()
            print(f"🗑️ Suppression de {filepath.name}")
            self._refresh_backups_list()
        except Exception as e:
            print(f"❌ Erreur: {e}")


class DiagnosticPage(ctk.CTkFrame):
    """Page Diagnostic avec vraie détection psutil"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color=DesignTokens.BG_PRIMARY)
        
        self.system_info = self._get_system_info()
        
        self._create_header()
        self._create_content()
    
    def _get_system_info(self):
        """Obtenir vraies informations système avec détails matériels"""
        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node(),
        }
        
        # Obtenir noms exacts des composants via WMI (Windows uniquement)
        try:
            import wmi
            w = wmi.WMI()
            
            # CPU - Nom exact
            for cpu in w.Win32_Processor():
                info["cpu_name"] = cpu.Name.strip()
                info["cpu_manufacturer"] = cpu.Manufacturer
                info["cpu_cores"] = cpu.NumberOfCores
                info["cpu_threads"] = cpu.NumberOfLogicalProcessors
                info["cpu_max_speed"] = cpu.MaxClockSpeed  # MHz
                break
            
            # RAM - Modules détaillés
            info["ram_modules"] = []
            total_ram_gb = 0
            for mem in w.Win32_PhysicalMemory():
                capacity_gb = int(mem.Capacity) / (1024**3)
                total_ram_gb += capacity_gb
                info["ram_modules"].append({
                    "manufacturer": mem.Manufacturer if mem.Manufacturer else "Unknown",
                    "capacity_gb": capacity_gb,
                    "speed_mhz": mem.Speed if mem.Speed else 0,
                    "type": mem.MemoryType if mem.MemoryType else "Unknown"
                })
            info["ram_total_gb"] = total_ram_gb
            
            # Carte mère
            for board in w.Win32_BaseBoard():
                info["motherboard_manufacturer"] = board.Manufacturer
                info["motherboard_product"] = board.Product
                break
            
            # GPU - Cartes graphiques
            info["gpus"] = []
            for gpu in w.Win32_VideoController():
                info["gpus"].append({
                    "name": gpu.Name,
                    "ram_bytes": gpu.AdapterRAM if gpu.AdapterRAM else 0,
                    "driver_version": gpu.DriverVersion if gpu.DriverVersion else "N/A"
                })
            
            # Disques - Modèles exacts
            info["storage_devices"] = []
            for disk in w.Win32_DiskDrive():
                size_gb = int(disk.Size) / (1024**3) if disk.Size else 0
                info["storage_devices"].append({
                    "model": disk.Model if disk.Model else "Unknown",
                    "size_gb": size_gb,
                    "interface": disk.InterfaceType if disk.InterfaceType else "Unknown"
                })
            
        except ImportError:
            print("⚠️ Module wmi non disponible - installation: pip install wmi")
            # Fallback sans WMI
            info["cpu_name"] = platform.processor()
        except Exception as e:
            print(f"⚠️ Erreur WMI: {e}")
        
        # Données psutil (usage actuel)
        if PSUTIL_AVAILABLE:
            # CPU usage
            info["cpu_count"] = psutil.cpu_count(logical=False)
            info["cpu_threads"] = psutil.cpu_count(logical=True)
            info["cpu_percent"] = psutil.cpu_percent(interval=1)
            info["cpu_freq"] = psutil.cpu_freq()
            
            # RAM usage
            mem = psutil.virtual_memory()
            info["ram_total"] = mem.total / (1024**3)  # GB
            info["ram_used"] = mem.used / (1024**3)
            info["ram_percent"] = mem.percent
            
            # Partitions disques
            info["disks"] = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    info["disks"].append({
                        "mount": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total": usage.total / (1024**3),
                        "used": usage.used / (1024**3),
                        "percent": usage.percent
                    })
                except:
                    continue
            
            # Réseau
            net = psutil.net_io_counters()
            info["net_sent"] = net.bytes_sent / (1024**2)  # MB
            info["net_recv"] = net.bytes_recv / (1024**2)
        
        return info
    
    def _create_header(self):
        """Header"""
        header = ModernCard(self)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        container = ctk.CTkFrame(header, fg_color="transparent")
        container.pack(fill=tk.X, padx=20, pady=15)
        
        title = ctk.CTkLabel(
            container,
            text="🔍 Diagnostic",
            font=(DesignTokens.FONT_FAMILY, 24, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(side=tk.LEFT)
        
        ModernButton(
            container,
            text="🔄 Analyser",
            variant="filled",
            command=self._run_diagnostic
        ).pack(side=tk.RIGHT)
    
    def _create_content(self):
        """Contenu"""
        # Stats système
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        cpu_val = f"{self.system_info.get('cpu_percent', 0):.1f}%" if PSUTIL_AVAILABLE else "N/A"
        ModernStatsCard(
            stats_frame,
            "CPU",
            cpu_val,
            "💻",
            DesignTokens.INFO
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        if PSUTIL_AVAILABLE:
            ram_val = f"{self.system_info['ram_used']:.1f}/{self.system_info['ram_total']:.1f} GB"
        else:
            ram_val = "N/A"
        ModernStatsCard(
            stats_frame,
            "RAM",
            ram_val,
            "🧠",
            DesignTokens.SUCCESS
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        if PSUTIL_AVAILABLE and self.system_info.get('disks'):
            disk = self.system_info['disks'][0]
            disk_val = f"{disk['used']:.0f}/{disk['total']:.0f} GB"
        else:
            disk_val = "N/A"
        ModernStatsCard(
            stats_frame,
            "Disque",
            disk_val,
            "💾",
            DesignTokens.WARNING
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        net_val = "OK" if PSUTIL_AVAILABLE else "N/A"
        ModernStatsCard(
            stats_frame,
            "Réseau",
            net_val,
            "🌐",
            DesignTokens.SUCCESS
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Résultats diagnostic
        scroll = ctk.CTkScrollableFrame(self, fg_color=DesignTokens.BG_PRIMARY)
        scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sections avec vraies données
        self._create_system_section(scroll)
        self._create_hardware_section(scroll)
        self._create_storage_section(scroll)
        self._create_network_section(scroll)
    
    def _create_system_section(self, parent):
        """Section système"""
        items = [
            ("OS", f"{self.system_info['os']} {self.system_info['os_release']}", "✅"),
            ("Version", self.system_info['os_version'][:50], "✅"),
            ("Architecture", self.system_info['architecture'], "✅"),
            ("Hostname", self.system_info['hostname'], "✅"),
        ]
        
        # Carte mère si disponible
        if 'motherboard_product' in self.system_info:
            mb_info = f"{self.system_info.get('motherboard_manufacturer', 'N/A')} {self.system_info.get('motherboard_product', 'N/A')}"
            items.append(("Carte mère", mb_info, "✅"))
        
        self._create_diagnostic_section(parent, "💻 Système", items)
    
    def _create_hardware_section(self, parent):
        """Section matériel avec noms exacts"""
        items = []
        
        # CPU - Nom exact si disponible via WMI
        if 'cpu_name' in self.system_info:
            cpu_name = self.system_info['cpu_name']
            cpu_details = f"{self.system_info.get('cpu_cores', '?')} cores / {self.system_info.get('cpu_threads', '?')} threads"
            if 'cpu_max_speed' in self.system_info:
                cpu_details += f" @ {self.system_info['cpu_max_speed']} MHz"
            items.append(("Processeur", cpu_name, "✅"))
            items.append(("Configuration CPU", cpu_details, "✅"))
            
            if PSUTIL_AVAILABLE:
                items.append(("Utilisation CPU", f"{self.system_info.get('cpu_percent', 0):.1f}%", "✅"))
        else:
            # Fallback
            if PSUTIL_AVAILABLE:
                cpu_count = self.system_info.get('cpu_count', '?')
                cpu_threads = self.system_info.get('cpu_threads', '?')
                cpu_info = f"{cpu_count} cores / {cpu_threads} threads"
                items.append(("Processeur", self.system_info.get('processor', 'N/A'), "✅"))
                items.append(("Configuration", cpu_info, "✅"))
            else:
                items.append(("Processeur", self.system_info.get('processor', 'N/A'), "⚠️"))
        
        # RAM - Modules détaillés si disponibles
        if 'ram_modules' in self.system_info and self.system_info['ram_modules']:
            total_ram = self.system_info.get('ram_total_gb', 0)
            items.append(("RAM Totale", f"{total_ram:.1f} GB", "✅"))
            
            # Afficher chaque module
            for i, module in enumerate(self.system_info['ram_modules'][:4], 1):  # Max 4 modules
                module_info = f"{module['manufacturer']} {module['capacity_gb']:.0f}GB @ {module['speed_mhz']}MHz"
                items.append((f"  Module {i}", module_info, "✅"))
            
            if PSUTIL_AVAILABLE:
                ram_used = self.system_info.get('ram_used', 0)
                ram_percent = self.system_info.get('ram_percent', 0)
                ram_usage = f"{ram_used:.1f} GB utilisés ({ram_percent:.1f}%)"
                items.append(("Utilisation RAM", ram_usage, "✅"))
        else:
            # Fallback
            if PSUTIL_AVAILABLE:
                ram_total = self.system_info.get('ram_total', 0)
                ram_percent = self.system_info.get('ram_percent', 0)
                ram_info = f"{ram_total:.1f} GB ({ram_percent:.1f}% utilisés)"
                items.append(("RAM", ram_info, "✅"))
            else:
                items.append(("RAM", "psutil requis", "⚠️"))
        
        # GPU - Cartes graphiques
        if 'gpus' in self.system_info and self.system_info['gpus']:
            for i, gpu in enumerate(self.system_info['gpus'][:3], 1):  # Max 3 GPUs
                gpu_name = gpu['name']
                gpu_ram = gpu['ram_bytes'] / (1024**3) if gpu['ram_bytes'] > 0 else 0
                if gpu_ram > 0:
                    gpu_info = f"{gpu_name} ({gpu_ram:.0f} GB VRAM)"
                else:
                    gpu_info = gpu_name
                items.append((f"GPU {i}" if len(self.system_info['gpus']) > 1 else "GPU", gpu_info, "✅"))
        
        self._create_diagnostic_section(parent, "🧠 Matériel", items)
    
    def _create_storage_section(self, parent):
        """Section stockage avec modèles de disques"""
        items = []
        
        # Disques physiques avec modèles
        if 'storage_devices' in self.system_info and self.system_info['storage_devices']:
            for i, device in enumerate(self.system_info['storage_devices'], 1):
                device_info = f"{device['model']} - {device['size_gb']:.0f} GB ({device['interface']})"
                items.append((f"Disque {i}", device_info, "✅"))
        
        # Partitions avec usage
        if PSUTIL_AVAILABLE and self.system_info.get('disks'):
            if items:  # Si on a déjà des disques physiques
                items.append(("", "--- Partitions ---", ""))  # Séparateur
            for disk in self.system_info['disks']:
                try:
                    percent = float(disk.get('percent', 0))
                    status = "✅" if percent < 80 else "⚠️"
                    used = float(disk.get('used', 0))
                    total = float(disk.get('total', 0))
                    items.append((
                        f"Partition {disk['mount']}",
                        f"{used:.1f} / {total:.1f} GB ({percent:.1f}%) - {disk.get('fstype', 'N/A')}",
                        status
                    ))
                except (TypeError, ValueError, KeyError):
                    continue
        elif not items:
            items = [("Disques", "Informations non disponibles", "⚠️")]
        
        self._create_diagnostic_section(parent, "💾 Stockage", items)
    
    def _create_network_section(self, parent):
        """Section réseau"""
        if PSUTIL_AVAILABLE:
            items = [
                ("Données envoyées", f"{self.system_info['net_sent']:.1f} MB", "✅"),
                ("Données reçues", f"{self.system_info['net_recv']:.1f} MB", "✅"),
            ]
        else:
            items = [("Réseau", "psutil requis", "⚠️")]
        
        self._create_diagnostic_section(parent, "🌐 Réseau", items)
    
    def _create_diagnostic_section(self, parent, title, items):
        """Section de diagnostic"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        header = ctk.CTkLabel(
            card,
            text=title,
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        header.pack(fill=tk.X, padx=20, pady=15)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        for label, value, status in items:
            row = ctk.CTkFrame(
                content,
                fg_color=DesignTokens.BG_ELEVATED,
                corner_radius=DesignTokens.RADIUS_SM
            )
            row.pack(fill=tk.X, pady=3)
            
            row_content = ctk.CTkFrame(row, fg_color="transparent")
            row_content.pack(fill=tk.X, padx=12, pady=8)
            
            label_widget = ctk.CTkLabel(
                row_content,
                text=label,
                font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM, "bold"),
                text_color=DesignTokens.TEXT_PRIMARY,
                anchor="w",
                width=150
            )
            label_widget.pack(side=tk.LEFT)
            
            value_widget = ctk.CTkLabel(
                row_content,
                text=value,
                font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
                text_color=DesignTokens.TEXT_SECONDARY,
                anchor="w"
            )
            value_widget.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            status_widget = ctk.CTkLabel(
                row_content,
                text=status,
                font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD),
                text_color=DesignTokens.SUCCESS if status == "✅" else DesignTokens.WARNING
            )
            status_widget.pack(side=tk.RIGHT)
    
    def _run_diagnostic(self):
        """Lancer diagnostic"""
        print("🔍 Lancement du diagnostic complet...")
        # Rafraîchir infos
        self.system_info = self._get_system_info()
        # Recréer contenu
        for widget in self.winfo_children():
            widget.destroy()
        self._create_header()
        self._create_content()
        print("✅ Diagnostic terminé")


class OptimizationsPage(ctk.CTkFrame):
    """Page Optimisations avec vraies commandes"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color=DesignTokens.BG_PRIMARY)
        
        self._create_header()
        self._create_content()
    
    def _create_header(self):
        """Header"""
        header = ModernCard(self)
        header.pack(fill=tk.X, padx=20, pady=10)
        
        container = ctk.CTkFrame(header, fg_color="transparent")
        container.pack(fill=tk.X, padx=20, pady=15)
        
        title = ctk.CTkLabel(
            container,
            text="⚡ Optimisations",
            font=(DesignTokens.FONT_FAMILY, 24, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY
        )
        title.pack(side=tk.LEFT)
        
        ModernButton(
            container,
            text="🚀 Optimiser Tout",
            variant="filled",
            command=self._optimize_all
        ).pack(side=tk.RIGHT)
    
    def _create_content(self):
        """Contenu"""
        scroll = ctk.CTkScrollableFrame(self, fg_color=DesignTokens.BG_PRIMARY)
        scroll.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self._create_cleanup_section(scroll)
        self._create_performance_section(scroll)
        self._create_services_section(scroll)
        self._create_startup_section(scroll)
    
    def _create_cleanup_section(self, parent):
        """Section nettoyage"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        title = ctk.CTkLabel(
            card,
            text="🧹 Nettoyage",
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        title.pack(fill=tk.X, padx=20, pady=15)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        actions = [
            ("🗑️ Vider la corbeille", "Libérer de l'espace", self._empty_recycle_bin),
            ("🧹 Fichiers temporaires", "Supprimer fichiers temp", self._clean_temp_files),
            ("📁 Cache navigateurs", "Nettoyer cache", self._clean_browser_cache),
            ("💾 Nettoyage disque Windows", "Outil système", self._clean_system_files),
        ]
        
        for text, desc, command in actions:
            self._create_action_row(content, text, desc, command)
    
    def _create_performance_section(self, parent):
        """Section performance"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        title = ctk.CTkLabel(
            card,
            text="⚡ Performance",
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        title.pack(fill=tk.X, padx=20, pady=15)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        actions = [
            ("🔧 Optimiser disques", "Défragmentation/TRIM", self._defragment),
            ("🎯 Gestionnaire des tâches", "Ouvrir Task Manager", self._optimize_boot),
            ("💻 Nettoyeur de disque", "Outil Windows", self._clean_registry),
            ("⚙️ Options performances", "Ajuster effets visuels", self._adjust_visual_effects),
        ]
        
        for text, desc, command in actions:
            self._create_action_row(content, text, desc, command)
    
    def _create_services_section(self, parent):
        """Section services"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        title = ctk.CTkLabel(
            card,
            text="🔧 Services",
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        title.pack(fill=tk.X, padx=20, pady=15)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        desc = ctk.CTkLabel(
            content,
            text="Gérer les services Windows",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color=DesignTokens.TEXT_SECONDARY,
            anchor="w"
        )
        desc.pack(anchor="w", pady=10)
        
        ModernButton(
            content,
            text="🔧 Ouvrir Services",
            variant="outlined",
            command=self._manage_services
        ).pack(anchor="w")
    
    def _create_startup_section(self, parent):
        """Section démarrage"""
        card = ModernCard(parent)
        card.pack(fill=tk.X, pady=10)
        
        title = ctk.CTkLabel(
            card,
            text="🚀 Démarrage",
            font=(DesignTokens.FONT_FAMILY, 18, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        title.pack(fill=tk.X, padx=20, pady=15)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        desc = ctk.CTkLabel(
            content,
            text="Gérer les programmes au démarrage",
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color=DesignTokens.TEXT_SECONDARY,
            anchor="w"
        )
        desc.pack(anchor="w", pady=10)
        
        ModernButton(
            content,
            text="🚀 Gestionnaire Démarrage",
            variant="outlined",
            command=self._manage_startup
        ).pack(anchor="w")
    
    def _create_action_row(self, parent, text, description, command):
        """Ligne d'action"""
        row = ctk.CTkFrame(
            parent,
            fg_color=DesignTokens.BG_ELEVATED,
            corner_radius=DesignTokens.RADIUS_MD
        )
        row.pack(fill=tk.X, pady=5)
        
        container = ctk.CTkFrame(row, fg_color="transparent")
        container.pack(fill=tk.X, padx=15, pady=12)
        
        left = ctk.CTkFrame(container, fg_color="transparent")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        text_label = ctk.CTkLabel(
            left,
            text=text,
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_MD, "bold"),
            text_color=DesignTokens.TEXT_PRIMARY,
            anchor="w"
        )
        text_label.pack(anchor="w")
        
        desc_label = ctk.CTkLabel(
            left,
            text=description,
            font=(DesignTokens.FONT_FAMILY, DesignTokens.FONT_SIZE_SM),
            text_color=DesignTokens.TEXT_TERTIARY,
            anchor="w"
        )
        desc_label.pack(anchor="w")
        
        ModernButton(
            container,
            text="▶️ Exécuter",
            variant="filled",
            size="sm",
            command=command
        ).pack(side=tk.RIGHT)
    
    # Callbacks avec vraies commandes
    def _optimize_all(self):
        """Optimisation complète"""
        print("🚀 Optimisation complète...")
        self._empty_recycle_bin()
        self._clean_temp_files()
        print("✅ Optimisation terminée")
    
    def _empty_recycle_bin(self):
        """Vider corbeille"""
        try:
            subprocess.run('powershell -Command "Clear-RecycleBin -Force"', shell=True, check=True)
            print("✅ Corbeille vidée")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _clean_temp_files(self):
        """Nettoyer fichiers temporaires"""
        try:
            temp_dirs = [
                os.environ.get('TEMP'),
                os.environ.get('TMP'),
                os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Temp')
            ]
            
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    try:
                        for item in os.listdir(temp_dir):
                            item_path = os.path.join(temp_dir, item)
                            try:
                                if os.path.isfile(item_path):
                                    os.unlink(item_path)
                                elif os.path.isdir(item_path):
                                    shutil.rmtree(item_path)
                            except:
                                continue
                    except:
                        continue
            
            print("✅ Fichiers temporaires nettoyés")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _clean_browser_cache(self):
        """Nettoyer cache navigateurs"""
        print("📁 Ouverture gestionnaire stockage...")
        try:
            subprocess.Popen('ms-settings:storagesense', shell=True)
        except:
            print("❌ Impossible d'ouvrir les paramètres")
    
    def _clean_system_files(self):
        """Nettoyage disque Windows"""
        try:
            subprocess.Popen('cleanmgr', shell=True)
            print("✅ Nettoyage disque lancé")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _defragment(self):
        """Défragmentation"""
        try:
            subprocess.Popen('dfrgui', shell=True)
            print("✅ Défragmenteur lancé")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _optimize_boot(self):
        """Gestionnaire des tâches"""
        try:
            subprocess.Popen('taskmgr', shell=True)
            print("✅ Gestionnaire des tâches lancé")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _clean_registry(self):
        """Nettoyage disque"""
        try:
            subprocess.Popen('cleanmgr /sageset:1', shell=True)
            print("✅ Nettoyage disque configuré")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _adjust_visual_effects(self):
        """Ajuster effets visuels"""
        try:
            subprocess.Popen('SystemPropertiesPerformance.exe', shell=True)
            print("✅ Options de performances ouvertes")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _manage_services(self):
        """Gérer services"""
        try:
            subprocess.Popen('services.msc', shell=True)
            print("✅ Gestionnaire de services ouvert")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def _manage_startup(self):
        """Gérer démarrage"""
        try:
            subprocess.Popen('taskmgr /0 /startup', shell=True)
            print("✅ Gestionnaire de démarrage ouvert")
        except Exception as e:
            print(f"❌ Erreur: {e}")