# 🎯 Recaps SENAC: Project Mandates

## 🛡️ Fonte Única da Verdade (SSOT)
- **Motor de Build:** O motor oficial é `90_Sistema/98_Recursos/03_Scripts/motor_portal_ads.py` (v4.2.x+).
- **Localização da Infra:** A infraestrutura de scripts foi migrada da pasta `~/scripts/ads-recaps` para dentro da Vault (`MultiPurpose`).
- **Arquitetura:** O portal utiliza o modelo **Dashboard Unificado** (`portal/Recap_Master_S1.html`). Não gerar mais arquivos individuais por semana.

## 🛠️ Workflow de Diagnóstico
1. **Sempre** verificar o `git status` do repositório antes de assumir pendências.
2. **Sempre** rodar o motor oficial da Vault para validar se o arquivo local está em sincronia com o SSOT.
3. **Ignorar** scripts em `~/scripts/ads-recaps/` (considerados LEGADO).

## 🚀 Publicação
- O deploy deve ser feito na branch `master`.
- A Landing Page (`index.html`) deve apontar para `./portal/Recap_Master_S1.html`.
