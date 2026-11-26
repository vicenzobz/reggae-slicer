# Reggae Slicer

Fork pessoal do [OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer) para a Anycubic Kobra X, com a paleta e a ligação ao [Selecta 3D](https://github.com/vicenzobz/selecta-3d) (programa local de fila, estoque e impressões, que antes se chamava Organizador 3D). Licença AGPL-3.0, a mesma do OrcaSlicer. O que o programa é e como usar estão no [README](README.md); aqui ficam as mudanças no código.

- Versão: Reggae Slicer 4.20 (`REGGAE_VERSION` 4.20.1.0.0 em `version.inc`), sobre o OrcaSlicer 2.5.2.
- Ramo de trabalho: `reggae`, criado a partir da tag `v2.5.2` do OrcaSlicer (`f92a7c0`). O `main` acompanha o OrcaSlicer original.
- Compilação: `.github/workflows/reggae_windows.yml` gera só o Windows x64 a cada push no `reggae`; o portátil fica nos artefatos da execução. As versões publicadas ficam em [Releases](https://github.com/vicenzobz/reggae-slicer/releases), com o zip portátil da compilação daquele commit (veja [Publicar uma versão](#publicar-uma-versão)).

## Mudanças em relação ao OrcaSlicer

| Mudança | Onde |
|---|---|
| Workflow só de Windows x64 | `.github/workflows/reggae_windows.yml` |
| Paleta do Selecta 3D: acento ouro `#F0B41C` (no lugar do `#009688`), texto escuro `#1A140C` sobre o ouro, fundos cor de madeira (`#15110C`, `#1E1811`, `#292117`, `#33291C`), textos cor de papel (`#F2E6C9`, `#DDCFAF`, `#A8997B`), musgo `#4D7C2A` e vermelho `#CF2E1F` | `scripts/reggae/paleta.py` (troca o verde-azulado do Orca pela paleta reggae da primeira versão) e `scripts/reggae/paleta_selecta.py` (troca essa paleta pela do Selecta 3D), automáticos em `src/` e `resources/`, + ajustes à mão em `StateColor.cpp`, `BitmapCache.cpp`, `Button.cpp`, `SideButton.cpp`, `SwitchButton.cpp`, `WebViewHostDialog.cpp`, `CalibrationWizardPage.cpp`, `ImGuiWrapper.cpp`, `GLCanvas3D.cpp`, `dark_mode.cpp` e CSS das telas web |
| Modo escuro como padrão | `src/libslic3r/AppConfig.cpp` |
| Logo do arco na mesa da Kobra X (quadrado vazado com os cantos do retângulo da Anycubic, abaixo do símbolo de mesa quente) | `resources/profiles/Anycubic/Anycubic Kobra X_buildplate_texture.svg`, versão do `Anycubic.json` |
| Abas do alto: fundo `#15110C`, texto cor de papel; aba ativa musgo `#4D7C2A` com texto e ícone brancos | `src/slic3r/GUI/Notebook.cpp` |
| Musgo `#4D7C2A` (hover `#588C31`, pressionado `#436E24`) em tudo que tem traço branco e era ouro: caixa de marcar, chaves ligar/desligar, seletor Global/Objetos, botões do menu do topo, ícones (61 SVG) | `scripts/reggae/verde_sob_branco.py`, `Widgets/SwitchButton.cpp`, `BBLTopbar.cpp`, `resources/images/*.svg` |
| Modo claro: linhas e textos do acento em âmbar `#7D5800` (o ouro some no branco). Ícones: troca no `BitmapCache.cpp` (o ouro que é fundo de desenho escuro usa `#F0B41D` e não é trocado); textos: `StateColor::accentText()`; telas web: `--orca-accent-text` e regras âmbar com o ouro de volta nos `dark.css` | `BitmapCache.cpp`, `Widgets/StateColor.cpp/.hpp`, `Widgets/WebViewHostDialog.cpp`, 16 telas com texto amarelo, `scripts/reggae/amarelo_no_claro.py`, `resources/web/**/*.css` |
| Texto escuro `#1A140C` nos botões ouro de diálogos que tinham texto branco | `SelectMachine.cpp`, `SelectMachinePop.cpp`, `PrintOptionsDialog.cpp`, `MultiTaskManagerPage.cpp`, `ReleaseNote.cpp` |
| Linhas da mesa mais claras no modo escuro (`#A8997B`, placa escolhida `#8F8268`) | `PartPlate.cpp` |
| Nome Reggae Slicer e marca do arco: ícones, abertura e Sobre com os mesmos nomes de arquivo; título da janela e descrição do executável. A pasta de dados e o produtor do G-code continuam OrcaSlicer, para configurações, perfis e a impressora seguirem funcionando | `scripts/reggae/gerar_marca.py`, `scripts/reggae/marca/`, `resources/images/OrcaSlicer*`, `splash_logo*.svg`, `Plater.cpp`, `MainFrame.cpp`, `OrcaSlicer.rc.in` |
| Página inicial com uma seção Selecta 3D: fila (abrir o arquivo da peça), projetos ativos e estoque, lidos de `%LOCALAPPDATA%\\Organizador3D\\reggae-slicer.json`, que o Selecta 3D grava (a pasta manteve o nome antigo); login e nuvens escondidos | `resources/web/homepage/js/organizador.js`, `css/organizador.css`, `index.html`, `WebViewDialog.cpp` (`SendOrganizador`), `GUI_App.cpp` (`reggae_get_organizador`, `reggae_open_file`) |
| Sem conta e sem nuvem por padrão: modo furtivo e painel de login escondido em configurações novas | `src/libslic3r/AppConfig.cpp` |
| Pasta de dados: se existir `dados-orca` ao lado da pasta do programa (`REGGAE-SLICER\\dados-orca`), é ela; assim o programa aberto direto e a aba do Selecta 3D usam as mesmas configurações e filamentos | `src/slic3r/GUI/GUI_App.cpp` |
| Escolher um filamento do usuário (como os do estoque do Selecta 3D) leva a cor dele para o quadradinho do slot, pela `default_filament_colour` do perfil; filamentos do sistema mantêm a cor do slot como no Orca | `src/slic3r/GUI/PresetComboBoxes.cpp` (`update_ams_color`) |
| Sem a aba Projeto (informações de modelo do 3MF, estilo MakerWorld): os projetos ficam no Selecta 3D e aparecem na página inicial | `src/slic3r/GUI/MainFrame.cpp` |
| Abertura sem a linha de versão do OrcaSlicer (saía por cima do logo); no lugar dela, a versão curta do Reggae Slicer em ouro depois de "slicer". Ouro da marca escura em `#F0B41D`, que o BitmapCache não troca por âmbar | `GUI_App.cpp`, `scripts/reggae/gerar_marca.py` |
| Imagens PNG com o verde-azulado do Orca passadas para o musgo (assistente inicial, umidade do AMS, ilustrações) e logo das telas web com o arco | `resources/web/image/logo*.png`, `resources/web/guide/11/*.png`, `resources/images/humidity_list_background.png`, `dev_ams_dry_ctr_filament_in_chamber.png`, `resources/web/model/img/null*.png` |
| Mostruário de cores: página com toda a paleta, os pares de cor do código com o contraste WCAG e os ícones do acento nos dois modos; `--verificar` reprova contraste baixo e ouro sob branco, e roda no workflow antes da compilação | `scripts/reggae/mostruario.py`, `scripts/reggae/cores.py`, `.github/workflows/reggae_windows.yml` |
| Cena 3D no modo escuro com as cores da prévia 3D do Selecta 3D: fundo `#15110C`, mesa `#3E3324`, barra de ferramentas `#33291C`, sem os cinzas azulados do Orca | `GLCanvas3D.cpp`, `3DBed.cpp`, `PartPlate.cpp`, `ImGuiWrapper.cpp`, `resources/images/toolbar_background_dark.png`, `resources/images/plate_*_dark.svg` |
| Botões Fatiar/Exportar: `SetForegroundColour` não troca mais as cores do texto por estado (a passada do modo escuro punha `#E0E0E0` em todas as janelas e o texto saía claro sobre o ouro) | `src/slic3r/GUI/Widgets/SideButton.cpp` |
| Exibir > Modo escuro (troca na hora, sem abrir as Preferências) e Exibir > Fundo claro na cena 3D (fundo creme `#E9DFC5` no modo escuro, para peças escuras) | `GUI_App.cpp/.hpp` (`switch_color_mode`), `MainFrame.cpp`, `GLCanvas3D.cpp`, `Preferences.cpp`, `AppConfig.cpp` (`reggae_light_scene_background`), tradução em `localization/i18n/pt_BR` |
| Versão própria 4.20 (`REGGAE_VERSION`): título da janela, Sobre (com o OrcaSlicer 2.5.2 na linha do build), abertura, versão mostrada pelo programa, propriedades do .exe e nome do zip. `SoftFever_VERSION` 2.5.2 e `SLIC3R_VERSION` continuam nos 3MF, perfis e G-code, para a compatibilidade | `version.inc`, `src/libslic3r/libslic3r_version.h.in`, `AboutDialog.cpp`, `GUI_App.cpp`, `Plater.cpp`, `OrcaSlicer.rc.in`, `.github/workflows/build_orca.yml` |
| Executável `reggae-slicer.exe` no Windows (até a 4.20 com `orca-slicer.exe`): alvo do CMake, recurso do .exe, abrir nova janela, plugin de rede, instaladores NSIS e MSIX | `CMakeLists.txt`, `src/CMakeLists.txt`, `OrcaSlicer.rc.in`, `src/slic3r/Utils/Process.cpp`, `src/slic3r/Utils/BBLNetworkPlugin.cpp`, `scripts/msix/` |
| README do Reggae Slicer com a apresentação; o do OrcaSlicer ficou em `README_OrcaSlicer.md` | `README.md`, `README_OrcaSlicer.md`, `reggae-apresentacao/` |

A cor padrão de filamento novo (`#26A69A` em `PresetBundle.cpp`) foi mantida: é dado de projeto, não cor da interface.

## Ao puxar uma versão nova do OrcaSlicer

1. Mesclar a tag nova no `reggae`.
2. Rodar na raiz, nesta ordem (troca o que vier novo com a cor antiga; os dois últimos procuram o ouro do Selecta 3D, então vêm depois do `paleta_selecta.py`):
   `python3 scripts/reggae/paleta.py`, `python3 scripts/reggae/paleta_selecta.py`, `python3 scripts/reggae/verde_sob_branco.py` e `python3 scripts/reggae/amarelo_no_claro.py`.
   Conferir com `python3 scripts/reggae/mostruario.py --verificar`.
3. Procurar sobras: `grep -rn -i "009688\|0, 150, 136\|FFD21F\|1D7F3A" src resources/web resources/images`.

## Publicar uma versão

1. Subir `REGGAE_VERSION` em `version.inc` e esperar a compilação do **Reggae Slicer - Windows** passar. Testar o zip dos artefatos.
2. Criar em Releases um rascunho com a etiqueta nova (ex.: `v4.20`) apontando para o commit compilado.
3. Rodar à mão o **Reggae Slicer - publicar versão** (`.github/workflows/reggae_publicar.yml`) com o número da execução e a etiqueta: ele anexa ao rascunho o mesmo zip portátil que foi testado, sem compilar de novo. Depois, publicar o rascunho.

| Versão | Commit | Base |
|---|---|---|
| 4.20 (4.20.1.0.0) | `edf0378e` | OrcaSlicer 2.5.2 |
