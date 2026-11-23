"""Troca a paleta reggae antiga (amarelo #FFD21F, verde #1D7F3A, fundos cinza-oliva) pela paleta do Selecta 3D
(ouro #F0B41C, musgo #4D7C2A, vermelho #CF2E1F, madeira #15110C, papel #F2E6C9).

Pega as cores escritas como hex (#RRGGBB, 0xRRGGBB), como wxColour/RGB(r, g, b), como r / 255.f e como
floats 0.xxxf, e os pixels exatos das PNG de resources/images. Roda a partir da raiz do repositório. Idempotente.

    python3 scripts/reggae/paleta_selecta.py
"""
import os
import re

TROCA = {
    # acento
    "FFD21F": "F0B41C", "FFE266": "F5C64A", "E6B800": "D69E0E", "F0C419": "F2BC2E", "FFF0A8": "F8DD94",
    "FFE680": "F6D06E", "F7E9AE": "F5E3B4", "FBF4D6": "FAF2DC", "FFD220": "F0B41D", "1C1500": "1A140C",
    # verde, vermelho
    "1D7F3A": "4D7C2A", "23913F": "588C31", "1A7535": "436E24", "2FBF5B": "8DBA63", "E8302A": "CF2E1F",
    # fundos e linhas do modo escuro
    "0B0B09": "15110C", "161612": "1E1811", "1E1D18": "292117", "2A2820": "33291C", "36332A": "3D3223",
    "3A372D": "45392A", "564A1A": "533F14", "352F19": "332812", "625E50": "66594A",
    # textos do modo escuro
    "F7F1DC": "F2E6C9", "DDD7C3": "DDCFAF", "A6A08B": "A8997B", "77725F": "7B6E56", "8E8873": "8F8268",
    # cena 3D
    "14140F": "15110C", "3A382A": "3E3324", "E6E1D1": "E9DFC5",
    # âmbar do modo claro
    "806300": "7D5800", "8C6D00": "8A6200", "6E5500": "6A4A00",
}
assert not set(TROCA.values()) & set(TROCA), "uma cor nova é também uma antiga: a troca não seria idempotente"

RGB = {tuple(int(k[i:i + 2], 16) for i in (0, 2, 4)): tuple(int(v[i:i + 2], 16) for i in (0, 2, 4)) for k, v in TROCA.items()}

EXT = (".cpp", ".hpp", ".h", ".c", ".svg", ".css", ".html", ".js", ".json")
# PNG desenhadas na paleta (as fotos de impressora e de calibração têm pixels iguais por acaso e ficam de fora)
PNG = ("toolbar_background_dark.png",)
PULAR = ("resources/profiles", "resources/web/include", "deps", "deps_src", "src/imgui", "src/libslic3r")


def _hex(m):
    velho = m.group(2)
    novo = TROCA.get(velho.upper())
    if not novo:
        return m.group(0)
    return m.group(1) + (novo if velho.isupper() or velho.isdigit() else novo.lower())


def _num(s):
    return int(s, 16) if s.lower().startswith("0x") else int(s)


def _wx(m):
    cor = tuple(_num(m.group(i)) for i in (2, 3, 4))
    novo = RGB.get(cor)
    if not novo:
        return m.group(0)
    hexa = m.group(2).lower().startswith("0x")
    fmt = (lambda n: "0x%02X" % n) if hexa else str
    return "%s(%s, %s, %s" % (m.group(1), *map(fmt, novo))


def _div(m):
    cor = tuple(int(m.group(i)) for i in (1, 2, 3))
    novo = RGB.get(cor)
    if not novo:
        return m.group(0)
    return "%d / 255.f, %d / 255.f, %d / 255.f" % novo


def _float(m):
    cor = tuple(round(float(m.group(i)) * 255) for i in (1, 2, 3))
    novo = next((n for v, n in RGB.items() if all(abs(a - b) <= 1 for a, b in zip(v, cor))), None)
    if not novo:
        return m.group(0)
    return "%.3ff, %.3ff, %.3ff" % tuple(c / 255 for c in novo)


PADROES = [
    (re.compile(r"(#|0x)([0-9A-Fa-f]{6})(?![0-9A-Fa-f])"), _hex),
    (re.compile(r"\b(wxColour|wxColor|RGB|ImColor|IM_COL32|rgba?)\(\s*(0x[0-9A-Fa-f]{2}|\d{1,3})\s*,\s*(0x[0-9A-Fa-f]{2}|\d{1,3})\s*,\s*(0x[0-9A-Fa-f]{2}|\d{1,3})"), _wx),
    (re.compile(r"(\{)\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(?=\s*\})"), lambda m: _wx(m).replace("{(", "{")),
    (re.compile(r"(\d{1,3})\s*/\s*255\.f\s*,\s*(\d{1,3})\s*/\s*255\.f\s*,\s*(\d{1,3})\s*/\s*255\.f"), _div),
    (re.compile(r"(0?\.\d+)f\s*,\s*(0?\.\d+)f\s*,\s*(0?\.\d+)f"), _float),
]


def textos():
    total = {}
    for raiz in ("src", "resources"):
        for base, pastas, nomes in os.walk(raiz):
            rel = os.path.relpath(base, ".").replace(os.sep, "/")
            if any(rel.startswith(p) for p in PULAR):
                pastas[:] = []
                continue
            for nome in nomes:
                if not nome.lower().endswith(EXT):
                    continue
                p = os.path.join(base, nome)
                try:
                    t = open(p, encoding="utf-8", newline="").read()
                except UnicodeDecodeError:
                    continue
                novo, n = t, 0
                for padrao, f in PADROES:
                    novo, k = padrao.subn(f, novo)
                    n += k
                if novo != t:
                    open(p, "w", encoding="utf-8", newline="").write(novo)
                    total[p] = n
    return total


def imagens():
    from PIL import Image
    mudadas = []
    for nome in PNG:
        if True:
            p = os.path.join("resources", "images", nome)
            try:
                img = Image.open(p)
            except OSError:  # arquivo com extensão .png que não é PNG
                continue
            modo = img.mode
            rgba = img.convert("RGBA")
            px = rgba.load()
            mudou = False
            for y in range(rgba.height):
                for x in range(rgba.width):
                    r, g, b, a = px[x, y]
                    novo = RGB.get((r, g, b))
                    if novo and a:
                        px[x, y] = (*novo, a)
                        mudou = True
            if mudou:
                rgba.convert(modo).save(p) if modo in ("RGB", "RGBA") else rgba.save(p)
                mudadas.append(p)
    return mudadas


if __name__ == "__main__":
    t = textos()
    print("textos:", len(t), "arquivos,", sum(t.values()), "trocas")
    print("png:", len(imagens()), "arquivos")
