"""
Module de surveillance système en temps réel pour NiTriTe V13
Surveillance CPU, RAM, Disque, Température, Processus
"""

import psutil
import threading
import time
import logging
from datetime import datetime
from typing import Dict, List, Callable, Optional
import platform

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False
    logging.warning("WMI non disponible - températures désactivées")


class SystemMonitor:
    """Gestionnaire de surveillance système en temps réel"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_monitoring = False
        self.monitor_thread = None
        self.callbacks = []
        self.update_interval = 1.0  # Secondes entre chaque mise à jour

        # Données de surveillance
        self.current_data = {
            'cpu': {'percent': 0, 'per_core': [], 'freq': 0},
            'memory': {'percent': 0, 'used': 0, 'total': 0, 'available': 0},
            'disk': {},
            'network': {'bytes_sent': 0, 'bytes_recv': 0, 'speed_up': 0, 'speed_down': 0},
            'temperature': {},
            'battery': None,
            'processes': []
        }

        # Historique pour calculs
        self.last_net_io = None
        self.last_update_time = None

        # Initialiser WMI si disponible
        self.wmi_conn = None
        if WMI_AVAILABLE:
            try:
                self.wmi_conn = wmi.WMI(namespace="root\\OpenHardwareMonitor")
            except Exception as e:
                self.logger.warning(f"OpenHardwareMonitor non détecté: {e}")
                try:
                    self.wmi_conn = wmi.WMI(namespace="root\\wmi")
                except Exception as e:
                    self.logger.warning(f"WMI sensors non disponibles: {e}")

        # Seuils d'alerte
        self.thresholds = {
            'cpu': 80,  # %
            'memory': 85,  # %
            'disk': 90,  # %
            'temperature': 80  # °C
        }

        self.alerts = []

    def start_monitoring(self, callback: Optional[Callable] = None, interval: float = 1.0):
        """Démarre la surveillance en temps réel"""
        if self.is_monitoring:
            self.logger.warning("Surveillance déjà active")
            return

        self.update_interval = interval
        if callback:
            self.add_callback(callback)

        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Surveillance système démarrée")

    def stop_monitoring(self):
        """Arrête la surveillance"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        self.logger.info("Surveillance système arrêtée")

    def add_callback(self, callback: Callable):
        """Ajoute une fonction callback appelée à chaque mise à jour"""
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def remove_callback(self, callback: Callable):
        """Retire une fonction callback"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def _monitor_loop(self):
        """Boucle principale de surveillance"""
        while self.is_monitoring:
            try:
                self._update_data()
                self._check_alerts()

                # Appeler tous les callbacks
                for callback in self.callbacks:
                    try:
                        callback(self.current_data)
                    except Exception as e:
                        self.logger.error(f"Erreur callback: {e}")

                time.sleep(self.update_interval)
            except Exception as e:
                self.logger.error(f"Erreur boucle surveillance: {e}")

    def _update_data(self):
        """Met à jour toutes les données système"""
        current_time = time.time()

        # CPU
        self.current_data['cpu'] = self._get_cpu_info()

        # Mémoire
        self.current_data['memory'] = self._get_memory_info()

        # Disques
        self.current_data['disk'] = self._get_disk_info()

        # Réseau (avec calcul de vitesse)
        self.current_data['network'] = self._get_network_info(current_time)

        # Température
        self.current_data['temperature'] = self._get_temperature_info()

        # Batterie
        self.current_data['battery'] = self._get_battery_info()

        # Top processus
        self.current_data['processes'] = self._get_top_processes(limit=10)

        self.last_update_time = current_time

    def _get_cpu_info(self) -> Dict:
        """Récupère les infos CPU"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
            cpu_freq = psutil.cpu_freq()

            return {
                'percent': cpu_percent,
                'per_core': cpu_per_core,
                'freq': cpu_freq.current if cpu_freq else 0,
                'freq_max': cpu_freq.max if cpu_freq else 0,
                'cores_physical': psutil.cpu_count(logical=False),
                'cores_logical': psutil.cpu_count(logical=True)
            }
        except Exception as e:
            self.logger.error(f"Erreur CPU: {e}")
            return {'percent': 0, 'per_core': [], 'freq': 0}

    def _get_memory_info(self) -> Dict:
        """Récupère les infos mémoire"""
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            return {
                'percent': mem.percent,
                'used': mem.used,
                'total': mem.total,
                'available': mem.available,
                'used_gb': round(mem.used / (1024**3), 2),
                'total_gb': round(mem.total / (1024**3), 2),
                'swap_percent': swap.percent,
                'swap_used_gb': round(swap.used / (1024**3), 2),
                'swap_total_gb': round(swap.total / (1024**3), 2)
            }
        except Exception as e:
            self.logger.error(f"Erreur mémoire: {e}")
            return {'percent': 0, 'used': 0, 'total': 0, 'available': 0}

    def _get_disk_info(self) -> Dict:
        """Récupère les infos disques"""
        disk_info = {}
        try:
            partitions = psutil.disk_partitions()
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info[partition.device] = {
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'percent': usage.percent,
                        'used': usage.used,
                        'total': usage.total,
                        'free': usage.free,
                        'used_gb': round(usage.used / (1024**3), 2),
                        'total_gb': round(usage.total / (1024**3), 2),
                        'free_gb': round(usage.free / (1024**3), 2)
                    }
                except (PermissionError, OSError):
                    continue
        except Exception as e:
            self.logger.error(f"Erreur disques: {e}")

        return disk_info

    def _get_network_info(self, current_time: float) -> Dict:
        """Récupère les infos réseau avec calcul de vitesse"""
        try:
            net_io = psutil.net_io_counters()

            network_data = {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'bytes_sent_mb': round(net_io.bytes_sent / (1024**2), 2),
                'bytes_recv_mb': round(net_io.bytes_recv / (1024**2), 2),
                'speed_up': 0,
                'speed_down': 0,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv
            }

            # Calculer vitesse si on a des données précédentes
            if self.last_net_io and self.last_update_time:
                time_delta = current_time - self.last_update_time
                if time_delta > 0:
                    sent_delta = net_io.bytes_sent - self.last_net_io.bytes_sent
                    recv_delta = net_io.bytes_recv - self.last_net_io.bytes_recv

                    # Vitesse en KB/s
                    network_data['speed_up'] = round((sent_delta / time_delta) / 1024, 2)
                    network_data['speed_down'] = round((recv_delta / time_delta) / 1024, 2)

            self.last_net_io = net_io
            return network_data
        except Exception as e:
            self.logger.error(f"Erreur réseau: {e}")
            return {'bytes_sent': 0, 'bytes_recv': 0, 'speed_up': 0, 'speed_down': 0}

    def _get_temperature_info(self) -> Dict:
        """Récupère les températures (nécessite WMI/OpenHardwareMonitor)"""
        temps = {}

        try:
            if hasattr(psutil, "sensors_temperatures"):
                sensors = psutil.sensors_temperatures()
                if sensors:
                    for name, entries in sensors.items():
                        for entry in entries:
                            temps[f"{name}_{entry.label}"] = {
                                'current': entry.current,
                                'high': entry.high if entry.high else 0,
                                'critical': entry.critical if entry.critical else 0
                            }
        except Exception as e:
            self.logger.debug(f"psutil sensors non disponibles: {e}")

        # Essayer avec WMI si disponible
        if self.wmi_conn:
            try:
                sensors = self.wmi_conn.Sensor()
                for sensor in sensors:
                    if sensor.SensorType == 'Temperature':
                        temps[sensor.Name] = {
                            'current': float(sensor.Value),
                            'high': 0,
                            'critical': 0
                        }
            except Exception as e:
                self.logger.debug(f"WMI sensors erreur: {e}")

        return temps

    def _get_battery_info(self) -> Optional[Dict]:
        """Récupère les infos batterie (pour portables)"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    'percent': battery.percent,
                    'plugged': battery.power_plugged,
                    'time_left': battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else -1
                }
        except Exception as e:
            self.logger.debug(f"Batterie non disponible: {e}")

        return None

    def _get_top_processes(self, limit: int = 10) -> List[Dict]:
        """Récupère les processus les plus gourmands"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    pinfo = proc.info
                    processes.append({
                        'pid': pinfo['pid'],
                        'name': pinfo['name'],
                        'cpu': pinfo['cpu_percent'] or 0,
                        'memory': pinfo['memory_percent'] or 0,
                        'status': pinfo['status']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Trier par CPU décroissant
            processes.sort(key=lambda x: x['cpu'], reverse=True)
            return processes[:limit]
        except Exception as e:
            self.logger.error(f"Erreur processus: {e}")
            return []

    def _check_alerts(self):
        """Vérifie les seuils et génère des alertes"""
        new_alerts = []

        # Alerte CPU
        if self.current_data['cpu']['percent'] > self.thresholds['cpu']:
            new_alerts.append({
                'type': 'cpu',
                'level': 'warning',
                'message': f"CPU élevé: {self.current_data['cpu']['percent']:.1f}%",
                'timestamp': datetime.now()
            })

        # Alerte mémoire
        if self.current_data['memory']['percent'] > self.thresholds['memory']:
            new_alerts.append({
                'type': 'memory',
                'level': 'warning',
                'message': f"Mémoire élevée: {self.current_data['memory']['percent']:.1f}%",
                'timestamp': datetime.now()
            })

        # Alerte disques
        for device, info in self.current_data['disk'].items():
            if info['percent'] > self.thresholds['disk']:
                new_alerts.append({
                    'type': 'disk',
                    'level': 'critical',
                    'message': f"Disque {device} plein: {info['percent']:.1f}%",
                    'timestamp': datetime.now()
                })

        # Alerte température
        for sensor, temp in self.current_data['temperature'].items():
            if temp['current'] > self.thresholds['temperature']:
                new_alerts.append({
                    'type': 'temperature',
                    'level': 'critical',
                    'message': f"Température {sensor}: {temp['current']:.1f}°C",
                    'timestamp': datetime.now()
                })

        # Ajouter nouvelles alertes
        self.alerts.extend(new_alerts)

        # Garder seulement les 50 dernières alertes
        if len(self.alerts) > 50:
            self.alerts = self.alerts[-50:]

    def get_system_info(self) -> Dict:
        """Récupère les informations système statiques"""
        try:
            uname = platform.uname()
            boot_time = datetime.fromtimestamp(psutil.boot_time())

            return {
                'system': uname.system,
                'node': uname.node,
                'release': uname.release,
                'version': uname.version,
                'machine': uname.machine,
                'processor': uname.processor,
                'boot_time': boot_time.strftime("%Y-%m-%d %H:%M:%S"),
                'uptime_hours': round((datetime.now() - boot_time).total_seconds() / 3600, 2)
            }
        except Exception as e:
            self.logger.error(f"Erreur infos système: {e}")
            return {}

    def get_current_data(self) -> Dict:
        """Retourne les données actuelles de surveillance"""
        return self.current_data

    def get_alerts(self, clear: bool = False) -> List[Dict]:
        """Retourne les alertes, optionnellement les efface"""
        alerts = self.alerts.copy()
        if clear:
            self.alerts.clear()
        return alerts

    def set_threshold(self, metric: str, value: float):
        """Définit un seuil d'alerte"""
        if metric in self.thresholds:
            self.thresholds[metric] = value
            self.logger.info(f"Seuil {metric} défini à {value}")

    def get_thresholds(self) -> Dict:
        """Retourne les seuils d'alerte actuels"""
        return self.thresholds.copy()


# Fonction utilitaire pour formater la taille
def format_bytes(bytes_value: int) -> str:
    """Formate les octets en unité lisible"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


# Test du module
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    def print_data(data):
        print(f"\n{'='*60}")
        print(f"CPU: {data['cpu']['percent']:.1f}% | RAM: {data['memory']['percent']:.1f}%")
        print(f"Réseau ↑ {data['network']['speed_up']:.1f} KB/s | ↓ {data['network']['speed_down']:.1f} KB/s")

        if data['temperature']:
            temps = [f"{name}: {info['current']:.1f}°C" for name, info in list(data['temperature'].items())[:3]]
            print(f"Temp: {' | '.join(temps)}")

    monitor = SystemMonitor()
    monitor.start_monitoring(callback=print_data, interval=2.0)

    try:
        time.sleep(30)
    except KeyboardInterrupt:
        pass
    finally:
        monitor.stop_monitoring()
