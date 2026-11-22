"""Troca o preenchimento amarelo pelo verde nos ícones SVG que têm traço branco por cima.

Amarelo com branco em cima fica ilegível (contraste 1,45:1). Só mexe nos SVGs em que
cores.amarelo_sob_branco() acusa o problema, e só nos preenchimentos: traços amarelos
sobre o fundo escuro continuam amarelos. Idempotente. Roda a partir da raiz do repositório,
depois de paleta.py.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cores  # noqa: E402

TROCA = {cores.AMARELO: cores.VERDE, cores.AMARELO_HOVER: cores.VERDE_HOVER,
         cores.AMARELO_PRESSIONADO: cores.VERDE_PRESSIONADO, "#F0C419": cores.VERDE_HOVER}


def trocar(svg):
    def sub(m):
        cor = cores.normalizar(m.group(3))
        return m.group(1) + m.group(2) + TROCA[cor] if cor in TROCA else m.group(0)
    return re.sub(r"""(fill)(\s*(?:=\s*["']|:\s*))(#[0-9a-fA-F]{6}\b)""", sub, svg, flags=re.I)


def main(raiz="."):
    mudados = []
    for caminho in sorted(glob.glob(os.path.join(raiz, "resources", "images", "*.svg"))):
        with open(caminho, encoding="utf-8") as f:
            svg = f.read()
        if not cores.amarelo_sob_branco(svg):
            continue
        novo = trocar(svg)
        if novo != svg:
            with open(caminho, "w", encoding="utf-8", newline="") as f:
                f.write(novo)
            mudados.append(os.path.basename(caminho))
    print(f"{len(mudados)} ícones com amarelo sob branco passaram para o verde {cores.VERDE}")
    for nome in mudados:
        print("  " + nome)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
