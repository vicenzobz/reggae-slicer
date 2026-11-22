# Reggae Slicer

Fork pessoal do [OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer) para a Anycubic Kobra X, com a paleta reggae e integrado ao Organizador 3D (programa local de fila, estoque e impressões). Licença AGPL-3.0, a mesma do OrcaSlicer.

- Ramo de trabalho: `reggae`, criado a partir da tag `v2.5.2` do OrcaSlicer (`f92a7c0`). O `main` acompanha o OrcaSlicer original.
- Compilação: `.github/workflows/reggae_windows.yml` gera só o Windows x64 a cada push no `reggae`; o portátil fica nos artefatos da execução.

## Mudanças em relação ao OrcaSlicer

| Mudança | Onde |
|---|---|
| Workflow só de Windows x64 | `.github/workflows/reggae_windows.yml` |
| Paleta reggae: acento amarelo `#FFD21F` (no lugar do `#009688`), texto escuro `#1C1500` sobre o amarelo, fundos escuros do Organizador (`#0B0B09`, `#161612`, `#1E1D18`, `#2A2820`), textos creme (`#F7F1DC`, `#DDD7C3`, `#A6A08B`), laranja `#FFA23A` e vermelho `#FF5A4A` | `scripts/reggae/paleta.py` (troca automática em `src/` e `resources/`) + ajustes à mão em `StateColor.cpp`, `BitmapCache.cpp`, `Button.cpp`, `SideButton.cpp`, `SwitchButton.cpp`, `WebViewHostDialog.cpp`, `CalibrationWizardPage.cpp`, `ImGuiWrapper.cpp`, `GLCanvas3D.cpp`, `dark_mode.cpp` e CSS das telas web |
| Modo escuro como padrão | `src/libslic3r/AppConfig.cpp` |
| Logo do arco na mesa da Kobra X (quadrado vazado com os cantos do retângulo da Anycubic, abaixo do símbolo de mesa quente) | `resources/profiles/Anycubic/Anycubic Kobra X_buildplate_texture.svg`, versão do `Anycubic.json` |
| Abas do alto: fundo `#0B0B09`, texto creme; aba ativa verde `#1D7F3A` com texto e ícone brancos | `src/slic3r/GUI/Notebook.cpp` |
| Verde `#1D7F3A` (hover `#23913F`, pressionado `#1A7535`) em tudo que tem traço branco e era amarelo: caixa de marcar, chaves ligar/desligar, seletor Global/Objetos, botões do menu do topo, ícones (61 SVG) | `scripts/reggae/verde_sob_branco.py`, `Widgets/SwitchButton.cpp`, `BBLTopbar.cpp`, `resources/images/*.svg` |
| Modo claro: linhas e textos do acento em âmbar `#806300` (o amarelo some no branco). Ícones: troca no `BitmapCache.cpp` (o amarelo que é fundo de desenho escuro usa `#FFD220` e não é trocado); textos: `StateColor::accentText()`; telas web: `--orca-accent-text` e regras âmbar com o amarelo de volta nos `dark.css` | `BitmapCache.cpp`, `Widgets/StateColor.cpp/.hpp`, `Widgets/WebViewHostDialog.cpp`, 16 telas com texto amarelo, `scripts/reggae/amarelo_no_claro.py`, `resources/web/**/*.css` |
| Texto escuro `#1C1500` nos botões amarelos de diálogos que tinham texto branco | `SelectMachine.cpp`, `SelectMachinePop.cpp`, `PrintOptionsDialog.cpp`, `MultiTaskManagerPage.cpp`, `ReleaseNote.cpp` |
| Linhas da mesa mais claras no modo escuro (`#A6A08B`, placa escolhida `#8E8873`) | `PartPlate.cpp` |
| Mostruário de cores: página com toda a paleta, os pares de cor do código com o contraste WCAG e os ícones do acento nos dois modos; `--verificar` reprova contraste baixo e amarelo sob branco, e roda no workflow antes da compilação | `scripts/reggae/mostruario.py`, `scripts/reggae/cores.py`, `.github/workflows/reggae_windows.yml` |
| Cena 3D no modo escuro com as cores da prévia 3D do Organizador: fundo `#14140F`, mesa `#3A382A`, barra de ferramentas `#2A2820`, sem os cinzas azulados do Orca | `GLCanvas3D.cpp`, `3DBed.cpp`, `PartPlate.cpp`, `ImGuiWrapper.cpp`, `resources/images/toolbar_background_dark.png`, `resources/images/plate_*_dark.svg` |
| Botões Fatiar/Exportar: texto desenhado no mesmo DC do fundo (no Windows saía cinza-claro `#E0E0E0` sobre o amarelo em vez do `#1C1500`) | `src/slic3r/GUI/Widgets/SideButton.cpp` |
| Exibir > Modo escuro (troca na hora, sem abrir as Preferências) e Exibir > Fundo claro na cena 3D (fundo creme `#E6E1D1` no modo escuro, para peças escuras) | `GUI_App.cpp/.hpp` (`switch_color_mode`), `MainFrame.cpp`, `GLCanvas3D.cpp`, `Preferences.cpp`, `AppConfig.cpp` (`reggae_light_scene_background`), tradução em `localization/i18n/pt_BR` |

A cor padrão de filamento novo (`#26A69A` em `PresetBundle.cpp`) foi mantida: é dado de projeto, não cor da interface.

## Ao puxar uma versão nova do OrcaSlicer

1. Mesclar a tag nova no `reggae`.
2. Rodar `python3 scripts/reggae/paleta.py`, `python3 scripts/reggae/verde_sob_branco.py` e `python3 scripts/reggae/amarelo_no_claro.py` na raiz (troca o que vier novo com a cor antiga).
   Conferir com `python3 scripts/reggae/mostruario.py --verificar`.
3. Procurar sobras: `grep -rn -i "009688\|0, 150, 136" src resources/web resources/images`.
