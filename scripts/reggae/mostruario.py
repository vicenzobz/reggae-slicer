"""Mostruário de cores do Reggae Slicer: gera uma página HTML com todas as combinações de cor
da interface e confere o contraste de cada uma.

    python scripts/reggae/mostruario.py                  # gera mostruario-cores.html
    python scripts/reggae/mostruario.py --saida X.html
    python scripts/reggae/mostruario.py --verificar      # também sai com erro se algo reprovar

Mostra:
- a paleta;
- os pares texto/fundo e traço/fundo desenhados no código (abas, botões, marcar, ligar...),
  com a razão de contraste WCAG: texto precisa de 4,5:1, traço de ícone de 3:1;
- os ícones SVG que usam as cores do acento, no fundo escuro e no claro, como o programa os mostra
  (no modo escuro aplica as mesmas trocas de cor que BitmapCache.cpp);
- os ícones com preenchimento amarelo e traço branco, que reprovam (verde_sob_branco.py corrige);
- as regras CSS das telas web com fundo amarelo e texto claro, ou texto amarelo no tema claro
  (amarelo_no_claro.py corrige).

Roda a partir da raiz do repositório. Só usa a biblioteca padrão do Python.
"""
import argparse
import base64
import glob
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cores  # noqa: E402
from cores import AMARELO, AMBAR, CLARO, ESCURO, TINTA_ACENTO, VERDE  # noqa: E402

MINIMO = {"texto": 4.5, "traço": 3.0, "apagado": 3.0}

# (onde aparece, modo, frente, fundo, tipo, arquivo, pendente)
# "pendente" marca um problema conhecido que ainda não foi resolvido: aparece no relatório,
# mas não derruba --verificar.
PARES = [
    ("Texto principal", "escuro", ESCURO["texto"], ESCURO["painel"], "texto", "StateColor.cpp", False),
    ("Texto secundário", "escuro", ESCURO["texto-2"], ESCURO["painel"], "texto", "StateColor.cpp", False),
    ("Rótulo de parâmetro", "escuro", ESCURO["texto-3"], ESCURO["painel"], "texto", "StateColor.cpp", False),
    ("Texto apagado", "escuro", ESCURO["apagado"], ESCURO["painel"], "apagado", "StateColor.cpp", False),
    ("Aba do alto", "escuro", ESCURO["texto"], ESCURO["fundo"], "texto", "Notebook.cpp", False),
    ("Aba do alto escolhida", "ambos", "#FFFFFF", VERDE, "texto", "Notebook.cpp", False),
    ("Botão Fatiar / Exportar", "ambos", TINTA_ACENTO, AMARELO, "texto", "SideButton.cpp", False),
    ("Botão de confirmar", "ambos", TINTA_ACENTO, AMARELO, "texto", "Button.cpp", False),
    ("Caixa de marcar marcada", "ambos", "#FFFFFF", VERDE, "traço", "check_on.svg", False),
    ("Chave ligada (bolinha)", "ambos", "#E6E6E6", VERDE, "traço", "toggle_on.svg / SwitchButton.cpp", False),
    ("Chave ligada no fundo escuro", "escuro", VERDE, ESCURO["painel"], "traço", "SwitchButton.cpp", False),
    ("Botão do menu do topo (hover / aberto)", "ambos", "#FFFFFF", VERDE, "traço", "BBLTopbar.cpp", False),
    ("Seletor Global / Objetos escolhido", "ambos", "#FFFFFF", VERDE, "texto", "SwitchButton.cpp", False),
    ("Ícone com traço amarelo", "escuro", AMARELO, ESCURO["painel"], "traço", "resources/images", False),
    ("Texto em destaque amarelo", "escuro", AMARELO, ESCURO["painel"], "texto", "várias telas", False),
    ("Nome e número da placa", "escuro", "#FFA23A", ESCURO["cena"], "texto", "PartPlate.cpp", False),
    ("Linha da mesa (placa escolhida)", "escuro", "#8E8873", ESCURO["mesa"], "traço", "PartPlate.cpp", False),
    ("Linha da mesa", "escuro", "#A6A08B", ESCURO["mesa"], "traço", "PartPlate.cpp", False),
    ("Texto principal", "claro", CLARO["texto"], CLARO["fundo"], "texto", "StateColor.cpp", False),
    ("Rótulo de parâmetro", "claro", CLARO["texto-2"], CLARO["fundo"], "texto", "StateColor.cpp", False),
    ("Texto apagado", "claro", CLARO["apagado"], CLARO["fundo"], "apagado", "StateColor.cpp", False),
    ("Ícone com traço do acento (âmbar)", "claro", AMBAR, CLARO["fundo"], "traço", "BitmapCache.cpp", False),
    ("Texto em destaque (âmbar)", "claro", AMBAR, CLARO["fundo"], "texto", "StateColor::accentText()", False),
    ("Link nas telas web (âmbar)", "claro", AMBAR, CLARO["fundo"], "texto", "--orca-accent-text", False),
    ("Botões de confirmar em diálogos", "ambos", TINTA_ACENTO, AMARELO, "texto", "SelectMachine.cpp e outros", False),
    ("Caixa de marcar no fundo claro", "claro", VERDE, CLARO["fundo"], "traço", "check_on.svg", False),
]

