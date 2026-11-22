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
| Abas do alto: fundo `#0B0B09`, texto creme; aba ativa amarela com texto e ícone escuros (`#1C1500`) | `src/slic3r/GUI/Notebook.cpp`, `resources/images/tab_*_active_on_accent.svg` |
| Exibir > Modo escuro (troca na hora, sem abrir as Preferências) e Exibir > Fundo claro na cena 3D (fundo creme `#E6E1D1` no modo escuro, para peças escuras) | `GUI_App.cpp/.hpp` (`switch_color_mode`), `MainFrame.cpp`, `GLCanvas3D.cpp`, `Preferences.cpp`, `AppConfig.cpp` (`reggae_light_scene_background`), tradução em `localization/i18n/pt_BR` |

A cor padrão de filamento novo (`#26A69A` em `PresetBundle.cpp`) foi mantida: é dado de projeto, não cor da interface.

## Ao puxar uma versão nova do OrcaSlicer

1. Mesclar a tag nova no `reggae`.
2. Rodar `python3 scripts/reggae/paleta.py` na raiz (troca o que vier novo com a cor antiga).
3. Procurar sobras: `grep -rn -i "009688\|0, 150, 136" src resources/web resources/images`.
