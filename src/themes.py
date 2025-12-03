"""
Thèmes de couleurs pour NiTriTe V13
10 thèmes modernes avec différentes palettes de couleurs
"""


class Theme:
    """Classe de base pour un thème"""
    def __init__(self, name, colors):
        self.name = name
        self.BG_DARK = colors['BG_DARK']
        self.BG_MEDIUM = colors['BG_MEDIUM']
        self.BG_LIGHT = colors['BG_LIGHT']
        self.BG_CARD = colors['BG_CARD']
        self.BG_HOVER = colors['BG_HOVER']

        self.PRIMARY = colors['PRIMARY']
        self.PRIMARY_HOVER = colors['PRIMARY_HOVER']
        self.PRIMARY_PRESSED = colors['PRIMARY_PRESSED']

        self.TEXT_PRIMARY = colors['TEXT_PRIMARY']
        self.TEXT_SECONDARY = colors['TEXT_SECONDARY']
        self.TEXT_MUTED = colors['TEXT_MUTED']

        self.SUCCESS = colors['SUCCESS']
        self.WARNING = colors['WARNING']
        self.DANGER = colors['DANGER']
        self.INFO = colors['INFO']

        self.BORDER_COLOR = colors['BORDER_COLOR']
        self.BORDER_HOVER = colors['BORDER_HOVER']


# ============================================================================
# THÈME 1 : ORANGE (PAR DÉFAUT - NITRITE)
# ============================================================================
THEME_ORANGE = Theme("Orange NiTriTe", {
    'BG_DARK': "#1a1a1a",
    'BG_MEDIUM': "#2d2d2d",
    'BG_LIGHT': "#3a3a3a",
    'BG_CARD': "#252525",
    'BG_HOVER': "#353535",

    'PRIMARY': "#FF6B35",
    'PRIMARY_HOVER': "#ff8555",
    'PRIMARY_PRESSED': "#e55525",

    'TEXT_PRIMARY': "#ffffff",
    'TEXT_SECONDARY': "#b0b0b0",
    'TEXT_MUTED': "#808080",

    'SUCCESS': "#4caf50",
    'WARNING': "#ff9800",
    'DANGER': "#f44336",
    'INFO': "#2196f3",

    'BORDER_COLOR': "#404040",
    'BORDER_HOVER': "#606060",
})


# ============================================================================
# THÈME 2 : BLEU NUIT
# ============================================================================
THEME_BLUE_NIGHT = Theme("Bleu Nuit", {
    'BG_DARK': "#0d1117",
    'BG_MEDIUM': "#161b22",
    'BG_LIGHT': "#21262d",
    'BG_CARD': "#161b22",
    'BG_HOVER': "#1f242b",

    'PRIMARY': "#58a6ff",
    'PRIMARY_HOVER': "#79b8ff",
    'PRIMARY_PRESSED': "#388bfd",

    'TEXT_PRIMARY': "#c9d1d9",
    'TEXT_SECONDARY': "#8b949e",
    'TEXT_MUTED': "#6e7681",

    'SUCCESS': "#3fb950",
    'WARNING': "#d29922",
    'DANGER': "#f85149",
    'INFO': "#58a6ff",

    'BORDER_COLOR': "#30363d",
    'BORDER_HOVER': "#58a6ff",
})


# ============================================================================
# THÈME 3 : VIOLET MODERNE
# ============================================================================
THEME_PURPLE = Theme("Violet Moderne", {
    'BG_DARK': "#1a1625",
    'BG_MEDIUM': "#2a2438",
    'BG_LIGHT': "#3a3349",
    'BG_CARD': "#252035",
    'BG_HOVER': "#342d47",

    'PRIMARY': "#a855f7",
    'PRIMARY_HOVER': "#c084fc",
    'PRIMARY_PRESSED': "#9333ea",

    'TEXT_PRIMARY': "#f3f4f6",
    'TEXT_SECONDARY': "#c4b5fd",
    'TEXT_MUTED': "#9ca3af",

    'SUCCESS': "#10b981",
    'WARNING': "#f59e0b",
    'DANGER': "#ef4444",
    'INFO': "#8b5cf6",

    'BORDER_COLOR': "#4c4560",
    'BORDER_HOVER': "#a855f7",
})


