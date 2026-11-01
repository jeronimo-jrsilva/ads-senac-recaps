# Ecossistema Soberano de Gestão do Conhecimento Acadêmico, Ingestão Multimodal de Aulas e Democratização Educacional (ADS Senac Recaps)

**Autor:** Jeronimo Silva  
**Instituição:** Faculdade de Tecnologia SENAC Ceará  
**Curso:** Superior de Tecnologia em Análise e Desenvolvimento de Sistemas  
**Disciplina:** Projeto Integrador 3 (PI 3) — Prof. Thyago Aquino  
**Semestre:** 2026.2  

---

### Abstract
This project presents an open-source, sovereign academic knowledge management ecosystem designed to mitigate educational drop-out and cognitive overload in higher education technology programs (Computer Science and Software Engineering). Addressing the acute friction faced by working students in reviewing dense technical lectures (covering Object-Oriented Programming, C systems programming, and Relational Database Systems), the platform introduces an end-to-end processing pipeline: (1) an on-premise multimodal audio ingestion pipeline powered by local GPU-accelerated Whisper models; (2) a normalized relational database schema implemented in SQLite; (3) an administrative curation cockpit built on Python/Django with Object-Relational Mapping (ORM); and (4) a zero-cost static site generator exporting single-page responsive portals hosted directly on GitHub Pages. Directly aligned with the United Nations Sustainable Development Goal 4 (Quality Education), the solution provides structured class notes, semantic timelines, and automated domain glossaries without reliance on proprietary cloud APIs.

### Resumo
Este trabalho apresenta a proposta do ecossistema soberano de gestão do conhecimento acadêmico e acessibilidade pedagógica voltado para a retenção e nivelamento de estudantes de graduação em tecnologia (Análise e Desenvolvimento de Sistemas). Enfrentando o gargalo crítico de retenção cognitiva vivenciado por alunos trabalhadores que lidam simultaneamente com disciplinas de alta densidade técnica (Programação Orientada a Objetos em Java, Linguagem C de baixo nível e Modelagem Relacional em Banco de Dados), o sistema implementa uma esteira completa de engenharia de software composta por: (1) pipeline de ingestão e transcrição local com aceleração de hardware em GPU dedicada (Whisper ROCm); (2) persistência relacional normalizada em SQLite; (3) cockpit administrativo de curadoria e gestão desenvolvido em Python/Django com Mapeamento Objeto-Relacional (ORM); e (4) compilador de distribuição estática de alta performance com custo operacional zero publicado no GitHub Pages. Alinhado de forma estrita ao Objetivo de Desenvolvimento Sustentável nº 4 da ONU (Educação de Qualidade), o projeto entrega resumos estruturados por semanas letivas, trilhas cronológicas por docente e glossário técnico hiperlinkado.

---

## 1. Tipo da Atividade
( x ) Projeto de Desenvolvimento de Software / Projeto Integrador de Extensão Tecnológica (PI 3)

## 2. Tema do Projeto
Engenharia de software aplicada à educação aberta e gestão do conhecimento: automação de esteiras de processamento de fala para texto (Whisper GPU), arquitetura relacional de persistência (SQLite), desenvolvimento de cockpit web com ORM (Django) e geração de portais estáticos de alto desempenho para democratização do ensino superior.

## 3. Título Oficial do Trabalho
**Ecossistema Soberano de Gestão do Conhecimento Acadêmico, Ingestão Multimodal de Aulas e Democratização Educacional (ADS Senac Recaps).**

## 4. Identificação Institucional
- **4.1 Coordenação de Curso:** Coordenação do Eixo de Tecnologia da Informação — Faculdade SENAC Ceará (Prof. Me. Frederico Costa).
- **4.2 Professor Orientador / Gestor de Projetos:** Prof. Thyago Aquino.
- **4.3 Alinhamento de Disciplinas Conexas:**
  - *Banco de Dados Relacional:* Prof. Alexandre — Modelagem DER, normalização e consultas SQL.
  - *Programação Orientada a Objetos:* Prof. Tibério — Mapeamento Objeto-Relacional (ORM) e entidades de domínio.
  - *Linguagem C:* Prof. Vinícius / Prof. Matheus — Otimização de compiladores e estruturas de dados.
- **4.4 Semestre Letivo:** 2026.2.

---

## 5. Justificativa & Alinhamento com a Agenda 2030 da ONU

### 5.1 O Problema Real
O perfil predominante do discente em graduações tecnológicas noturnas e semipresenciais é composto por profissionais que trabalham em regime integral. A grade curricular do 2º semestre reúne simultaneamente linguagens com diferentes paradigmas (Java corporativo e C procedural) e abstrações de modelagem relacional. A perda eventual de uma única aula presencial (por plantões de trabalho, compromissos familiares ou saúde) gera uma quebra em cascata na compreensão do semestre, levando à desmotivação e ao abandono do curso. Reouvir gravações de áudio de 2 a 3 horas é inviável na rotina cotidiana do estudante trabalhador.

### 5.2 Alinhamento com o ODS 4 da ONU (Educação de Qualidade)
O projeto atende de forma direta às seguintes metas da **Agenda 2030 da Organização das Nações Unidas (ONU)**:
- **Meta 4.3:** Assegurar a igualdade de acesso para todos os homens e mulheres à educação técnica, profissional e superior de qualidade.
- **Meta 4.4:** Aumentar substancialmente o número de jovens e adultos que tenham habilidades relevantes, inclusive competências técnicas e profissionais, para emprego e empreendedorismo.
- **Inclusão & Acessibilidade:** Estudantes com dificuldades auditivas ou em ambientes ruidosos de transporte público passam a ter acesso integral ao conteúdo expositivo dos professores em formato textual estruturado com diagramas e blocos de código legíveis.

