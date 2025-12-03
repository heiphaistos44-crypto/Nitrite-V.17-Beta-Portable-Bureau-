# 🎨 Migration CustomTkinter - Guide Complet

## 📊 PLAN DE MIGRATION

### Phase 1 : Préparation ✅ TERMINÉ
- ✅ Installation CustomTkinter
- ✅ Ajout à requirements.txt
- ✅ Tests de compatibilité

### Phase 2 : Module Wrapper (EN COURS)
- 🔄 Création module `ctk_widgets.py`
- 🔄 Wrapper pour migration progressive
- 🔄 Thèmes CustomTkinter

### Phase 3 : Migration Interface Principale
- ⏳ Widgets de base (Buttons, Labels, Frames)
- ⏳ Navigation menu
- ⏳ Content area
- ⏳ Sidebar

### Phase 4 : Migration Pages
- ⏳ Applications page
- ⏳ Tools page
- ⏳ Settings page
- ⏳ Diagnostic page
- ⏳ Monitoring dashboard
- ⏳ Network tools
- ⏳ Script automation

### Phase 5 : Effets Modernes
- ⏳ Animations de transition
- ⏳ Hover effects avancés
- ⏳ Fade in/out
- ⏳ Coins arrondis partout
- ⏳ Ombres portées

### Phase 6 : Tests et Polish
- ⏳ Tests complets
- ⏳ Ajustements de couleurs
- ⏳ Performance
- ⏳ Responsive design

---

## 🔧 CHANGEMENTS PRINCIPAUX

### Imports

**AVANT** :
```python
import tkinter as tk
from tkinter import ttk, messagebox
```

**APRÈS** :
```python
import customtkinter as ctk
from tkinter import messagebox  # Garder pour dialogs
```

### Widgets de Base

#### Bouton

**AVANT** :
```python
button = tk.Button(
    parent,
    text="Installer",
    bg="#ff6b00",
    fg="white",
    font=("Segoe UI", 10),
    command=callback
)
```

**APRÈS** :
```python
button = ctk.CTkButton(
    parent,
    text="Installer",
    fg_color="#ff6b00",
    hover_color="#ff8533",
    text_color="white",
    font=("Segoe UI", 10),
    corner_radius=10,
    command=callback
)
```

#### Label

**AVANT** :
```python
label = tk.Label(
    parent,
    text="NiTriTe V13",
    bg="#0a0a0a",
    fg="#ffffff",
    font=("Segoe UI", 16, "bold")
)
```

**APRÈS** :
```python
label = ctk.CTkLabel(
    parent,
    text="NiTriTe V13",
    fg_color="transparent",
    text_color="#ffffff",
    font=("Segoe UI", 16, "bold")
)
```

#### Frame

**AVANT** :
```python
frame = tk.Frame(parent, bg="#1e1e1e")
```

**APRÈS** :
```python
frame = ctk.CTkFrame(
    parent,
    fg_color="#1e1e1e",
    corner_radius=15
)
```

#### Entry

**AVANT** :
```python
entry = tk.Entry(
    parent,
    bg="#1e1e1e",
    fg="white",
    insertbackground="white"
)
```

**APRÈS** :
```python
entry = ctk.CTkEntry(
    parent,
    fg_color="#1e1e1e",
    text_color="white",
    border_color="#ff6b00",
    corner_radius=10
)
```

---

## 🎨 NOUVEAUX WIDGETS MODERNES

### Switch (Toggle)

```python
switch = ctk.CTkSwitch(
    parent,
    text="Mode sombre",
    command=toggle_theme,
    fg_color="#ff6b00",
    progress_color="#ff8533"
)
```

### Slider

```python
slider = ctk.CTkSlider(
    parent,
    from_=0,
    to=100,
    command=on_slider_change,
    fg_color="#1e1e1e",
    progress_color="#ff6b00",
    button_color="#ff8533"
)
```

### ProgressBar

```python
progress = ctk.CTkProgressBar(
    parent,
    fg_color="#1e1e1e",
    progress_color="#ff6b00",
    corner_radius=10
)
progress.set(0.5)  # 50%
```

### Segmented Button

