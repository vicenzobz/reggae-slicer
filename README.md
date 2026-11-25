<p align="center"><img alt="Reggae Slicer 4.20" src="reggae-apresentacao/banner.png" width="100%"></p>

# Reggae Slicer 4.20

**Fork do [OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer) feito para uma Anycubic Kobra X de 4 cores, com a paleta reggae e integrado ao [Selecta 3D](https://github.com/vicenzobz/selecta-3d).**

*A fork of OrcaSlicer for a 4-colour Anycubic Kobra X, with a reggae palette and a link to the Selecta 3D print organizer. Portuguese (Brazil) first.*

> [!IMPORTANT]
> **Projeto pessoal, compartilhado para testes e como referência para outros projetos.** Eu não dou suporte a quem for usar: issues e pedidos podem ficar sem resposta. Para adaptar à sua impressora ou à sua rotina, use um agente de IA como o **[Claude Code](https://claude.com/claude-code)** ou o **[Codex](https://openai.com/codex)**: aponte o agente para este repositório e peça as mudanças que quiser. É assim que este fork é feito.

## Como é

| | |
|---|---|
| <img src="reggae-apresentacao/abertura.png" width="360" alt="Abertura"> | **Abertura** com o arco nas cores do reggae e a versão 4.20. |
| <img src="reggae-apresentacao/preparar.png" alt="Preparar"> | **Preparar** no modo escuro com a paleta do Selecta 3D: fundos cor de madeira, texto cor de papel, ouro nos botões e o logo do arco na mesa da Kobra X. Os filamentos do estoque aparecem como perfis prontos (cor, marca, temperatura e preço). |

![Página inicial](reggae-apresentacao/inicio.png)

**Página inicial** com o Selecta 3D: as próximas peças da fila (o botão **Abrir** carrega o arquivo da peça), os projetos ativos e o estoque de filamentos:

![Estoque](reggae-apresentacao/estoque.png)

## O que é

O Reggae Slicer é o OrcaSlicer 2.5.2 com mudanças pequenas e localizadas. O fatiamento, os perfis e os arquivos são os do OrcaSlicer: um 3MF salvo aqui abre no OrcaSlicer e no Anycubic Slicer Next, e vice-versa. O que muda é a cara do programa e a ligação com o Selecta 3D, o organizador de impressão 3D do mesmo autor.

| | |
|---|---|
| **Base** | OrcaSlicer 2.5.2 (versão interna; aparece no Sobre) |
| **Versão** | 4.20 (4.20.1.0.0 completa) |
| **Impressora** | Anycubic Kobra X (perfis oficiais que já vêm no OrcaSlicer) |
| **Sistema** | Windows x64 (só este é compilado) |
| **Executável** | `reggae-slicer.exe` (compilações antigas: `orca-slicer.exe`) |
| **Licença** | AGPL-3.0, a mesma do OrcaSlicer (`LICENSE.txt`) |

## O que muda em relação ao OrcaSlicer

**Visual**
- Paleta do Selecta 3D: ouro `#F0B41C`, musgo `#4D7C2A`, vermelho `#CF2E1F`, fundos cor de madeira e texto cor de papel; cena 3D e mesa no mesmo tom.
- Modo escuro por padrão; **Exibir → Modo escuro** troca na hora, e **Exibir → Fundo claro** clareia só a cena 3D (para peças escuras).
- Logo do arco na abertura (com "4.20"), nos ícones e na mesa da Kobra X.
- Contraste conferido: o script `scripts/reggae/mostruario.py` roda antes de cada compilação e barra a compilação se algum par de cores ficar ilegível.

**Uso**
- **Página inicial com o Selecta 3D:** próximas peças da fila, projetos ativos e estoque, lidos do arquivo `%LOCALAPPDATA%\Organizador3D\reggae-slicer.json` que o Selecta 3D grava (funciona com o Selecta 3D fechado).
- **Filamentos do estoque como perfis:** cada cor de PLA do estoque vira um filamento com cor, marca, temperatura e preço; escolher um deles leva a cor para o slot.
- **Sem conta e sem nuvem por padrão** (modo furtivo); login e nuvens escondidos na página inicial.
- Aba "Projeto" (informações do modelo do 3MF) retirada.

## Como baixar

Não há página de versões. Cada push no ramo `reggae` compila o Windows x64 no GitHub Actions (workflow **Reggae Slicer - Windows**, ~45–70 min):

1. Abra a aba **Actions** e a última execução verde de **Reggae Slicer - Windows**.
2. Em **Artifacts**, baixe `ReggaeSlicer_4.20_Windows_x64_portable` (precisa estar logado no GitHub).
3. Extraia e abra `reggae-slicer.exe`. É portátil: não instala nada. O Windows pode avisar que o programa não é assinado ("Mais informações → Executar assim mesmo").

Sozinho, ele funciona como um OrcaSlicer com outra cara: as configurações ficam no AppData, como no Orca.

## Como ligar ao Selecta 3D

A aba **Reggae Slicer** do Selecta 3D mostra estes passos com o caminho certo da sua pasta.

1. Extraia o zip em `<pasta de dados do Selecta 3D>\PROGRAMAS\REGGAE-SLICER\reggae-slicer` (por padrão, `Documentos\Selecta 3D\...`), com o `reggae-slicer.exe` direto nela.
2. No Selecta 3D, aba **Reggae Slicer → Procurar de novo**. O Selecta 3D cria a pasta `dados-orca` ao lado do programa; o Reggae Slicer guarda as configurações nela.
3. Abra o Reggae Slicer pela aba e escolha a Kobra X. Em alguns segundos os filamentos do estoque aparecem como perfis, e a página inicial mostra a fila.

A partir daí o Selecta 3D fatia as peças da fila por linha de comando (com os perfis da Kobra X que vêm com ele) e guarda a estimativa de gramas por cor, tempo e custo. O OrcaSlicer oficial portátil também funciona no lugar do Reggae Slicer, em `...\REGGAE-SLICER\orca-oficial`.

## Ramos

| Ramo | Para quê |
|---|---|
| `reggae` | o que é compilado (padrão deste repositório) |
| `reggae-proximo` | mudanças guardadas para a próxima compilação (não compila sozinho) |
| `main` | cópia do OrcaSlicer, sem as mudanças do Reggae Slicer |

Para achar as mudanças no código, procure por `Reggae Slicer` nos comentários. A versão mostrada fica em `version.inc` (`REGGAE_VERSION`); a do OrcaSlicer (`SoftFever_VERSION`) não muda, porque vai dentro dos 3MF e dos perfis.

## Créditos

Tudo o que importa no fatiamento é do **[OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer)** e de quem veio antes dele (Slic3r, PrusaSlicer, Bambu Studio, SuperSlicer). O README original do OrcaSlicer está em [`README_OrcaSlicer.md`](README_OrcaSlicer.md). Este fork não tem ligação com a Anycubic nem com a equipe do OrcaSlicer; "Kobra X" e "Anycubic" são marcas da Anycubic.
