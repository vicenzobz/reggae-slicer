"""Gera a marca do Reggae Slicer (ícones, logo da abertura e do Sobre) a partir de marca/icone_arco_v05.svg.

Sobrescreve os arquivos de resources/images que levam a marca do OrcaSlicer, mantendo os nomes
(o código continua procurando "OrcaSlicer.ico", "splash_logo.svg" etc.). O texto vira caminho
vetorial (o nanosvg do programa não desenha <text>), com a fonte Inter, a mesma do Selecta 3D.

Precisa de: Python com fontTools, rsvg-convert e ImageMagick (convert), e as fontes Inter instaladas.
Os arquivos gerados vão para o repositório; a compilação não roda este script.

    python3 scripts/reggae/gerar_marca.py
"""
import os
import re
import subprocess
import tempfile

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
IMAGENS = os.path.join(RAIZ, "resources", "images")
FONTES = ["/usr/share/fonts/opentype/inter", os.path.expanduser("~/.fonts"), "C:/Windows/Fonts"]

# AMARELO_FIXO: igual ao amarelo a olho nu, mas fora da troca por âmbar que o BitmapCache faz no modo claro.
# A abertura é desenhada antes de o programa saber o modo, então a troca pegava o "reggae" da versão escura.
AMARELO, AMARELO_FIXO, AMBAR, CREME, TINTA = "#F0B41C", "#F0B41D", "#7D5800", "#F2E6C9", "#262E30"

with open(os.path.join(AQUI, "marca", "icone_arco_v05.svg"), encoding="utf-8") as f:
    ICONE = f.read()
DEFS = re.search(r"<defs>.*?</defs>", ICONE, re.S).group(0)
ARCO = re.search(r"<g transform=.*?</g>", ICONE, re.S).group(0)  # arco em 0..512


def fonte(nome):
    for pasta in FONTES:
        caminho = os.path.join(pasta, nome)
        if os.path.exists(caminho):
            return TTFont(caminho)
    raise SystemExit(f"fonte {nome} não encontrada")


def texto(t, arquivo_fonte, tamanho, x, y, cor, espaco=0.0):
    """Texto como <path>; (x, y) é o início da linha de base."""
    f = fonte(arquivo_fonte)
    escala = tamanho / f["head"].unitsPerEm
    cmap, glifos, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    caminhos, cursor = [], 0.0
    for ch in t:
        nome = cmap[ord(ch)]
        caneta = SVGPathPen(glifos)
        glifos[nome].draw(TransformPen(caneta, (escala, 0, 0, -escala, x + cursor, y)))
        caminhos.append(caneta.getCommands())
        cursor += hmtx[nome][0] * escala + espaco
    return f'<path d="{" ".join(caminhos)}" fill="{cor}"/>', cursor


def arco(x, y, lado):
    """O arco ocupando um quadrado de `lado` px com canto em (x, y)."""
    s = lado / 512
    return f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.5f})">{ARCO}</g>'


def svg(largura, altura, corpo):
    # data-reggae-marca: o texto amarelo e o creme ficam lado a lado, não um sobre o outro;
    # verde_sob_branco.py e o mostruário pulam estes arquivos.
    return (f'<svg xmlns="http://www.w3.org/2000/svg" data-reggae-marca="1" width="{largura}" height="{altura}" '
            f'viewBox="0 0 {largura} {altura}">{DEFS}{corpo}</svg>\n')


def escrever(nome, conteudo):
    with open(os.path.join(IMAGENS, nome), "w", encoding="utf-8", newline="\n") as f:
        f.write(conteudo)


def abertura(cor_texto, destaque):
    # 480 x 480: arco em cima, "reggae" e "slicer" embaixo, centralizados
    corpo = arco(150, 40, 180)
    _, l1 = texto("reggae", "Inter-Bold.otf", 92, 0, 0, cor_texto, -2)
    p1, _ = texto("reggae", "Inter-Bold.otf", 92, (480 - l1) / 2, 330, destaque, -2)
    _, l2 = texto("slicer", "Inter-Light.otf", 64, 0, 0, cor_texto, 6)
    p2, _ = texto("slicer", "Inter-Light.otf", 64, (480 - l2) / 2, 400, cor_texto, 6)
    return svg(480, 480, corpo + p1 + p2)