```python
segmented = ctk.CTkSegmentedButton(
    parent,
    values=["Option 1", "Option 2", "Option 3"],
    command=on_segment_change,
    fg_color="#1e1e1e",
    selected_color="#ff6b00"
)
```

---

## 🎯 THÈMES CUSTOMTKINTER

### Configuration Thème Global

```python
# Définir le thème par défaut
ctk.set_appearance_mode("dark")  # "dark" ou "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

# OU créer thème personnalisé
ctk.set_default_color_theme({
    "CTkButton": {
        "fg_color": ("#ff6b00", "#ff8533"),
        "hover_color": ("#ff8533", "#ff6b00"),
        "text_color": "#ffffff"
    }
})
```

### Thème Orange Personnalisé (NiTriTe)

```python
NITRITE_THEME = {
    "CTk": {
        "fg_color": ["#0a0a0a", "#0a0a0a"]
    },
    "CTkToplevel": {
        "fg_color": ["#0a0a0a", "#0a0a0a"]
    },
    "CTkFrame": {
        "corner_radius": 15,
        "border_width": 0,
        "fg_color": ["#1e1e1e", "#1e1e1e"],
        "top_fg_color": ["#252525", "#252525"],
        "border_color": ["#333333", "#333333"]
    },
    "CTkButton": {
        "corner_radius": 10,
        "border_width": 0,
        "fg_color": ["#ff6b00", "#ff6b00"],
        "hover_color": ["#ff8533", "#ff8533"],
        "text_color": ["#ffffff", "#ffffff"],
        "border_color": ["#ff6b00", "#ff6b00"]
    },
    "CTkLabel": {
        "corner_radius": 0,
        "fg_color": "transparent",
        "text_color": ["#ffffff", "#ffffff"]
    },
    "CTkEntry": {
        "corner_radius": 10,
        "border_width": 2,
        "fg_color": ["#1e1e1e", "#1e1e1e"],
        "border_color": ["#ff6b00", "#ff6b00"],
        "text_color": ["#ffffff", "#ffffff"],
        "placeholder_text_color": ["#888888", "#888888"]
    },
    "CTkSwitch": {
        "corner_radius": 1000,
        "border_width": 3,
        "button_length": 0,
        "fg_color": ["#333333", "#333333"],
        "progress_color": ["#ff6b00", "#ff6b00"],
        "button_color": ["#ffffff", "#ffffff"],
        "button_hover_color": ["#cccccc", "#cccccc"],
        "text_color": ["#ffffff", "#ffffff"]
    },
    "CTkProgressBar": {
        "corner_radius": 10,
        "border_width": 0,
        "fg_color": ["#1e1e1e", "#1e1e1e"],
        "progress_color": ["#ff6b00", "#ff6b00"],
        "border_color": ["#333333", "#333333"]
    }
}
```

---

## ⚡ EFFETS MODERNES

### Animation Fade In

```python
def fade_in(widget, duration=300):
    """Anime l'apparition du widget"""
    steps = 20
    delay = duration // steps

    def animate(step=0):
        if step <= steps:
            alpha = step / steps
            # CustomTkinter n'a pas d'alpha direct, on utilise une approche différente
            widget.after(delay, lambda: animate(step + 1))

    animate()
```

### Hover Effect Avancé

```python
def create_hover_button(parent, text, command):
    """Bouton avec effet hover avancé"""
    button = ctk.CTkButton(
        parent,
        text=text,
        fg_color="#ff6b00",
        hover_color="#ff8533",
        corner_radius=15,
        border_width=2,
        border_color="transparent",
        command=command
    )

    def on_enter(e):
        button.configure(border_color="#ff8533")
        button.configure(cursor="hand2")

    def on_leave(e):
        button.configure(border_color="transparent")

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    return button
```

### Transition Smooth

```python
def smooth_transition(widget, from_color, to_color, steps=20):
    """Transition de couleur smooth"""
    import colorsys

    # Convertir hex en RGB
    from_rgb = tuple(int(from_color[i:i+2], 16) for i in (1, 3, 5))
    to_rgb = tuple(int(to_color[i:i+2], 16) for i in (1, 3, 5))

    def animate(step=0):
        if step <= steps:
            # Interpoler entre les couleurs
            factor = step / steps
            current_rgb = tuple(
                int(from_rgb[i] + (to_rgb[i] - from_rgb[i]) * factor)
                for i in range(3)
            )
            current_color = f"#{current_rgb[0]:02x}{current_rgb[1]:02x}{current_rgb[2]:02x}"

            widget.configure(fg_color=current_color)
            widget.after(15, lambda: animate(step + 1))

    animate()
```

