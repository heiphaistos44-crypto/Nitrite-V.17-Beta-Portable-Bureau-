"""
Gestionnaire réseau avancé pour NiTriTe V13
Scanner réseau, ports, connexions actives, test de vitesse
"""

import socket
import threading
import subprocess
import logging
import time
import psutil
import requests
from typing import List, Dict, Optional, Callable
from ipaddress import ip_network, IPv4Network
from datetime import datetime
import json


class NetworkManager:
    """Gestionnaire complet pour opérations réseau avancées"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_scanning = False
        self.scan_results = []
        self.speed_test_results = {}

    def get_local_ip(self) -> str:
        """Récupère l'IP locale"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            self.logger.error(f"Erreur récupération IP locale: {e}")
            return "127.0.0.1"

    def get_network_interfaces(self) -> List[Dict]:
        """Récupère toutes les interfaces réseau"""
        interfaces = []
        try:
            addrs = psutil.net_if_addrs()
            stats = psutil.net_if_stats()

            for interface_name, addresses in addrs.items():
                interface_info = {
                    'name': interface_name,
                    'addresses': [],
                    'is_up': stats[interface_name].isup if interface_name in stats else False,
                    'speed': stats[interface_name].speed if interface_name in stats else 0
                }

                for addr in addresses:
                    if addr.family == socket.AF_INET:
                        interface_info['addresses'].append({
                            'type': 'IPv4',
                            'address': addr.address,
                            'netmask': addr.netmask,
                            'broadcast': addr.broadcast
                        })
                    elif addr.family == socket.AF_INET6:
                        interface_info['addresses'].append({
                            'type': 'IPv6',
                            'address': addr.address,
                            'netmask': addr.netmask
                        })

                interfaces.append(interface_info)

        except Exception as e:
            self.logger.error(f"Erreur interfaces réseau: {e}")

        return interfaces

    def get_active_connections(self) -> List[Dict]:
        """Récupère toutes les connexions réseau actives"""
        connections = []
        try:
            conns = psutil.net_connections(kind='inet')

            for conn in conns:
                try:
                    # Récupérer le processus associé
                    process_name = "Unknown"
                    if conn.pid:
                        try:
                            process = psutil.Process(conn.pid)
                            process_name = process.name()
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass

                    connection_info = {
                        'pid': conn.pid,
                        'process': process_name,
                        'family': 'IPv4' if conn.family == socket.AF_INET else 'IPv6',
                        'type': 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP',
                        'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "",
                        'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "",
                        'status': conn.status
                    }

                    connections.append(connection_info)

                except Exception as e:
                    self.logger.debug(f"Erreur traitement connexion: {e}")
                    continue

        except Exception as e:
            self.logger.error(f"Erreur récupération connexions: {e}")

        return connections

    def scan_network(self, network: Optional[str] = None, timeout: float = 0.5,
                     progress_callback: Optional[Callable] = None) -> List[Dict]:
        """
        Scanne le réseau local pour découvrir les appareils

        Args:
            network: Réseau à scanner (ex: "192.168.1.0/24"), auto-détecté si None
            timeout: Timeout par host (secondes)
            progress_callback: Fonction appelée avec (current, total, host)

        Returns:
            Liste des appareils découverts
        """
        if self.is_scanning:
            self.logger.warning("Un scan est déjà en cours")
            return []

        self.is_scanning = True
        self.scan_results = []

        try:
            # Déterminer le réseau à scanner
            if network is None:
                local_ip = self.get_local_ip()
                # Calculer le réseau (assume /24)
                network = ".".join(local_ip.split(".")[:3]) + ".0/24"

            self.logger.info(f"Scan réseau {network} démarré")

            # Créer le réseau
            net = ip_network(network, strict=False)
            hosts = list(net.hosts())
            total_hosts = len(hosts)

            # Scanner chaque host
            threads = []
            for i, host in enumerate(hosts):
                if not self.is_scanning:
                    break

                thread = threading.Thread(
                    target=self._scan_host,
                    args=(str(host), timeout),
                    daemon=True
                )
                thread.start()
                threads.append(thread)

                # Callback de progression
                if progress_callback:
                    progress_callback(i + 1, total_hosts, str(host))

                # Limiter threads concurrents
                if len(threads) >= 50:
                    for t in threads:
                        t.join()
                    threads = []

            # Attendre les threads restants
            for thread in threads:
                thread.join()

            self.logger.info(f"Scan terminé: {len(self.scan_results)} appareils trouvés")

        except Exception as e:
            self.logger.error(f"Erreur scan réseau: {e}")
        finally:
            self.is_scanning = False

        return self.scan_results

    def _scan_host(self, host: str, timeout: float):
        """Scanne un host individuel"""
        try:
            # Ping test (TCP connect sur port commun)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            # Essayer port 445 (SMB - commun sur Windows)
            result = sock.connect_ex((host, 445))

            if result == 0:
                # Host actif
                try:
                    hostname = socket.gethostbyaddr(host)[0]
                except socket.herror:
                    hostname = "Unknown"

                device_info = {
                    'ip': host,
                    'hostname': hostname,
                    'mac': self._get_mac_address(host),
                    'open_ports': [],
                    'timestamp': datetime.now()
                }

                self.scan_results.append(device_info)

            sock.close()

        except Exception as e:
            self.logger.debug(f"Host {host} non accessible: {e}")

    def _get_mac_address(self, ip: str) -> str:
        """Récupère l'adresse MAC via ARP (Windows)"""
        try:
            result = subprocess.run(
                ['arp', '-a', ip],
                capture_output=True,
                text=True,
                timeout=2
            )

            # Parser la sortie ARP
            for line in result.stdout.split('\n'):
                if ip in line:
                    parts = line.split()
                    for part in parts:
                        if '-' in part and len(part) == 17:  # Format MAC xx-xx-xx-xx-xx-xx
                            return part.replace('-', ':')

        except Exception as e:
            self.logger.debug(f"Erreur récupération MAC pour {ip}: {e}")

        return "Unknown"

    def scan_ports(self, host: str, ports: Optional[List[int]] = None,
                   timeout: float = 0.5, progress_callback: Optional[Callable] = None) -> List[Dict]:
        """
        Scanne les ports d'un host

        Args:
            host: IP ou hostname à scanner
            ports: Liste de ports (utilise ports communs si None)
            timeout: Timeout par port
            progress_callback: Fonction appelée avec (current, total, port)

        Returns:
            Liste des ports ouverts avec infos
        """
        # Ports communs par défaut
        if ports is None:
            ports = [
                21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995,
                1723, 3306, 3389, 5900, 8080, 8443
            ]

        open_ports = []
        total_ports = len(ports)

        self.logger.info(f"Scan de {total_ports} ports sur {host}")

        for i, port in enumerate(ports):
            if progress_callback:
                progress_callback(i + 1, total_ports, port)

            result = self._check_port(host, port, timeout)
            if result:
                open_ports.append(result)

        self.logger.info(f"Scan terminé: {len(open_ports)} ports ouverts")
        return open_ports

    def _check_port(self, host: str, port: int, timeout: float) -> Optional[Dict]:
        """Vérifie si un port est ouvert"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()

            if result == 0:
                # Port ouvert
                service = self._get_service_name(port)
                return {
                    'port': port,
                    'state': 'open',
                    'service': service,
                    'protocol': 'tcp'
                }

        except Exception as e:
            self.logger.debug(f"Erreur scan port {port}: {e}")

        return None

    def _get_service_name(self, port: int) -> str:
        """Retourne le nom du service pour un port donné"""
        services = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            111: 'RPC',
            135: 'MS-RPC',
            139: 'NetBIOS',
            143: 'IMAP',
            443: 'HTTPS',
            445: 'SMB',
            993: 'IMAPS',
            995: 'POP3S',
            1723: 'PPTP',
            3306: 'MySQL',
            3389: 'RDP',
            5900: 'VNC',
            8080: 'HTTP-Proxy',
            8443: 'HTTPS-Alt'
        }
        return services.get(port, 'Unknown')

    def test_internet_speed(self, progress_callback: Optional[Callable] = None) -> Dict:
        """
        Test de vitesse Internet (download/upload)

        Args:
            progress_callback: Fonction appelée avec (step, message)

        Returns:
            Résultats du test {download_mbps, upload_mbps, ping_ms, server}
        """
        results = {
            'download_mbps': 0,
            'upload_mbps': 0,
            'ping_ms': 0,
            'server': '',
            'timestamp': datetime.now(),
            'success': False
        }

        try:
            # 1. Test de ping
            if progress_callback:
                progress_callback('ping', 'Test de latence...')

            ping_ms = self._test_ping('8.8.8.8')
            results['ping_ms'] = ping_ms

            # 2. Test download
            if progress_callback:
                progress_callback('download', 'Test de téléchargement...')

            download_mbps = self._test_download()
            results['download_mbps'] = download_mbps

            # 3. Test upload
            if progress_callback:
                progress_callback('upload', 'Test d\'envoi...')

            upload_mbps = self._test_upload()
            results['upload_mbps'] = upload_mbps

            results['server'] = 'Google/Cloudflare'
            results['success'] = True

            self.logger.info(f"Test vitesse: ↓{download_mbps:.2f} Mbps ↑{upload_mbps:.2f} Mbps")

        except Exception as e:
            self.logger.error(f"Erreur test vitesse: {e}")
            results['error'] = str(e)

        self.speed_test_results = results
        return results

    def _test_ping(self, host: str = '8.8.8.8', count: int = 4) -> float:
        """Test de ping (latence)"""
        try:
            result = subprocess.run(
                ['ping', '-n', str(count), host],
                capture_output=True,
                text=True,
                timeout=10
            )

            # Parser la sortie pour extraire le temps moyen
            for line in result.stdout.split('\n'):
                if 'Average' in line or 'Moyenne' in line:
                    # Format: "Average = XXms" ou "Moyenne = XXms"
                    parts = line.split('=')
                    if len(parts) > 1:
                        time_str = parts[-1].strip().replace('ms', '')
                        return float(time_str)

        except Exception as e:
            self.logger.error(f"Erreur test ping: {e}")

        return 0

    def _test_download(self, size_mb: int = 10) -> float:
        """Test de vitesse download"""
        try:
            # URL de test (fichier de taille connue)
            # Utiliser un CDN rapide
            test_urls = [
                f'http://speedtest.ftp.otenet.gr/files/test{size_mb}Mb.db',
                'http://ipv4.download.thinkbroadband.com/10MB.zip',
            ]

            start_time = time.time()
            downloaded = 0

            for url in test_urls:
                try:
                    response = requests.get(url, timeout=15, stream=True)
                    if response.status_code == 200:
                        for chunk in response.iter_content(chunk_size=8192):
                            downloaded += len(chunk)

                        # Calculer vitesse
                        duration = time.time() - start_time
                        if duration > 0:
                            mbps = (downloaded * 8) / (duration * 1_000_000)
                            return round(mbps, 2)

                except requests.RequestException:
                    continue

        except Exception as e:
            self.logger.error(f"Erreur test download: {e}")

        return 0

    def _test_upload(self, size_kb: int = 1024) -> float:
        """Test de vitesse upload"""
        try:
            # Générer données de test
            data = b'0' * (size_kb * 1024)

            # URLs de test upload
            test_url = 'http://httpbin.org/post'

            start_time = time.time()
            response = requests.post(test_url, data=data, timeout=15)

            if response.status_code == 200:
                duration = time.time() - start_time
                if duration > 0:
                    mbps = (len(data) * 8) / (duration * 1_000_000)
                    return round(mbps, 2)

        except Exception as e:
            self.logger.error(f"Erreur test upload: {e}")

        return 0

    def get_public_ip(self) -> Dict:
        """Récupère l'IP publique et informations géographiques"""
        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            self.logger.error(f"Erreur récupération IP publique: {e}")

        return {'ip': 'Unknown'}

    def get_dns_servers(self) -> List[str]:
        """Récupère les serveurs DNS configurés"""
        dns_servers = []

        try:
            # Windows: utiliser ipconfig /all
            result = subprocess.run(
                ['ipconfig', '/all'],
                capture_output=True,
                text=True,
                timeout=5
            )

            in_dns_section = False
            for line in result.stdout.split('\n'):
                if 'DNS Servers' in line or 'Serveurs DNS' in line:
                    in_dns_section = True
                    # Extraire l'IP sur la même ligne
                    parts = line.split(':')
                    if len(parts) > 1:
                        ip = parts[1].strip()
                        if ip and ip[0].isdigit():
                            dns_servers.append(ip)

                elif in_dns_section:
                    # Continuer à lire les IPs suivantes
                    line = line.strip()
                    if line and line[0].isdigit():
                        dns_servers.append(line)
                    elif line and not line[0].isdigit():
                        in_dns_section = False

        except Exception as e:
            self.logger.error(f"Erreur récupération DNS: {e}")

        return dns_servers

    def traceroute(self, host: str, max_hops: int = 30) -> List[Dict]:
        """Effectue un traceroute vers un host"""
        hops = []

        try:
            result = subprocess.run(
                ['tracert', '-h', str(max_hops), host],
                capture_output=True,
                text=True,
                timeout=60
            )

            hop_num = 0
            for line in result.stdout.split('\n'):
                if line.strip() and line.strip()[0].isdigit():
                    hop_num += 1
                    # Parser la ligne traceroute
                    parts = line.split()
                    if len(parts) >= 2:
                        hop_info = {
                            'hop': hop_num,
                            'ip': '',
                            'hostname': '',
                            'rtt_ms': []
                        }

                        # Extraire IP et hostname
                        for part in parts:
                            if '[' in part and ']' in part:
                                hop_info['ip'] = part.strip('[]')
                            elif '.' in part and part.replace('.', '').isdigit():
                                hop_info['ip'] = part

                        hops.append(hop_info)

        except Exception as e:
            self.logger.error(f"Erreur traceroute: {e}")

        return hops

    def stop_scan(self):
        """Arrête le scan en cours"""
        self.is_scanning = False


# Test du module
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    manager = NetworkManager()

    print("=== Informations Réseau ===")
    print(f"IP locale: {manager.get_local_ip()}")
    print(f"\nIP publique: {manager.get_public_ip().get('ip')}")

    print(f"\nServeurs DNS: {', '.join(manager.get_dns_servers())}")

    print("\n=== Interfaces Réseau ===")
    for iface in manager.get_network_interfaces():
        if iface['is_up']:
            print(f"{iface['name']}: {iface['addresses']}")

    print("\n=== Connexions Actives ===")
    connections = manager.get_active_connections()
    for conn in connections[:10]:
        print(f"{conn['process']:<20} {conn['type']} {conn['local_addr']} -> {conn['remote_addr']} [{conn['status']}]")

    print(f"\nTotal connexions: {len(connections)}")
