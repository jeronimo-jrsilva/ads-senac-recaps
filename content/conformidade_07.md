---
tipo: portal
titulo: "Análise de Conformidade - Aula 07"
disciplina: "Análise de Conformidade de Software"
semestre: "2026.1"
data: 2026-04-30
professor: "Tibério"
---

A sétima sessão de Análise de Conformidade marcou o início de um novo ciclo sob a orientação do Professor Tibério. A aula foi uma imersão teórica e prática sobre a governança de TI, os modelos de serviço em nuvem e a responsabilidade jurídica e ética no tratamento de dados, estabelecendo o nexo entre o código desenvolvido e as exigências normativas do mercado.

---

## 1. Governança e Carreira em TI
O professor Tibério, com background em Engenharia e Segurança Cibernética, apresentou um panorama das carreiras modernas. Enfatizou que hoje o profissional de TI não é apenas suporte técnico, mas um pilar estratégico do negócio.

- **Valor da Certificação**: Discutiu-se como certificações (AWS, Azure, ISO 27001) muitas vezes possuem peso equivalente ou superior à graduação em processos seletivos de alta performance, especialmente para profissionais que recebem por hora de consultoria.
- **Regras de Negócio**: O software deve refletir as necessidades da organização. Ignorar o contexto do negócio (ex: hospital vs startup financeira) resulta em sistemas tecnicamente funcionais, mas processualmente nulos.

---

## 2. Computação em Nuvem e Disponibilidade
Expandindo o tema de Arquitetura, a aula abordou a nuvem sob a ótica da conformidade e escalabilidade.

- **Elasticidade**: O exemplo do Magazine Luiza na Black Friday serviu para ilustrar a vantagem de serviços como AWS: a capacidade de suportar picos de acesso sem a necessidade de manter hardware ocioso e caro durante o resto do ano.
- **Modelos de Entrega**:
    - **IaaS**: Responsabilidade total do cliente sobre o SO e segurança.
    - **PaaS**: Abstração da infraestrutura, foco no desenvolvimento de software.
    - **SaaS**: Aplicação como serviço final.

---

## 3. Segurança Cibernética e LGPD
Um ponto de debate intenso foi a distinção entre dados importantes e dados sensíveis conforme a Lei Geral de Proteção de Dados (LGPD).

- **Dados Sensíveis**: São aqueles que podem gerar discriminação (origem racial, convicção religiosa, dados de saúde, orientação sexual).
- **O Caso do CPF**: O professor gerou uma reflexão importante: embora o CPF seja o dado mais crítico para fraudes e acesso bancário, ele não é classificado juridicamente como "sensível" pela LGPD, mas sim como um dado pessoal identificável.
- **Mitigação de Riscos**: A máxima da segurança é: "Você será atacado". A diferença reside no seu plano de resposta (Plano A, B e C), incluindo backups offline e protocolos de isolamento.

---

## 4. Engenharia de Software e Qualidade: DevOps e SRE
A conformidade também se aplica ao ciclo de vida do desenvolvimento.

- **DevOps**: Integração entre o pessoal de infraestrutura (que preza pela estabilidade) e o desenvolvimento (que busca inovação). O foco é automação total de deploys via Kubernetes e Jenkins.
- **Observabilidade**: Uso de ferramentas como **Prometheus** (coleta de dados) e **Grafana** (visualização) para monitoramento contínuo da saúde dos sistemas.
- **Documentação Imemorável**: O professor defendeu a cultura da documentação bem feita, citando o exemplo do Arch Linux, onde a qualidade do manual define a qualidade do sistema.

---

## 5. Práticas de Desenvolvimento Seguro
- **SQL Injection**: Exemplo da invasão de banco de dados via placas de veículos no Detran (comando `DROP DATABASE` inserido no campo de texto).
- **Test-Driven Development (TDD)**: A prática de escrever o teste antes do código para garantir que a saída atenda aos requisitos desde o primeiro minuto.
- **Política de Código**: Exemplo de empresas que exigem funções curtas (ex: 25 linhas) para garantir a legibilidade em monitores padrão, facilitando a auditoria.

---

## Glossário Técnico
- **LGPD**: Lei Geral de Proteção de Dados (Lei 13.709/2018).
- **Elasticidade**: Capacidade da nuvem de aumentar ou diminuir recursos conforme a demanda.
- **DevOps**: Cultura de colaboração entre Desenvolvimento e Operações.
- **SRE (Site Reliability Engineering)**: Engenharia focada na confiabilidade e escalabilidade de sites.
- **SQL Injection**: Técnica de ataque que insere comandos maliciosos em campos de entrada de formulários.
- **Prometheus**: Ferramenta de monitoramento e alerta de código aberto.
- **Kubernetes**: Orquestrador de containers para automação de implantação e escala.