---

## 📋 CHECKLIST MIGRATION

### Interface Principale (gui_modern_v13.py)

- [ ] Importer CustomTkinter
- [ ] Changer `tk.Tk()` en `ctk.CTk()`
- [ ] Migrer sidebar (navigation menu)
- [ ] Migrer header
- [ ] Migrer content area
- [ ] Migrer tous les boutons
- [ ] Migrer tous les labels
- [ ] Migrer tous les frames
- [ ] Tester navigation

### Pages Avancées (advanced_pages.py)

- [ ] Settings page
  - [ ] Thème selector (utiliser CTkSegmentedButton)
  - [ ] Switches pour options
  - [ ] Boutons modernes
- [ ] Diagnostic page
  - [ ] Cards avec coins arrondis
  - [ ] Progress bars CustomTkinter
  - [ ] Boutons de benchmark
- [ ] Autres pages similaires

### Nouveaux Modules

- [ ] Monitoring Dashboard
  - [ ] Graphiques (garder Canvas ou migrer vers CTkCanvas)
  - [ ] Boutons Start/Stop
  - [ ] Cards d'infos
- [ ] Network Tools
  - [ ] Tabs (CTkTabview)
  - [ ] Entrées pour IP/ports
  - [ ] Boutons d'action
- [ ] Script Automation
  - [ ] Éditeur de code (CTkTextbox)
  - [ ] Boutons de contrôle
  - [ ] Liste de scripts

---

## 🚀 PROCHAINES ÉTAPES

### Étape 1 : Créer Module Wrapper (AUJOURD'HUI)
Créer `src/ctk_wrapper.py` qui facilite la migration :

```python
"""
Wrapper CustomTkinter pour migration progressive
"""
import customtkinter as ctk

class ModernButton(ctk.CTkButton):
    """Bouton moderne NiTriTe avec settings par défaut"""
    def __init__(self, parent, **kwargs):
        # Settings par défaut
        defaults = {
            'corner_radius': 10,
            'fg_color': "#ff6b00",
            'hover_color': "#ff8533",
            'text_color': "white",
            'font': ("Segoe UI", 10)
        }
        defaults.update(kwargs)
        super().__init__(parent, **defaults)

class ModernFrame(ctk.CTkFrame):
    """Frame moderne avec coins arrondis"""
    def __init__(self, parent, **kwargs):
        defaults = {
            'corner_radius': 15,
            'fg_color': "#1e1e1e",
            'border_width': 0
        }
        defaults.update(kwargs)
        super().__init__(parent, **defaults)

# Ajouter d'autres wrappers...
```

### Étape 2 : Migrer Interface Principale (DEMAIN)
- Remplacer imports
- Changer classe principale
- Migrer widgets un par un
- Tester à chaque étape

### Étape 3 : Migrer Pages (JOUR 3-4)
- Une page à la fois
- Tester après chaque page
- Ajuster les couleurs

### Étape 4 : Polish Final (JOUR 5)
- Ajouter animations
- Effets hover
- Tests complets
- Documentation

---

## 📊 PROGRESS TRACKING

### Jour 1 (AUJOURD'HUI)
- [x] Installer CustomTkinter
- [x] Créer guide de migration
- [ ] Créer module wrapper
- [ ] Premiers tests

### Jour 2
- [ ] Migrer interface principale
- [ ] Migrer sidebar
- [ ] Migrer header
- [ ] Tests navigation

### Jour 3
- [ ] Migrer pages avancées
- [ ] Settings page
- [ ] Diagnostic page
- [ ] Tests pages

### Jour 4
- [ ] Migrer nouveaux modules
- [ ] Dashboard
- [ ] Network tools
- [ ] Script automation

### Jour 5
- [ ] Animations et effets
- [ ] Tests complets
- [ ] Ajustements finaux
- [ ] Documentation

---

**Status** : 🚀 Migration en cours - Jour 1
**Prochaine étape** : Créer module wrapper CustomTkinter
