"""Acerta o acento amarelo no modo claro, onde o amarelo some no branco (contraste 1,45:1).

- SVG: no modo claro o BitmapCache.cpp troca o amarelo por âmbar escuro. Nos ícones em que o
  amarelo é o fundo de um desenho escuro, o preenchimento passa para cores.AMARELO_FUNDO (#F0B41D,
  igual a olho nu), que a troca não pega, para o desenho continuar legível.
- CSS das telas web: `color: #F0B41C` vira âmbar nos arquivos do tema claro (os `dark.css` ficam
  amarelos) e as caixas de marcar e os botões de opção marcados passam para o verde, como no resto
  do programa.

Idempotente. Roda a partir da raiz do repositório, depois de paleta.py e verde_sob_branco.py.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cores  # noqa: E402

FUNDO = {cores.AMARELO, cores.AMARELO_HOVER, cores.AMARELO_PRESSIONADO, "#F2BC2E"}


def svg_fundo(svg):
    def sub(m):
        return m.group(1) + m.group(2) + cores.AMARELO_FUNDO if cores.normalizar(m.group(3)) in FUNDO else m.group(0)
    return re.sub(r"""(fill)(\s*(?:=\s*["']|:\s*))(#[0-9a-fA-F]{6}\b)""", sub, svg, flags=re.I)


# regras CSS de caixa de marcar / botão de opção marcados
MARCADO = re.compile(r"(?i)checked|checkbox-mark")


def css(texto, tema_escuro):
    def bloco(m):
        seletor, corpo = m.group(1), m.group(2)
        if MARCADO.search(seletor):
            corpo = re.sub(r"(?i)#F0B41C", cores.VERDE, corpo)
        elif not tema_escuro:
            corpo = re.sub(r"(?i)((?<![-\w])color\s*:\s*)#F0B41C", r"\g<1>" + cores.AMBAR, corpo)
        return seletor + "{" + corpo + "}"
    return re.sub(r"([^{}]*)\{([^{}]*)\}", bloco, texto)


def main(raiz="."):
    n_svg = 0
    for caminho in sorted(glob.glob(os.path.join(raiz, "resources", "images", "*.svg"))):
        with open(caminho, encoding="utf-8") as f:
            svg = f.read()
        if cores.amarelo_de_fundo(svg):
            novo = svg_fundo(svg)
            if novo != svg:
                with open(caminho, "w", encoding="utf-8", newline="") as f:
                    f.write(novo)
                n_svg += 1
    n_css = 0
    web = os.path.join(raiz, "resources", "web")
    for caminho in sorted(glob.glob(os.path.join(web, "**", "*.css"), recursive=True)
                          + glob.glob(os.path.join(web, "**", "*.html"), recursive=True)):
        if os.sep + "include" + os.sep in caminho:
            continue
        with open(caminho, encoding="utf-8", errors="surrogateescape") as f:
            texto = f.read()
        novo = css(texto, os.path.basename(caminho).lower() == "dark.css")
        if novo != texto:
            with open(caminho, "w", encoding="utf-8", errors="surrogateescape", newline="") as f:
                f.write(novo)
            n_css += 1
    print(f"{n_svg} ícones com amarelo de fundo marcados com {cores.AMARELO_FUNDO}; {n_css} arquivos CSS/HTML acertados")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