def sobre(cor_texto, destaque):
    # 560 x 125 (o amarelo de destaque vira âmbar no tema claro): arco à esquerda, nome e "baseado no OrcaSlicer" (licença AGPL) à direita
    corpo = arco(10, 12, 100)
    p1, _ = texto("Reggae Slicer", "Inter-Bold.otf", 46, 130, 66, destaque)
    p2, _ = texto("baseado no OrcaSlicer", "Inter-Regular.otf", 20, 132, 98, cor_texto)
    faixa = ('<rect x="130" y="112" width="140" height="4" fill="#CF2E1F"/>'
             '<rect x="270" y="112" width="140" height="4" fill="#F0B41D"/>'
             '<rect x="410" y="112" width="140" height="4" fill="#8DBA63"/>')
    return svg(560, 125, corpo + p1 + p2 + faixa)


def horizontal(cor_texto, destaque):
    # 214 x 80: arco e nome em duas linhas
    corpo = arco(4, 8, 64)
    p1, _ = texto("reggae", "Inter-Bold.otf", 30, 78, 38, destaque)
    p2, _ = texto("slicer", "Inter-Light.otf", 24, 79, 64, cor_texto, 2)
    return svg(214, 80, corpo + p1 + p2)


def png(svg_texto, lado, destino, fundo=None, cinza=False):
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as t:
        t.write(svg_texto)
    args = ["rsvg-convert", "-w", str(lado), "-h", str(lado), t.name, "-o", destino]
    if fundo:
        args[1:1] = ["-b", fundo]
    subprocess.run(args, check=True)
    if cinza:
        subprocess.run(["convert", destino, "-colorspace", "Gray", destino], check=True)
    os.unlink(t.name)


def main():
    icone = svg(64, 64, arco(0, 0, 64))
    escrever("OrcaSlicer.svg", icone)
    for nome in ("OrcaSlicer_gradient.svg", "OrcaSlicer_gradient_circle.svg", "OrcaSlicer_gradient_narrow.svg"):
        escrever(nome, icone)
    escrever("OrcaSlicer_gray.svg", icone.replace("url(#reggae)", "#9E9E9E"))
    escrever("splash_logo.svg", abertura(TINTA, AMBAR))
    escrever("splash_logo_dark.svg", abertura(CREME, AMARELO_FIXO))
    escrever("OrcaSlicer_about.svg", sobre(TINTA, AMBAR))
    escrever("OrcaSlicer_about_dark.svg", sobre(CREME, AMARELO_FIXO))
    escrever("OrcaSlicer_horizontal_light.svg", horizontal(TINTA, AMBAR))
    escrever("OrcaSlicer_horizontal_dark.svg", horizontal(CREME, AMARELO_FIXO))

    grande = svg(512, 512, arco(0, 0, 512))
    for nome, lado in (("OrcaSlicer.png", 256), ("OrcaSlicer_32px.png", 32), ("OrcaSlicer_64.png", 64),
                       ("OrcaSlicer_128px.png", 128), ("OrcaSlicer_154.png", 154), ("OrcaSlicer_192px.png", 192),
                       ("OrcaSlicer_192px_transparent.png", 192), ("OrcaSlicer-mac_128px.png", 128),
                       ("OrcaSlicerTitle.png", 64), ("OrcaSlicer_154_title.png", 154)):
        png(grande, lado, os.path.join(IMAGENS, nome))
    png(grande, 192, os.path.join(IMAGENS, "OrcaSlicer_192px_grayscale.png"), cinza=True)

    with tempfile.TemporaryDirectory() as tmp:
        tamanhos = (16, 20, 24, 32, 40, 48, 64, 128, 256)
        pngs = []
        for lado in tamanhos:
            destino = os.path.join(tmp, f"{lado}.png")
            png(grande, lado, destino)
            pngs.append(destino)
        for nome in ("OrcaSlicer.ico", "OrcaSlicerTitle.ico", "OrcaSlicer-mac_256px.ico"):
            subprocess.run(["convert", *pngs, os.path.join(IMAGENS, nome)], check=True)
    print("marca do Reggae Slicer gerada em resources/images")


if __name__ == "__main__":
    main()