# ============================================================================
# THÈME 4 : VERT CYBERPUNK
# ============================================================================
THEME_GREEN_CYBER = Theme("Vert Cyberpunk", {
    'BG_DARK': "#0a0e0a",
    'BG_MEDIUM': "#151a15",
    'BG_LIGHT': "#1f2a1f",
    'BG_CARD': "#141914",
    'BG_HOVER': "#1e291e",

    'PRIMARY': "#00ff41",
    'PRIMARY_HOVER': "#33ff66",
    'PRIMARY_PRESSED': "#00cc34",

    'TEXT_PRIMARY': "#e0ffe0",
    'TEXT_SECONDARY': "#a0ffa0",
    'TEXT_MUTED': "#60a060",

    'SUCCESS': "#00ff41",
    'WARNING': "#ffaa00",
    'DANGER': "#ff0055",
    'INFO': "#00ddff",

    'BORDER_COLOR': "#2a4a2a",
    'BORDER_HOVER': "#00ff41",
})


# ============================================================================
# THÈME 5 : ROSE ÉLÉGANT
# ============================================================================
THEME_PINK = Theme("Rose Élégant", {
    'BG_DARK': "#1a0e1a",
    'BG_MEDIUM': "#2d1a2d",
    'BG_LIGHT': "#3d2a3d",
    'BG_CARD': "#251525",
    'BG_HOVER': "#352535",

    'PRIMARY': "#ec4899",
    'PRIMARY_HOVER': "#f472b6",
    'PRIMARY_PRESSED': "#db2777",

    'TEXT_PRIMARY': "#fce7f3",
    'TEXT_SECONDARY': "#f9a8d4",
    'TEXT_MUTED': "#9d8b9d",

    'SUCCESS': "#10b981",
    'WARNING': "#f59e0b",
    'DANGER': "#ef4444",
    'INFO': "#ec4899",

    'BORDER_COLOR': "#4a3a4a",
    'BORDER_HOVER': "#ec4899",
})


# ============================================================================
# THÈME 6 : BLEU OCÉAN
# ============================================================================
THEME_OCEAN = Theme("Bleu Océan", {
    'BG_DARK': "#0a1628",
    'BG_MEDIUM': "#162a45",
    'BG_LIGHT': "#1e3a5f",
    'BG_CARD': "#142234",
    'BG_HOVER': "#1e3548",

    'PRIMARY': "#06b6d4",
    'PRIMARY_HOVER': "#22d3ee",
    'PRIMARY_PRESSED': "#0891b2",

    'TEXT_PRIMARY': "#f0f9ff",
    'TEXT_SECONDARY': "#bae6fd",
    'TEXT_MUTED': "#7dd3fc",

    'SUCCESS': "#14b8a6",
    'WARNING': "#f59e0b",
    'DANGER': "#ef4444",
    'INFO': "#06b6d4",

    'BORDER_COLOR': "#334e68",
    'BORDER_HOVER': "#06b6d4",
})


# ============================================================================
# THÈME 7 : ROUGE FEU
# ============================================================================
THEME_RED_FIRE = Theme("Rouge Feu", {
    'BG_DARK': "#1a0a0a",
    'BG_MEDIUM': "#2d1515",
    'BG_LIGHT': "#3d2020",
    'BG_CARD': "#251010",
    'BG_HOVER': "#352020",

    'PRIMARY': "#ef4444",
    'PRIMARY_HOVER': "#f87171",
    'PRIMARY_PRESSED': "#dc2626",

    'TEXT_PRIMARY': "#fee2e2",
    'TEXT_SECONDARY': "#fca5a5",
    'TEXT_MUTED': "#9d7070",

    'SUCCESS': "#10b981",
    'WARNING': "#f59e0b",
    'DANGER': "#ef4444",
    'INFO': "#3b82f6",

    'BORDER_COLOR': "#4a3030",
    'BORDER_HOVER': "#ef4444",
})


# ============================================================================
# THÈME 8 : DORÉ LUXE
# ============================================================================
THEME_GOLD = Theme("Doré Luxe", {
    'BG_DARK': "#1a1510",
    'BG_MEDIUM': "#2d2418",
    'BG_LIGHT': "#3d3420",
    'BG_CARD': "#251f14",
    'BG_HOVER': "#352f24",

    'PRIMARY': "#f59e0b",
    'PRIMARY_HOVER': "#fbbf24",
    'PRIMARY_PRESSED': "#d97706",

    'TEXT_PRIMARY': "#fef3c7",
    'TEXT_SECONDARY': "#fde68a",
    'TEXT_MUTED': "#9d8b6b",

    'SUCCESS': "#10b981",
    'WARNING': "#f59e0b",
    'DANGER': "#ef4444",
    'INFO': "#3b82f6",

    'BORDER_COLOR': "#4a4030",
    'BORDER_HOVER': "#f59e0b",
})


