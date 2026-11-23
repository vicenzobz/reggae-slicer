"""Paleta do Reggae Slicer e funções de cor usadas por verde_sob_branco.py e mostruario.py."""
import re

# Paleta do Selecta 3D (tema reggae)
AMARELO = "#F0B41C"          # acento
AMARELO_HOVER = "#F5C64A"
AMARELO_PRESSIONADO = "#D69E0E"
TINTA_ACENTO = "#1A140C"     # texto sobre o amarelo
# Verde para elementos pequenos com traço branco (marcar, ligar, botão escolhido).
# O ouro com branco em cima tem contraste 1,87:1; este musgo tem 4,96:1 com o branco
# e 3,79:1 com o fundo #15110C, então aparece nos dois modos.
VERDE = "#4D7C2A"
VERDE_HOVER = "#588C31"
VERDE_PRESSIONADO = "#436E24"
VERDE_ARCO = "#8DBA63"
# Modo claro: o amarelo some no branco. Linhas e textos do acento viram âmbar escuro
# (BitmapCache.cpp e StateColor::accentText()); o amarelo que é fundo de um desenho escuro
# usa AMARELO_FUNDO, igual a olho nu, para a troca não pegar nele.
AMBAR = "#7D5800"
AMBAR_HOVER = "#8A6200"
AMBAR_PRESSIONADO = "#6A4A00"
AMARELO_FUNDO = "#F0B41D"
VERMELHO = "#CF2E1F"

ESCURO = {"fundo": "#15110C", "painel": "#1E1811", "painel-2": "#292117", "painel-3": "#33291C",
          "linha": "#45392A", "texto": "#F2E6C9", "texto-2": "#DDCFAF", "texto-3": "#A8997B",
          "apagado": "#7B6E56", "cena": "#15110C", "mesa": "#3E3324"}
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


AMARELOS = {AMARELO, AMARELO_HOVER, AMARELO_PRESSIONADO, "#F2BC2E", AMARELO_FUNDO}
# troca que BitmapCache.cpp faz nos SVG no modo claro
TROCAS_CLARO = {AMARELO: AMBAR, AMARELO_HOVER: AMBAR_HOVER, AMARELO_PRESSIONADO: AMBAR_PRESSIONADO}

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


def marca(svg):
    """Arquivos da marca gerados por gerar_marca.py: cores lado a lado, sem sobreposição."""
    return 'data-reggae-marca="1"' in svg


def amarelo_sob_branco(svg):
    """True se o SVG pinta um preenchimento amarelo e também algo claro (traço ou preenchimento)."""
    if marca(svg):
        return False
    p = pinturas(svg)
    tem_amarelo = any(t == "fill" and c in AMARELOS for t, c in p)
    tem_claro = any(claro(c) and c not in AMARELOS for t, c in p)
    return tem_amarelo and tem_claro


def escuro_demais(cor):
    return luminancia(cor) < 0.2


def amarelo_de_fundo(svg):
    """True se o SVG pinta um preenchimento amarelo e também um desenho escuro (o amarelo é o fundo)."""
    if marca(svg):
        return False
    p = pinturas(svg)
    tem_amarelo = any(t == "fill" and c in (AMARELOS - {AMARELO_FUNDO}) for t, c in p)
    tem_escuro = any(escuro_demais(c) for t, c in p if c not in AMARELOS)
    return tem_amarelo and tem_escuro
