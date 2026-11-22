"""Paleta do Reggae Slicer e funções de cor usadas por verde_sob_branco.py e mostruario.py."""
import re

# Paleta do Organizador 3D (tema reggae)
AMARELO = "#FFD21F"          # acento
AMARELO_HOVER = "#FFE266"
AMARELO_PRESSIONADO = "#E6B800"
TINTA_ACENTO = "#1C1500"     # texto sobre o amarelo
# Verde para elementos pequenos com traço branco (marcar, ligar, botão escolhido).
# O amarelo com branco em cima tem contraste 1,45:1; este verde tem 5,06:1 com o branco
# e 3,89:1 com o fundo #0B0B09, então aparece nos dois modos.
VERDE = "#1D7F3A"
VERDE_HOVER = "#23913F"
VERDE_PRESSIONADO = "#1A7535"
VERDE_ARCO = "#2FBF5B"
VERMELHO = "#E8302A"

ESCURO = {"fundo": "#0B0B09", "painel": "#161612", "painel-2": "#1E1D18", "painel-3": "#2A2820",
          "linha": "#3A372D", "texto": "#F7F1DC", "texto-2": "#DDD7C3", "texto-3": "#A6A08B",
          "apagado": "#77725F", "cena": "#14140F", "mesa": "#3A382A"}
CLARO = {"fundo": "#FFFFFF", "painel": "#F8F8F8", "linha": "#DBDBDB", "texto": "#262E30",
         "texto-2": "#363636", "apagado": "#6B6B6B", "cena": "#E7E7E7"}

HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")


def normalizar(cor):
    """'#fff' ou 'white' -> '#FFFFFF'."""
    cor = cor.strip()
    if cor.lower() == "white":
        return "#FFFFFF"
    m = HEX.fullmatch(cor)
    if not m:
        return None
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h.upper()


def luminancia(cor):
    h = normalizar(cor)[1:]
    canais = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    canais = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canais]
    return 0.2126 * canais[0] + 0.7152 * canais[1] + 0.0722 * canais[2]


def contraste(a, b):
    """Razão de contraste WCAG entre duas cores (1 a 21)."""
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


AMARELOS = {AMARELO, AMARELO_HOVER, AMARELO_PRESSIONADO, "#F0C419"}

# fill:#xxx, fill="#xxx", stroke:#xxx, stroke="#xxx"
_PINTURA = re.compile(r"""(fill|stroke)\s*(?:=\s*["']|:\s*)(#[0-9a-fA-F]{3,6}\b|white)""", re.I)


def pinturas(svg):
    """Lista de (tipo, cor) de um SVG: tipo é 'fill' ou 'stroke'."""
    out = []
    for m in _PINTURA.finditer(svg):
        cor = normalizar(m.group(2))
        if cor:
            out.append((m.group(1).lower(), cor))
    return out


def claro(cor):
    return luminancia(cor) > 0.75


def amarelo_sob_branco(svg):
    """True se o SVG pinta um preenchimento amarelo e também algo claro (traço ou preenchimento)."""
    p = pinturas(svg)
    tem_amarelo = any(t == "fill" and c in AMARELOS for t, c in p)
    tem_claro = any(claro(c) and c not in AMARELOS for t, c in p)
    return tem_amarelo and tem_claro
