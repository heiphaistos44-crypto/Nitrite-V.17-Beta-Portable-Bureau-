# 🐍 INSTRUCTIONS PYTHON 3.12

## ⚠️ PROBLÈME DÉTECTÉ

Vous avez **Python 3.14.0** installé, mais **CustomTkinter 5.2.2** ne supporte que **Python 3.8 à 3.12**.

```
❌ Python 3.14 → INCOMPATIBLE
✅ Python 3.12 → COMPATIBLE
```

---

## 🎯 SOLUTIONS

### Option A : Installer Python 3.12 (RECOMMANDÉ)

#### 1. Télécharger Python 3.12

**Lien direct :** https://www.python.org/downloads/release/python-3120/

Choisissez :
- **Windows 64-bit** : `Windows installer (64-bit)`
- **Windows 32-bit** : `Windows installer (32-bit)`

#### 2. Installation

1. **Lancer l'installateur**
2. ✅ **Cocher** : "Add Python 3.12 to PATH"
3. Cliquer : **"Customize installation"**
4. Cocher toutes les options
5. **Chemin recommandé** : `C:\Python312\`
6. Installer

#### 3. Vérification

```bash
C:\Python312\python.exe --version
# Doit afficher: Python 3.12.x
```

#### 4. Lancer l'application

Double-clic sur : **`LANCER_AVEC_PYTHON312.bat`**

Ce script :
- ✅ Cherche Python 3.12 automatiquement
- ✅ Installe CustomTkinter si besoin
- ✅ Lance l'application

---

### Option B : Utiliser py launcher

Si vous avez installé Python 3.12 mais le système utilise Python 3.14 par défaut :

```bash
py -3.12 -m src.v14_mvp.main_app
```

Ou créer un raccourci :

```batch
@echo off
py -3.12 -m src.v14_mvp.main_app
pause
```

---

### Option C : Environnement virtuel Python 3.12

```bash
# Créer venv avec Python 3.12
C:\Python312\python.exe -m venv venv_312

# Activer
venv_312\Scripts\activate

# Installer dépendances
pip install customtkinter

# Lancer
python -m src.v14_mvp.main_app
```

---

## 🔧 CHEMINS D'INSTALLATION PYTHON 3.12

Le script `LANCER_AVEC_PYTHON312.bat` cherche automatiquement dans :

```
C:\Python312\python.exe
C:\Program Files\Python312\python.exe
C:\Program Files (x86)\Python312\python.exe
%LOCALAPPDATA%\Programs\Python\Python312\python.exe
%APPDATA%\Python\Python312\python.exe
```

---

## 🎯 APRÈS INSTALLATION

### 1. Vérifier Python 3.12

```bash
C:\Python312\python.exe --version
# Python 3.12.x
```

### 2. Installer CustomTkinter

```bash
C:\Python312\python.exe -m pip install customtkinter
```

### 3. Lancer l'application

**Double-clic sur :** `LANCER_AVEC_PYTHON312.bat`

**Résultat attendu :**

```
✅ Python 3.12 trouvé: C:\Python312\python.exe
Python 3.12.x
✅ CustomTkinter 5.2.2
🚀 Lancement NiTriTe V14 MVP avec Python 3.12...

[Fenêtre s'ouvre avec interface moderne]
```

---

## 🆘 DÉPANNAGE

### Script ne trouve pas Python 3.12

**Vérifier manuellement :**
```bash
dir C:\Python312\python.exe
```

Si le chemin est différent, modifiez `LANCER_AVEC_PYTHON312.bat` ligne 15-19.

### Python 3.12 installé mais non détecté

**Lancer directement :**
```bash
"C:\Chemin\Vers\Python312\python.exe" -m src.v14_mvp.main_app
```

### CustomTkinter ne s'installe pas

**Installer manuellement :**
```bash
C:\Python312\python.exe -m pip install --upgrade pip
C:\Python312\python.exe -m pip install customtkinter
```

---

## 📊 COMPATIBILITÉ

### ✅ Versions Python Supportées

| Version | CustomTkinter | NiTriTe V14 |
|---------|---------------|-------------|
| 3.8     | ✅            | ✅          |
| 3.9     | ✅            | ✅          |
| 3.10    | ✅            | ✅          |
| 3.11    | ✅            | ✅          |
| 3.12    | ✅            | ✅          |
| 3.13    | ❌            | ❌          |
| 3.14    | ❌            | ❌          |

### 🎯 Version Recommandée

**Python 3.12.x** - Dernière version compatible avec CustomTkinter

---

## 💡 POURQUOI PYTHON 3.12 ?

1. **CustomTkinter 5.2.2** utilise des APIs qui ont changé en Python 3.13+
2. **Stabilité maximale** avec Python 3.12
3. **Bibliothèques tierces** bien testées avec 3.12
4. **Support LTS** de Python 3.12 jusqu'en 2028

---

## 🚀 RÉSUMÉ RAPIDE

```bash
# 1. Télécharger Python 3.12
# https://www.python.org/downloads/release/python-3120/

# 2. Installer avec "Add to PATH"

# 3. Lancer
Double-clic sur: LANCER_AVEC_PYTHON312.bat

# OU
C:\Python312\python.exe -m src.v14_mvp.main_app
```

---

## 📞 BESOIN D'AIDE ?

Si l'application ne se lance toujours pas après installation de Python 3.12 :

1. Vérifier version : `C:\Python312\python.exe --version`
2. Vérifier CustomTkinter : `C:\Python312\python.exe -c "import customtkinter"`
3. Copier l'erreur complète et demander de l'aide

**Bon développement ! 🎉**