# ============================================================================
# THÈME 9 : MINIMALISTE GRIS
# ============================================================================
THEME_MINIMAL = Theme("Minimaliste Gris", {
    'BG_DARK': "#18181b",
    'BG_MEDIUM': "#27272a",
    'BG_LIGHT': "#3f3f46",
    'BG_CARD': "#27272a",
    'BG_HOVER': "#3f3f46",

    'PRIMARY': "#71717a",
    'PRIMARY_HOVER': "#a1a1aa",
    'PRIMARY_PRESSED': "#52525b",

    'TEXT_PRIMARY': "#fafafa",
    'TEXT_SECONDARY': "#d4d4d8",
    'TEXT_MUTED': "#a1a1aa",

    'SUCCESS': "#22c55e",
    'WARNING': "#eab308",
    'DANGER': "#ef4444",
    'INFO': "#3b82f6",

    'BORDER_COLOR': "#52525b",
    'BORDER_HOVER': "#a1a1aa",
})


# ============================================================================
# THÈME 10 : AURORE BORÉALE
# ============================================================================
THEME_AURORA = Theme("Aurore Boréale", {
    'BG_DARK': "#0f1419",
    'BG_MEDIUM': "#1a1f2e",
    'BG_LIGHT': "#252a3a",
    'BG_CARD': "#1a1f2e",
    'BG_HOVER': "#252a3a",

    'PRIMARY': "#00d9ff",
    'PRIMARY_HOVER': "#33e1ff",
    'PRIMARY_PRESSED': "#00b8d4",

    'TEXT_PRIMARY': "#e6fffa",
    'TEXT_SECONDARY': "#99f6e4",
    'TEXT_MUTED': "#5eead4",

    'SUCCESS': "#2dd4bf",
    'WARNING': "#fbbf24",
    'DANGER': "#f87171",
    'INFO': "#00d9ff",

    'BORDER_COLOR': "#2c3e50",
    'BORDER_HOVER': "#00d9ff",
})


# ============================================================================
# THÈME 11 : SUNSET GRADIENT (PREMIUM)
# ============================================================================
THEME_SUNSET = Theme("Coucher de Soleil", {
    'BG_DARK': "#1a1215",
    'BG_MEDIUM': "#2d1f24",
    'BG_LIGHT': "#3d2f34",
    'BG_CARD': "#251a1f",
    'BG_HOVER': "#352a2f",

    'PRIMARY': "#ff7b54",
    'PRIMARY_HOVER': "#ff9a76",
    'PRIMARY_PRESSED': "#e86840",

    'TEXT_PRIMARY': "#fff4f0",
    'TEXT_SECONDARY': "#ffcdb2",
    'TEXT_MUTED': "#b5838d",

    'SUCCESS': "#52b788",
    'WARNING': "#f4a261",
    'DANGER': "#e63946",
    'INFO': "#ff7b54",

    'BORDER_COLOR': "#4a3a3f",
    'BORDER_HOVER': "#ff7b54",
})


# ============================================================================
# THÈME 12 : MIDNIGHT BLUE (PREMIUM)
# ============================================================================
THEME_MIDNIGHT = Theme("Bleu Minuit", {
    'BG_DARK': "#0d1b2a",
    'BG_MEDIUM': "#1b263b",
    'BG_LIGHT': "#2a3f5f",
    'BG_CARD': "#152238",
    'BG_HOVER': "#1f3048",

    'PRIMARY': "#3a86ff",
    'PRIMARY_HOVER': "#5fa8ff",
    'PRIMARY_PRESSED': "#2670e0",

    'TEXT_PRIMARY': "#e0e1dd",
    'TEXT_SECONDARY': "#778da9",
    'TEXT_MUTED': "#415a77",

    'SUCCESS': "#52b788",
    'WARNING': "#ffba08",
    'DANGER': "#d90429",
    'INFO': "#3a86ff",

    'BORDER_COLOR': "#415a77",
    'BORDER_HOVER': "#3a86ff",
})


# ============================================================================
# THÈME 13 : EMERALD FOREST (PREMIUM)
# ============================================================================
THEME_EMERALD = Theme("Forêt Émeraude", {
    'BG_DARK': "#0b1a12",
    'BG_MEDIUM': "#142820",
    'BG_LIGHT': "#1e3a2c",
    'BG_CARD': "#102018",
    'BG_HOVER': "#1a3025",

    'PRIMARY': "#2ecc71",
    'PRIMARY_HOVER': "#58d68d",
    'PRIMARY_PRESSED': "#27ae60",

    'TEXT_PRIMARY': "#ecfdf5",
    'TEXT_SECONDARY': "#a7f3d0",
    'TEXT_MUTED': "#6ee7b7",

    'SUCCESS': "#2ecc71",
    'WARNING': "#f1c40f",
    'DANGER': "#e74c3c",
    'INFO': "#3498db",

    'BORDER_COLOR': "#2d5a40",
    'BORDER_HOVER': "#2ecc71",
})