# trocas que BitmapCache.cpp faz nos SVG no modo escuro
TROCAS_ESCURO = {"#262E30": "#F7F1DC", "#323A3D": "#A6A08B", "#808080": "#8E8873", "#CECECE": "#2A2820",
                 "#6B6B6B": "#8E8873", "#909090": "#FFFFFF", "#F1F1F1": "#1E1D18", "#DBDBDB": "#3A372D",
                 "#F0F0F1": "#1E1D18", "#949494": "#7C8282"}

CSS = """
body { background:#0b0b09; color:#f7f1dc; font:14px/1.45 'Segoe UI', system-ui, sans-serif; margin:24px; }
h1 { margin:0 0 4px; } h2 { margin:32px 0 10px; border-bottom:1px solid #3a372d; padding-bottom:6px; }
.sub { color:#a6a08b; margin:0 0 18px; }
.paleta { display:flex; flex-wrap:wrap; gap:10px; }
.cor { width:120px; border-radius:8px; overflow:hidden; background:#161612; font-size:12px; }
.cor div { height:44px; } .cor span { display:block; padding:6px 8px; }
table { border-collapse:collapse; width:100%; } td, th { padding:7px 10px; border-bottom:1px solid #2a2820; text-align:left; }
th { color:#a6a08b; font-weight:600; }
.amostra { padding:6px 14px; border-radius:6px; font-weight:600; display:inline-block; min-width:150px; }
.ok { color:#2fbf5b; font-weight:700; } .ruim { color:#ff5a4a; font-weight:700; } .pend { color:#ffa23a; font-weight:700; }
.grade { display:grid; grid-template-columns:repeat(auto-fill, minmax(150px, 1fr)); gap:8px; }
.icone { border-radius:8px; overflow:hidden; font-size:11px; background:#161612; }
.icone .par { display:flex; } .icone .par div { flex:1; display:grid; place-items:center; height:52px; }
.icone img { width:28px; height:28px; } .icone span { display:block; padding:4px 6px; color:#a6a08b; word-break:break-all; }
.icone.ruim { outline:2px solid #ff5a4a; }
.resumo { display:flex; gap:12px; flex-wrap:wrap; } .resumo div { background:#161612; border-radius:8px; padding:10px 14px; }
"""


def no_claro(svg):
    for velho, novo in cores.TROCAS_CLARO.items():
        svg = svg.replace(velho, novo).replace(velho.lower(), novo)
    return svg


# CSS: regra com fundo amarelo e texto claro, ou texto amarelo fora do tema escuro
_BLOCO = re.compile(r"([^{}]*)\{([^{}]*)\}")
_FUNDO_AMARELO = re.compile(r"(?i)background(?:-color)?\s*:\s*#FFD21F")
_TEXTO = re.compile(r"(?i)(?<![-\w])color\s*:\s*([^;}]+)")


