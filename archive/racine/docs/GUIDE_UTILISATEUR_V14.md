# Guide Utilisateur - NiTriTe V14.0 MVP

## 🚀 Bienvenue dans NiTriTe V14

NiTriTe V14 est une application professionnelle de maintenance informatique avec interface moderne Material Design 3.

---

## 📋 Table des Matières

1. [Installation](#installation)
2. [Lancement](#lancement)
3. [Interface](#interface)
4. [Pages](#pages)
5. [Fonctionnalités](#fonctionnalites)
6. [Paramètres](#parametres)
7. [Dépannage](#depannage)

---

## 🔧 Installation

### Prérequis

- **Windows 10/11** (64-bit)
- **Python 3.12** (requis pour CustomTkinter 5.2.2)
- **WinGet** (optionnel, pour installations automatiques)

### Télécharger Python 3.12

1. Aller sur https://www.python.org/downloads/
2. Télécharger Python 3.12.x
3. **IMPORTANT**: Cocher "Add Python to PATH" lors de l'installation

### Installer les Dépendances

```bash
pip install customtkinter
```

---

## 🚀 Lancement

### Méthode 1: Lancer avec BAT (Recommandé)

Double-cliquez sur **`LANCER_V14_MVP.bat`**

### Méthode 2: Ligne de commande

```bash
cd "c:\Users\Momo\Documents\GitHub\Nitrite V.13 Beta"
python -m src.v14_mvp.main_app
```

---

## 🖥️ Interface

### Layout Principal

```
┌─────────────────────────────────────────────────────────┐
│  NiTriTe V14.0 MVP                                  ⚙️ │
├───────┬─────────────────────────────────────────────────┤
│ 📦    │                                                 │
│ Apps  │           Contenu Principal                     │
│       │                                                 │
│ 🛠️    │                                                 │
│ Tools │                                                 │
│       │                                                 │
│ 🚀    │                                                 │
│Master │                                                 │
│       │                                                 │
│ 🔄    │                                                 │
│Update │                                                 │
└───────┴─────────────────────────────────────────────────┘
```

### Navigation Sidebar

La barre de navigation à gauche permet d'accéder aux 8 pages principales:

- **📦 Applications** - Catalogue de 700+ applications
- **🛠️ Outils** - 500+ outils système
- **🚀 Master Install** - Packs d'applications
- **🔄 Mises à jour** - Gestionnaire de mises à jour
- **💾 Sauvegarde** - Backup/Restore
- **⚡ Optimisations** - Nettoyage et performance
- **🔍 Diagnostic** - Analyse système
- **⚙️ Paramètres** - Configuration

---

## 📄 Pages

### 1. 📦 Page Applications

**Fonctionnalités:**
- Affichage de 20 applications par catégorie (performance)
- Grille 3 colonnes responsive
- Recherche en temps réel
- Sélection multiple avec checkboxes
- Badge ⭐ pour applications essentielles
- Catégories groupées avec headers

**Catégories Spéciales (non limitées):**
- Désinstallateurs
- Antivirus
- Outils OrdiPlus

**Utilisation:**
1. Parcourir les catégories
2. Cocher les applications désirées
3. Cliquer "🚀 Installer Sélection"
4. Une fenêtre d'installation s'ouvre avec progression

**Stats Affichées:**
- Total: 716 applications disponibles
- Affichées: Nombre actuellement visible
- Sélection: Nombre d'apps cochées

---

### 2. 🛠️ Page Outils

**Fonctionnalités:**
- 548 outils système organisés
- Sections repliables (cliquer header pour ouvrir/fermer)
- Max 20 outils affichés par section (performance)
- Exécution directe des commandes

**Sections (12):**
- Réseau
- Système
- Disques
- Sécurité
- Performance
- Registre
- Services
- Tâches
- Utilisateurs
- Dépannage
- Maintenance
- Avancé

**Utilisation:**
1. Cliquer sur nom de section pour déplier
2. Cliquer sur bouton outil pour exécuter
3. Recliquer section pour refermer

---

### 3. 🚀 Page Master Install

**Fonctionnalités:**
- 10 packs d'applications prédéfinis
- Grille 2 colonnes
- Installation de pack complet en un clic
- Sélection multiple de packs

**Packs Disponibles:**

1. **🎮 Gaming** (5 apps)
   - Steam, Epic Games, Discord, OBS Studio, GeForce Experience

2. **💼 Bureau** (5 apps)
   - Microsoft Office, Adobe Reader, 7-Zip, Notepad++, TeamViewer

3. **💻 Développeur** (6 apps)
   - VS Code, Git, Python, Node.js, Docker, Postman

4. **🎨 Creative** (5 apps)
   - GIMP, Inkscape, Blender, Audacity, OBS Studio

5. **🌐 Navigateurs** (5 apps)
   - Chrome, Firefox, Edge, Brave, Opera

6. **📺 Multimédia** (5 apps)
   - VLC, Spotify, iTunes, HandBrake, K-Lite Codec Pack

7. **🔧 Utilitaires** (5 apps)
   - CCleaner, WinRAR, Process Explorer, TreeSize, Everything

8. **💬 Communication** (5 apps)
   - Discord, Slack, Zoom, Microsoft Teams, Skype

9. **🎓 Étudiant** (5 apps)
   - LibreOffice, Notion, Obsidian, Anki, Zotero

10. **🏠 Usage Personnel** (5 apps)
    - Chrome, VLC, 7-Zip, Adobe Reader, Spotify

**Utilisation:**
- Cocher packs désirés + cliquer "🚀 Installer Sélection"
- OU cliquer "🚀 Installer" sur un pack individuel

---

### 4. 🔄 Page Mises à Jour

**Fonctionnalités:**
- Détection automatique des mises à jour disponibles
- Affichage version actuelle → nouvelle version
- Taille de téléchargement affichée
- Mise à jour individuelle ou globale

**Stats:**
- Installées: Total d'applications installées
- À jour: Applications avec dernière version
- Mises à jour: Nombre de mises à jour disponibles

**Utilisation:**
1. Cliquer "🔍 Rechercher" pour scanner
2. Sélectionner apps à mettre à jour
3. Cliquer "⬇️ Mettre à jour" (individuel) ou "⬇️ Tout Mettre à Jour"

---

### 5. 💾 Page Sauvegarde

**3 Sections:**

#### A. Créer Sauvegarde
Options disponibles:
- ☑ Liste des applications installées
- ☑ Drivers système
- ☐ Paramètres Windows
- ☐ Clés de registre
- ☐ Documents utilisateur

**Utilisation:**
1. Cocher éléments à sauvegarder
2. Cliquer "💾 Créer Sauvegarde"
3. Fichier créé dans `/backups/`

#### B. Restaurer
Instructions pour restaurer une sauvegarde existante

#### C. Sauvegardes Disponibles
Liste des sauvegardes avec:
- Nom (date/heure)
- Contenu (X apps • Y drivers)
- Taille
- Actions: ♻️ Restaurer | 🗑️ Supprimer

---

### 6. ⚡ Page Optimisations

**4 Sections:**

#### A. 🧹 Nettoyage
- Vider la corbeille (gain d'espace affiché)
- Fichiers temporaires
- Cache navigateurs
- Fichiers système inutiles

#### B. ⚡ Performance
- Défragmenter disques
- Optimiser démarrage
- Nettoyer registre
- Ajuster effets visuels

#### C. 🔧 Services
Désactiver services inutiles

#### D. 🚀 Démarrage
Gérer les 24 programmes au démarrage

**Utilisation:**
- Cliquer "🚀 Optimiser Tout" pour tout optimiser
- OU cliquer "▶️ Exécuter" sur action individuelle

---

### 7. 🔍 Page Diagnostic

**Fonctionnalités:**
- Stats système en temps réel
- 4 sections détaillées
- Statut ✅/⚠️ pour chaque élément

**Stats Affichées:**
- 💻 CPU: Utilisation en %
- 🧠 RAM: Utilisé / Total
- 💾 Disque: Utilisé / Total
- 🌐 Réseau: État connexion

**Sections Diagnostiquées:**

1. **💻 Système**
   - OS, Version Build, Architecture

2. **🧠 Matériel**
   - CPU, RAM, GPU

3. **💾 Stockage**
   - Espace disque, Santé SSD, Fragmentation

4. **🌐 Réseau**
   - Connexion, Latence, DNS

**Utilisation:**
Cliquer "🔄 Analyser" pour lancer diagnostic complet

---

### 8. ⚙️ Page Paramètres

**10 Sections de Configuration:**

#### 1. 🎨 Apparence
- **Thème**: Orange NiTriTe, Bleu Pro, Vert Tech, Violet Creative, Rouge Energy
- **Mode**: Sombre / Clair / Auto
- **Taille police**: 12-20px (slider)

#### 2. 🌍 Langue
- 🇫🇷 Français
- 🇬🇧 English

#### 3. 🔄 Mises à jour
- Vérification automatique (toggle)
- Canal: Stable / Beta

#### 4. ⚡ Performances
- Limite apps/catégorie: 10-50 (slider, défaut 20)
- Animations (toggle)

#### 5. 📦 Installation
- Gestionnaire: WinGet / Chocolatey / Téléchargement Direct
- Dossier téléchargement

#### 6. 💾 Sauvegarde
- Sauvegarde automatique (toggle)

#### 7. 🔔 Notifications
- Notifications système (toggle)
- Sons (toggle)

#### 8. 🔧 Avancé
- Mode Debug (toggle)
- Mode Portable (toggle)

#### 9. ℹ️ À propos
- Informations version
- Stats application
- Copyright

#### 10. 🚀 Actions
- 💾 Sauvegarder Configuration
- 🔄 Réinitialiser
- 📂 Ouvrir Dossier Config

---

## 🎯 Fonctionnalités

### Installation d'Applications

**3 Méthodes Supportées:**

#### 1. WinGet (Recommandé)
- Installation silencieuse
- Gestion des dépendances
- Mises à jour automatiques

**Vérifier WinGet:**
```cmd
winget --version
```

#### 2. Chocolatey
- Alternative à WinGet
- Large catalogue

**Installer Chocolatey:**
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

#### 3. Téléchargement Direct
- Télécharge le fichier d'installation
- Lance l'installeur
- Fichiers dans `/downloads/`

### Fenêtre d'Installation

Quand vous installez des apps, une fenêtre popup s'affiche avec:
- Titre: "📦 Installation de X applications"
- Barre de progression
- Log en temps réel
- Messages de succès/erreur
- Bouton "Fermer" à la fin

---

## 🎨 Thèmes et Couleurs

### Thème Orange NiTriTe (Défaut)

**Palette:**
- Accent: `#FF8C00` (Orange vif)
- Fond Principal: `#0D0D0D` (Noir profond)
- Fond Élevé: `#1A1A1A` (Gris très foncé)
- Fond Secondaire: `#262626` (Gris foncé)
- Texte Principal: `#FFFFFF` (Blanc)
- Texte Secondaire: `#B3B3B3` (Gris clair)
- Texte Tertiaire: `#808080` (Gris moyen)

**Autres Couleurs:**
- Success: `#4CAF50` (Vert)
- Warning: `#FF9800` (Orange)
- Error: `#F44336` (Rouge)
- Info: `#2196F3` (Bleu)

### Changer de Thème

1. Aller dans **⚙️ Paramètres**
2. Section **🎨 Apparence**
3. Sélectionner thème dans le menu déroulant
4. Redémarrer l'application

---

## 🔍 Recherche

### Page Applications
- Recherche en temps réel
- Filtre par nom ET description
- Affiche uniquement catégories contenant résultats
- Stats mises à jour dynamiquement

### Page Tools
- Pas de recherche (sections repliables)
- Organiser par type d'outil

---

## ⚙️ Configuration Avancée

### Fichiers de Configuration

**Emplacement:** `/config/`

1. **app_config.json** - Configuration globale
2. **theme_config.json** - Thèmes personnalisés
3. **custom_layout.json** - Layout personnalisé

### Mode Portable

**Activer:**
1. ⚙️ Paramètres → 🔧 Avancé
2. Toggle "Mode Portable"
3. Redémarrer

**Effet:**
- Données stockées dans dossier app (pas AppData)
- Pas de modifications registre
- Transportable sur clé USB

### Mode Debug

**Activer:**
1. ⚙️ Paramètres → 🔧 Avancé
2. Toggle "Mode Debug"

**Effet:**
- Logs détaillés dans `/logs/`
- Messages console affichés
- Informations de débogage

---

## 🐛 Dépannage

### L'application ne se lance pas

**Problème:** Double-clic sur .bat ne fait rien

**Solution:**
1. Vérifier Python 3.12 installé:
   ```cmd
   python --version
   ```
   Doit afficher: `Python 3.12.x`

2. Vérifier CustomTkinter:
   ```cmd
   pip show customtkinter
   ```
   Version requise: 5.2.2

3. Réinstaller dépendances:
   ```cmd
   pip install --upgrade customtkinter
   ```

### L'application crash au lancement

**Problème:** Fenêtre s'ouvre puis se ferme

**Solutions:**
1. Vérifier logs dans `/logs/`
2. Lancer en mode debug (voir console)
3. Vérifier fichier `data/programs.json` existe

### Les applications ne s'installent pas

**Problème:** Bouton "Installer" ne fait rien

**Vérifications:**
1. WinGet installé?
   ```cmd
   winget --version
   ```

2. Droits administrateur?
   - Clic droit sur .bat → "Exécuter en tant qu'administrateur"

3. Connexion internet active?

### Erreur "Python 3.14 incompatible"

**Problème:** Vous avez Python 3.14 ou 3.13

**Solution:**
CustomTkinter supporte uniquement Python 3.8-3.12

1. Désinstaller Python 3.14
2. Installer Python 3.12.x
3. Recréer environnement virtuel

### Interface trop petite/grande

**Solution:**
1. ⚙️ Paramètres → 🎨 Apparence
2. Ajuster "Taille de police" (slider)
3. Valeurs: 12-20px

### Performances lentes

**Solutions:**
1. Réduire limite apps/catégorie:
   - ⚙️ Paramètres → ⚡ Performances
   - Slider "Limite apps" → 10-15

2. Désactiver animations:
   - ⚙️ Paramètres → ⚡ Performances
   - Toggle "Animation" → OFF

3. Nettoyer système:
   - ⚡ Optimisations → 🧹 Nettoyage
   - Exécuter toutes les actions

---

## 📞 Support

### Fichiers Logs

**Emplacement:** `/logs/nitrite_YYYYMMDD_HHMMSS.log`

Contient:
- Messages d'erreur
- Actions utilisateur
- État système
- Stack traces

### Informations Système

Pour rapport de bug, inclure:
1. Version Windows
2. Version Python (`python --version`)
3. Version CustomTkinter (`pip show customtkinter`)
4. Contenu dernier log
5. Capture d'écran si possible

---

## 🚀 Raccourcis Clavier

(À implémenter)

- `Ctrl + F` - Recherche
- `Ctrl + S` - Sauvegarder config
- `Ctrl + R` - Rafraîchir
- `Ctrl + Q` - Quitter
- `F5` - Recharger page
- `F11` - Plein écran

---

## 📝 Notes Importantes

### Limitations Actuelles

1. **20 apps max par catégorie** (sauf catégories protégées)
   - Raison: Performance
   - Exception: Désinstallateurs, Antivirus, Outils OrdiPlus

2. **20 outils max par section** (page Tools)
   - Raison: Performance
   - "... et X autres outils" affiché

3. **Installation séquentielle** (pas parallèle)
   - Les apps s'installent une par une
   - Évite conflits et surcharge

### Catégories Protégées

Ces catégories affichent TOUTES leurs applications:
- ✅ Désinstallateurs
- ✅ Antivirus
- ✅ Outils OrdiPlus

### Compatibilité

**Testé sur:**
- Windows 10 21H2+
- Windows 11 22H2+

**Non supporté:**
- Windows 7/8/8.1 (CustomTkinter incompatible)
- Python < 3.8 ou > 3.12

---

## 🎓 Conseils d'Utilisation

### Pour Techniciens

1. **Master Install d'abord** pour setup rapide
2. **Diagnostic** avant toute intervention
3. **Backup** avant modifications importantes
4. **Optimisations** en fin d'intervention

### Pour Particuliers

1. Commencer par **🚀 Master Install** → Pack "Usage Personnel"
2. Explorer **📦 Applications** pour besoins spécifiques
3. Configurer **⚙️ Paramètres** selon préférences
4. Utiliser **💾 Sauvegarde** régulièrement

### Pour Développeurs

1. Pack "💻 Développeur" dans **Master Install**
2. Compléter avec apps spécifiques dans **📦 Applications**
3. Activer **Mode Debug** dans paramètres
4. Consulter logs pour diagnostics

---

## 📚 Ressources

- **Site Web:** (à venir)
- **GitHub:** (à venir)
- **Documentation API:** (à venir)
- **Vidéos Tutoriels:** (à venir)

---

## 📄 Licence

© 2024 NiTriTe - Tous droits réservés

---

**Version:** 14.0 MVP  
**Date:** Décembre 2024  
**Auteur:** NiTriTe Development Team