# ============================================================================
# THÈME 14 : AMOLED BLACK (PREMIUM - Pour économie batterie)
# ============================================================================
THEME_AMOLED = Theme("AMOLED Noir Pur", {
    'BG_DARK': "#000000",
    'BG_MEDIUM': "#0a0a0a",
    'BG_LIGHT': "#151515",
    'BG_CARD': "#0d0d0d",
    'BG_HOVER': "#1a1a1a",

    'PRIMARY': "#FF6B35",
    'PRIMARY_HOVER': "#ff8555",
    'PRIMARY_PRESSED': "#e55525",

    'TEXT_PRIMARY': "#ffffff",
    'TEXT_SECONDARY': "#c0c0c0",
    'TEXT_MUTED': "#707070",

    'SUCCESS': "#00ff7f",
    'WARNING': "#ffd700",
    'DANGER': "#ff3333",
    'INFO': "#00bfff",

    'BORDER_COLOR': "#252525",
    'BORDER_HOVER': "#FF6B35",
})


# ============================================================================
# THÈME 15 : LIGHT MODE ORANGE (PREMIUM)
# ============================================================================
THEME_LIGHT_ORANGE = Theme("Mode Clair Orange", {
    'BG_DARK': "#f5f5f5",
    'BG_MEDIUM': "#ffffff",
    'BG_LIGHT': "#fafafa",
    'BG_CARD': "#ffffff",
    'BG_HOVER': "#f0f0f0",

    'PRIMARY': "#FF6B35",
    'PRIMARY_HOVER': "#e55525",
    'PRIMARY_PRESSED': "#cc4a20",

    'TEXT_PRIMARY': "#1a1a1a",
    'TEXT_SECONDARY': "#505050",
    'TEXT_MUTED': "#808080",

    'SUCCESS': "#2e7d32",
    'WARNING': "#f57c00",
    'DANGER': "#c62828",
    'INFO': "#1565c0",

    'BORDER_COLOR': "#e0e0e0",
    'BORDER_HOVER': "#FF6B35",
})


# ============================================================================
# DICTIONNAIRE DE TOUS LES THÈMES
# ============================================================================
ALL_THEMES = {
    "Orange NiTriTe": THEME_ORANGE,
    "Bleu Nuit": THEME_BLUE_NIGHT,
    "Violet Moderne": THEME_PURPLE,
    "Vert Cyberpunk": THEME_GREEN_CYBER,
    "Rose Élégant": THEME_PINK,
    "Bleu Océan": THEME_OCEAN,
    "Rouge Feu": THEME_RED_FIRE,
    "Doré Luxe": THEME_GOLD,
    "Minimaliste Gris": THEME_MINIMAL,
    "Aurore Boréale": THEME_AURORA,
    # Thèmes Premium
    "Coucher de Soleil": THEME_SUNSET,
    "Bleu Minuit": THEME_MIDNIGHT,
    "Forêt Émeraude": THEME_EMERALD,
    "AMOLED Noir Pur": THEME_AMOLED,
    "Mode Clair Orange": THEME_LIGHT_ORANGE,
}

# Thèmes premium (nécessitent une licence)
PREMIUM_THEMES = [
    "Coucher de Soleil",
    "Bleu Minuit", 
    "Forêt Émeraude",
    "AMOLED Noir Pur",
    "Mode Clair Orange",
]

# Thème actuel (par défaut: Orange)
current_theme = THEME_ORANGE


def get_theme(theme_name):
    """Récupérer un thème par son nom"""
    return ALL_THEMES.get(theme_name, THEME_ORANGE)


def get_theme_names():
    """Récupérer la liste des noms de thèmes"""
    return list(ALL_THEMES.keys())


def get_free_themes():
    """Récupérer la liste des thèmes gratuits"""
    return [name for name in ALL_THEMES.keys() if name not in PREMIUM_THEMES]


def get_premium_themes():
    """Récupérer la liste des thèmes premium"""
    return PREMIUM_THEMES


def is_premium_theme(theme_name):
    """Vérifier si un thème est premium"""
    return theme_name in PREMIUM_THEMES


def set_current_theme(theme_name):
    """Définir le thème actuel"""
    global current_theme
    current_theme = ALL_THEMES.get(theme_name, THEME_ORANGE)
    return current_theme