def problemas_css(raiz):
    achados = []
    web = os.path.join(raiz, "resources", "web")
    arquivos = glob.glob(os.path.join(web, "**", "*.css"), recursive=True) + glob.glob(os.path.join(web, "**", "*.html"), recursive=True)
    for caminho in sorted(arquivos):
        if os.sep + "include" + os.sep in caminho:
            continue
        escuro = os.path.basename(caminho).lower() == "dark.css"
        with open(caminho, encoding="utf-8", errors="replace") as f:
            texto = f.read()
        rel = os.path.relpath(caminho, raiz).replace(os.sep, "/")
        for m in _BLOCO.finditer(texto):
            seletor, corpo = m.group(1).strip().splitlines()[-1:] or [""], m.group(2)
            seletor = seletor[0].strip()
            t = _TEXTO.search(corpo)
            cor_texto = cores.normalizar(t.group(1).strip()) if t else None
            if _FUNDO_AMARELO.search(corpo) and cor_texto and cores.claro(cor_texto):
                achados.append((rel, seletor, f"texto {cor_texto} sobre fundo amarelo"))
            if not escuro and cor_texto in cores.AMARELOS:
                achados.append((rel, seletor, "texto amarelo no tema claro"))
    return achados


def svg_uri(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")


def no_escuro(svg):
    for velho, novo in TROCAS_ESCURO.items():
        svg = svg.replace(velho, novo).replace(velho.lower(), novo)
    return svg


def avaliar_pares():
    linhas = []
    for onde, modo, frente, fundo, tipo, arquivo, pendente in PARES:
        razao = cores.contraste(frente, fundo)
        passa = razao >= MINIMO[tipo]
        linhas.append(dict(onde=onde, modo=modo, frente=frente, fundo=fundo, tipo=tipo, arquivo=arquivo,
                           razao=razao, passa=passa, pendente=pendente))
    return linhas


def ler_icones(raiz):
    icones = []
    for caminho in sorted(glob.glob(os.path.join(raiz, "resources", "images", "*.svg"))):
        with open(caminho, encoding="utf-8", errors="replace") as f:
            svg = f.read()
        cs = {c for _, c in cores.pinturas(svg)}
        if not cs & (cores.AMARELOS | {VERDE, cores.VERDE_HOVER, cores.VERDE_PRESSIONADO}):
            continue
        icones.append(dict(nome=os.path.basename(caminho), svg=svg, ruim=cores.amarelo_sob_branco(svg)))
    return icones


def gerar_html(pares, icones, css):
    e = html.escape
    ruins_par = [p for p in pares if not p["passa"] and not p["pendente"]]
    pendentes = [p for p in pares if not p["passa"] and p["pendente"]]
    ruins_ico = [i for i in icones if i["ruim"]]
    partes = [f"<!DOCTYPE html><html lang='pt-BR'><head><meta charset='utf-8'><title>Mostruário de cores — Reggae Slicer</title><style>{CSS}</style></head><body>",
              "<h1>Mostruário de cores do Reggae Slicer</h1>",
              "<p class='sub'>Gerado por <code>scripts/reggae/mostruario.py</code>. Contraste mínimo: texto 4,5:1; traço de ícone e texto apagado 3:1.</p>",
              "<div class='resumo'>",
              f"<div><b>{len(pares) - len(ruins_par) - len(pendentes)}</b> pares aprovados</div>",
              f"<div class='{'ruim' if ruins_par else 'ok'}'><b>{len(ruins_par)}</b> pares reprovados</div>",
              f"<div class='pend'><b>{len(pendentes)}</b> pendentes conhecidos</div>",
              f"<div class='{'ruim' if ruins_ico else 'ok'}'><b>{len(ruins_ico)}</b> ícones com amarelo sob branco</div>",
              f"<div class='{'ruim' if css else 'ok'}'><b>{len(css)}</b> regras CSS reprovadas</div>",
              f"<div><b>{len(icones)}</b> ícones com as cores do acento</div></div>",
              "<h2>Paleta</h2><div class='paleta'>"]
    paleta = [("Amarelo (acento)", AMARELO), ("Texto sobre o amarelo", TINTA_ACENTO), ("Verde (marcar, ligar, escolhido)", VERDE),
              ("Verde do arco", cores.VERDE_ARCO), ("Vermelho", cores.VERMELHO)]
    paleta += [(f"Escuro: {k}", v) for k, v in ESCURO.items()] + [(f"Claro: {k}", v) for k, v in CLARO.items()]
    for nome, cor in paleta:
        partes.append(f"<div class='cor'><div style='background:{cor}'></div><span>{e(nome)}<br><code>{cor}</code></span></div>")
    partes.append("</div>")

    partes.append("<h2>Pares desenhados no código</h2><table><tr><th>Amostra</th><th>Onde</th><th>Modo</th><th>Tipo</th><th>Contraste</th><th>Arquivo</th></tr>")
    for p in sorted(pares, key=lambda p: (p["passa"], p["modo"])):
        if p["passa"]:
            selo = f"<span class='ok'>{p['razao']:.2f}:1 ✓</span>"
        elif p["pendente"]:
            selo = f"<span class='pend'>{p['razao']:.2f}:1 pendente</span>"
        else:
            selo = f"<span class='ruim'>{p['razao']:.2f}:1 ✗</span>"
        amostra = "Texto de exemplo" if p["tipo"] != "traço" else "✓ ━━ ●"
        partes.append(f"<tr><td><span class='amostra' style='color:{p['frente']};background:{p['fundo']}'>{amostra}</span></td>"
                      f"<td>{e(p['onde'])}</td><td>{p['modo']}</td><td>{p['tipo']}</td><td>{selo}</td><td><code>{e(p['arquivo'])}</code></td></tr>")
    partes.append("</table>")

    def grade(lista):
        out = ["<div class='grade'>"]
        for i in lista:
            out.append(f"<div class='icone{' ruim' if i['ruim'] else ''}'><div class='par'>"
                       f"<div style='background:{ESCURO['painel']}'><img src='{svg_uri(no_escuro(i['svg']))}'></div>"
                       f"<div style='background:{CLARO['fundo']}'><img src='{svg_uri(no_claro(i['svg']))}'></div></div>"
                       f"<span>{e(i['nome'])}</span></div>")
        out.append("</div>")
        return out

    partes.append("<h2>Telas web (CSS): amarelo com texto claro ou texto amarelo no tema claro (reprovados)</h2>")
    if css:
        partes.append("<table><tr><th>Arquivo</th><th>Regra</th><th>Problema</th></tr>")
        partes += [f"<tr><td><code>{e(a)}</code></td><td><code>{e(s)}</code></td><td class='ruim'>{e(p)}</td></tr>" for a, s, p in css]
        partes.append("</table>")
    else:
        partes.append("<p class='ok'>Nenhum.</p>")
    partes.append("<h2>Ícones com amarelo sob branco (reprovados)</h2>")
    partes += grade(ruins_ico) if ruins_ico else ["<p class='ok'>Nenhum.</p>"]
    partes.append("<h2>Todos os ícones com as cores do acento</h2><p class='sub'>À esquerda, no modo escuro; à direita, no claro.</p>")
    partes += grade(icones)
    partes.append("</body></html>")
    return "\n".join(partes), ruins_par, pendentes, ruins_ico


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--raiz", default=".")
    ap.add_argument("--saida", default="mostruario-cores.html")
    ap.add_argument("--verificar", action="store_true", help="sai com erro se algum par ou ícone reprovar")
    a = ap.parse_args()
    pares = avaliar_pares()
    icones = ler_icones(a.raiz)
    css = problemas_css(a.raiz)
    pagina, ruins_par, pendentes, ruins_ico = gerar_html(pares, icones, css)
    with open(a.saida, "w", encoding="utf-8") as f:
        f.write(pagina)
    print(f"{a.saida}: {len(pares)} pares ({len(ruins_par)} reprovados, {len(pendentes)} pendentes), "
          f"{len(icones)} ícones ({len(ruins_ico)} com amarelo sob branco), {len(css)} regras CSS reprovadas")
    for p in ruins_par:
        print(f"  REPROVADO {p['onde']} ({p['modo']}): {p['frente']} sobre {p['fundo']} = {p['razao']:.2f}:1")
    for i in ruins_ico:
        print(f"  REPROVADO ícone {i['nome']}")
    for arq, sel, prob in css:
        print(f"  REPROVADO {arq} {sel}: {prob}")
    if a.verificar and (ruins_par or ruins_ico or css):
        sys.exit(1)


if __name__ == "__main__":
    main()
