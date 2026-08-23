---
name: ads-recap-curator
description: "Fluxo de curadoria, refinamento de transcrições, padronização e compilação dos portais acadêmicos de ADS SENAC (2026.1 e 2026.2)."
---

# 🎓 ADS Recap Curator — Instruções de Execução

Esta skill guia o agente no processamento completo de novas aulas, transcrições e manutenção dos portais de ADS SENAC.

## 📋 Regras de Formatação de Aula (`.md`)

1. **Frontmatter Padrão:**
   ```markdown
   ---
   tipo: portal
   titulo: "Disciplina - Aula XX (Tema da Aula)"
   disciplina: "Nome da Disciplina"
   semestre: "2026.2"
   data: YYYY-MM-DD
   professor: "Nome do Professor"
   ---
   ```

2. **Espaçamento de Listas:**
   - Sempre incluir uma linha em branco antes do início da lista e uma linha em branco após o término da lista inteira.

3. **Proibição de Metadados de Auditoria:**
   - Nunca incluir blocos de auditoria/caixa preta (`> [!abstract]- 📦 CAIXA PRETA...`) no arquivo da aula.

4. **Seção de Glossário Obrigatória:**
   ```markdown
   ## Glossário
   - **Termo**: Definição clara e objetiva do conceito. [Wikipedia](https://pt.wikipedia.org/wiki/Termo).
   ```

---

## ⚙️ Motores de Compilação

- **1º Semestre (2026.1):**
  ```bash
  python3 /home/jeronimo/G-Sync/ads-senac-recaps/engine/master_builder_s1.py
  ```
- **2º Semestre (2026.2):**
  ```bash
  python3 /home/jeronimo/G-Sync/ads-senac-recaps/engine/master_builder_s2.py
  ```

---

## 🌐 Estrutura para Deploy no GitHub Pages

1. A raiz do repositório `/home/jeronimo/G-Sync/ads-senac-recaps/index.html` deve ser mantida atualizada como espelho de `portal/Recap_Master_S2.html` (ou portal principal).
2. Os links relativos no Top App Bar (`Recap_Master_S1.html` e `Recap_Master_S2.html`) permitem navegação fluida em qualquer dispositivo.
3. Para publicar, basta executar:
   ```bash
   git add -A && git commit -m "feat: adicionar aula e atualizar portais" && git push origin master
   ```