---

## 6. Objetivos

### 6.1 Objetivo Geral
Conceber, modelar e construir a arquitetura completa do ecossistema de gestão pedagógica **ADS Senac Recaps**, integrando uma esteira soberana de inteligência artificial para extração de fala, um banco de dados relacional em SQLite, um cockpit web em Django para curadoria e um exportador de site estático gratuito hospedado no GitHub Pages.

### 6.2 Objetivos Específicos
- Desenvolver pipeline em Python com processamento de fala acelerado por hardware GPU (AMD Radeon RX 7600 via ROCm) para transcrição rápida de áudios brutos de 2 horas em menos de 5 minutos.
- Modelar e implementar o schema relacional em SQLite com integridade referencial estrita entre Disciplinas, Professores, Semanas Letivas, Aulas, Segmentos de Transcrição e Termos de Glossário.
- Desenvolver um cockpit administrativo web utilizando o framework Python/Django, permitindo o gerenciamento visual dos registros acadêmicos e curadoria de notas através do Django Admin.
- Criar comando customizado de automação (`python manage.py build_portal`) para leitura dos dados persistidos via ORM e compilação do portal estático em Single Page Application (SPA).
- Publicar e manter a plataforma operacional com custo de infraestrutura zero através do GitHub Pages, oferecendo visualização responsiva, navegação cronológica e modo escuro para smartphones e desktops.

---

## 7. Arquitetura da Solução & Engenharia Técnica

A arquitetura do projeto adota o princípio da **Soberania Tecnológica**, operando localmente na máquina do desenvolvedor sem dependência de serviços pagos de terceiros, e distribuindo o resultado final na nuvem pública gratuita:

```
[ Gravação de Áudio no Tablet (.m4a) ]
                  │
                  ▼
[ Esteira Local: Whisper ROCm GPU (whisper.cpp) ]
                  │
                  ▼ (Segmentos de Texto + Timestamps)
[ Banco de Dados Relacional: SQLite (recap_senac.db) ]
                  ▲
                  │  (ORM / Mapeamento Objeto-Relacional)
[ Cockpit Administrativo Web: Python/Django (/admin) ]
                  │
                  ▼  (Comando: python manage.py build_portal)
[ Compilador Estático: HTML5 / Modern CSS / Vanilla JS ]
                  │
                  ▼  (git push)
[ Deploy em Nuvem: GitHub Pages (Acesso Universal para a Turma) ]
```

---

## 8. Delimitação de Escopo (Gestão de Projetos)

### 8.1 Escopo do Produto (Entregáveis Finais)
1. **Portal Web Acadêmico (SPA):** Interface pública responsiva, indexada por 12 semanas letivas, trilhas por docente, linha do tempo interativa e glossário conceitual unificado.
2. **Banco de Dados SQLite (`recap_senac.db`):** Modelo relacional com 6 entidades normalizadas persistindo todo o histórico do semestre 2026.2.
3. **Cockpit Django:** Aplicação web local com autenticação, painel administrativo e interface de curadoria via ORM.
4. **Pipeline Automatizado de Ingestão:** Scripts de conversão de áudio e transcrição via GPU dedicada.

### 8.2 Escopo do Projeto (Trabalho de Engenharia)
- Modelagem conceitual (MER) e lógica (DER) das entidades de domínio.
- Criação dos scripts de carga de dados históricos (ETL das Semanas 01 a 12).
- Configuração de testes de integridade referencial e validação de chaves estrangeiras.
- Validação de usabilidade do portal junto a colegas da turma de ADS.
- Elaboração dos relatórios e slides de defesa para banca do Projeto Integrador.

---

## 9. Mapeamento de Stakeholders

| Stakeholder | Papel no Projeto | Interesse / Valor Agregado |
| :--- | :--- | :--- |
| **Estudantes de ADS (Usuário Primário)** | Consumidor do conteúdo | Acesso rápido a resumos estruturados de aulas perdidas, códigos-fonte comentados e preparação para provas (AV1/AV2). |
| **Professores das Disciplinas** | Fontes do conhecimento | Garantia de que suas diretrizes metodológicas e conceitos centrais estão documentados com fidelidade pedagógica. |
| **Prof. Thyago Aquino (Avaliador PI3)** | Gerente de Projetos / Banca | Rigor metodológico de escopo, documentação técnica, aplicação prática de banco de dados e entrega de software funcional. |
| **Comunidade Acadêmica Externa** | Beneficiário de Extensão | Disponibilização de material didático aberto de alta qualidade para estudantes autodidatas de computação. |

---

## 10. Cronograma de Sprints e Marcos (2026.2)

- **Sprint 1 (Agosto):** Definição do escopo, levantamento de requisitos e estrutura de coleta de áudios brutos. *(Concluído)*
- **Sprint 2 (Setembro):** Criação dos primeiros protótipos de portal estático e estruturação das Semanas 01 a 06. *(Concluído)*
- **Sprint 3 (Outubro):** Aceleração de hardware com ROCm GPU, consolidação das Semanas 07 a 12 e unificação de disciplinas. *(Concluído)*
- **Sprint 4 (Novembro - Em Execução):** Migração para arquitetura relacional SQLite e desenvolvimento do Cockpit Django.
- **Sprint 5 (Dezembro):** Defesa pública da solução funcional na banca de Projeto Integrador 3 perante o Prof. Thyago Aquino.
