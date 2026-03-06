# 📑 Documento de Requisitos - Portal de Recaps ADS

Este documento descreve as funcionalidades e restrições do Portal de Recaps, focado no suporte ao curso de ADS (2026.1).

## 1. Objetivo do Projeto
O objetivo primário é fornecer uma interface centralizada e otimizada para o consumo de resumos técnicos gerados a partir das aulas presenciais, garantindo a preservação da didática e a facilidade de consulta.

## 2. Requisitos Funcionais (RF)

| ID | Requisito | Descrição |
| :--- | :--- | :--- |
| **RF01** | **Hub de Navegação** | O portal deve possuir uma página inicial (index) que liste cronologicamente os resumos semanais disponíveis. |
| **RF02** | **Glossário Transversal** | Cada portal semanal deve conter um glossário consolidado de termos técnicos das disciplinas abordadas. |
| **RF03** | **Links Internos** | Termos técnicos citados no corpo do resumo devem possuir links diretos para suas definições no glossário. |
| **RF04** | **Realce de Sintaxe** | Trechos de código (Python, SQL, etc.) devem ser exibidos com formatação e cores adequadas (Syntax Highlight). |
| **RF05** | **Fidelidade Didática** | Os resumos devem manter analogias, exemplos práticos e referências bibliográficas citadas pelos professores. |

## 3. Requisitos Não-Funcionais (RNF)

| ID | Requisito | Descrição |
| :--- | :--- | :--- |
| **RNF01** | **Responsividade** | A interface deve ser otimizada para dispositivos móveis, tablets e desktops. |
| **RNF02** | **Estética Gold Standard** | O design deve seguir uma paleta de cores sóbria (Dark Mode) com detalhes em dourado, priorizando a legibilidade. |
| **RNF03** | **Disponibilidade** | O acesso deve ser feito via web pública (GitHub Pages) sem necessidade de autenticação. |
| **RNF04** | **Performance** | As páginas devem ser leves (HTML/CSS puro) para carregamento instantâneo. |

## 4. Stakeholders
- **Alunos:** Usuários primários para revisão e estudo.
- **Professores:** Consultores de conteúdo e validação técnica.
- **Desenvolvedor (Jeronimo):** Responsável pela curadoria e engenharia de processamento.

---
*Última atualização: 06/03/2026*
