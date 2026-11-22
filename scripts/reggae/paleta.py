"""Troca a paleta do OrcaSlicer pela paleta reggae do Organizador 3D.

Acento (verde-azulado do Orca) -> amarelo; fundos e textos do modo escuro -> tons quentes do Organizador.
Roda a partir da raiz do repositório. Idempotente.
"""
import os, re, sys

# acento e derivados (valem nos dois modos)
ACENTO = {
    "009688": "FFD21F",  # cor do Orca -> amarelo
    "26A69A": "FFE266",  # hover
    "00675B": "E6B800",  # acento escuro / pressionado
    "008172": "F0C419",  # hover no escuro
    "00897B": "E6B800",  # pressionado
    "22BFB0": "FFE266",  # foco
    "00FFD4": "FFF0A8",  # foco forte
    "4DB6AC": "FFE680",
    "52C7B8": "FFE680",
    "BFE1DE": "F7E9AE",  # item marcado (acento 25%) no claro
    "E5F0EE": "FBF4D6",  # foco de lista (acento 10%) no claro
}
# fundos do modo escuro do Orca -> Organizador (#0b0b09, #161612, #1e1d18, #2a2820)
ESCURO = {
    "2D2D31": "161612",  # fundo da janela
    "2D2D30": "0B0B09",  # barra superior
    "242428": "0B0B09",  # barra lateral de abas
    "36363C": "1E1D18", "36363B": "1E1D18", "36363D": "1E1D18", "333337": "1E1D18",
    "3E3E45": "2A2820",  # fundo de botão
    "4D4D54": "36332A",  # botão hover
    "4C4C55": "3A372D", "4C4C54": "3A372D", "4A4A51": "3A372D",  # linhas e bordas
    "54545B": "2A2820",  # painel lateral
    "223C3C": "564A1A",  # item marcado (acento 25%) no escuro
    "283232": "352F19",  # foco de lista (acento 10%) no escuro
}
# triplas RGB e floats usados no código
TRIPLAS = [
    (r"\b0\s*,\s*150\s*,\s*136\b", "255, 210, 31"),
    (r"\b0\s*,\s*137\s*,\s*123\b", "230, 184, 0"),
    (r"\b38\s*,\s*166\s*,\s*154\b", "255, 226, 102"),
    (r"0\.0?f?\s*,\s*150\.?0?f?\s*/\s*255\.?0?f?\s*,\s*136\.?0?f?\s*/\s*255\.?0?f?",
     "255.f / 255.f, 210.f / 255.f, 31.f / 255.f"),
    (r"0\.f\s*,\s*103\s*/\s*255\.f\s*,\s*91\s*/\s*255\.f", "230 / 255.f, 184 / 255.f, 0.f"),
    (r"38\s*/\s*255\.f\s*,\s*166\s*/\s*255\.f\s*,\s*154\s*/\s*255\.f", "255 / 255.f, 226 / 255.f, 102 / 255.f"),
    (r"0\.f\s*,\s*129\s*/\s*255\.f\s*,\s*114\s*/\s*255\.f", "240 / 255.f, 196 / 255.f, 25 / 255.f"),
]

def trocar_hex(texto, tabela):
    n = 0
    for velho, novo in tabela.items():
        padrao = re.compile(r"(?i)(#|0x)" + velho + r"(?![0-9a-f])")
        texto, k = padrao.subn(lambda m: m.group(1) + novo, texto)
        n += k
    return texto, n

EXT_SRC = (".cpp", ".hpp", ".h", ".c")
EXT_RES = (".svg", ".css", ".html", ".js", ".json")
PULAR = ("resources/profiles", "resources/web/include/three", "deps", "deps_src")

def processar(raiz, ext, tabelas, triplas):
    total = {}
    for base, pastas, nomes in os.walk(raiz):
        rel = os.path.relpath(base, ".")
        if any(rel.startswith(p) for p in PULAR):
            pastas[:] = []
            continue
        for nome in nomes:
            if not nome.lower().endswith(ext):
                continue
            p = os.path.join(base, nome)
            try:
                t = open(p, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            novo, n = t, 0
            for tab in tabelas:
                novo, k = trocar_hex(novo, tab); n += k
            for padrao, troca in triplas:
                novo, k = re.subn(padrao, troca, novo); n += k
            if n:
                open(p, "w", encoding="utf-8", newline="").write(novo)
                total[p] = n
    return total

if __name__ == "__main__":
    a = processar("src", EXT_SRC, [ACENTO, ESCURO], TRIPLAS)
    b = processar("resources", EXT_RES, [ACENTO, ESCURO], [])
    print("src:", len(a), "arquivos,", sum(a.values()), "trocas")
    print("resources:", len(b), "arquivos,", sum(b.values()), "trocas")
