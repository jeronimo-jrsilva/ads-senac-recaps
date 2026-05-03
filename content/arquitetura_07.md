---
tipo: portal
titulo: "Arquitetura de Computadores - Aula 07"
disciplina: "Arquitetura de Computadores"
semestre: "2026.1"
data: 2026-04-22
professor: "Thyago"
---

A décima terceira sessão de Arquitetura de Computadores consolidou a unificação oficial das turmas do primeiro semestre e aprofundou o estudo sobre Virtualização e Computação em Nuvem. O Professor Thyago nivelou o conhecimento técnico dos grupos, revisou a política de avaliações e explorou a anatomia dos Hypervisors, estabelecendo as bases para o entendimento de infraestruturas modernas e escaláveis.

---

## 1. Unificação e Alinhamento Pedagógico
A aula marcou a integração definitiva das turmas 1 e 2 de ADS. O início foi dedicado à revisão da avaliação AV1, onde o professor identificou disparidades no nível de dificuldade cobrado anteriormente.

- **Bônus Institucional**: Devido à complexidade desbalanceada da prova em relação ao conteúdo visto por um dos grupos, foi concedido 1 ponto extra para todos os alunos na AV1.
- **Composição de Nota**: A segunda parte da nota será composta por um trabalho prático valendo 9.0 pontos, focado na aplicação dos conceitos de hardware e virtualização.
- **Unificação de Cronograma**: As sessões agora seguem um roteiro único para todo o semestre, garantindo que ambos os grupos tenham acesso ao mesmo rigor técnico.

---

## 2. Níveis de Virtualização: Hypervisors Tipo 1 e 2
O centro técnico da aula foi a diferenciação entre as camadas de abstração de hardware. Virtualizar não é apenas rodar um sistema dentro de outro, mas gerenciar recursos físicos de forma eficiente.

- **Hypervisor Tipo 1 (Bare Metal)**: O virtualizador é o próprio "sistema operacional" que roda diretamente sobre o hardware. É uma camada finíssima que entrega performance máxima.
    - **Exemplos**: VMWare ESXi, Microsoft Hyper-V (versão servidor), Citrix Xen.
    - **Uso**: Ambientes corporativos críticos, data centers e servidores de produção.
- **Hypervisor Tipo 2 (Hosted)**: O virtualizador roda como uma aplicação dentro de um Sistema Operacional convencional (como Windows, Linux ou Mac).
    - **Exemplos**: Oracle VirtualBox, VMWare Workstation.
    - **Uso**: Ambientes de estudo, testes de desenvolvedores e uso doméstico.
- **A Abstração do Ferro**: O Hypervisor cria drivers virtuais genéricos. Isso permite que uma Máquina Virtual seja migrada entre hardwares fisicamente distintos (ex: mover do processador Intel para AMD ou de um servidor Dell para HP) sem que o sistema operacional dentro da VM perceba a mudança ou exija reconfiguração.

---

## 3. Virtualização Total vs. Containers (Docker)
Um debate técnico aprofundado diferenciou a virtualização de hardware (VMs) da virtualização de sistema operacional (Containers).

- **Máquinas Virtuais (VMs)**: Cada VM possui seu próprio Kernel e sistema operacional completo. Isso garante isolamento total e segurança, mas consome significativamente mais recursos (memória, processamento e disco).
- **Containers (Docker)**: Não possuem um Kernel próprio. Eles compartilham o Kernel do sistema hospedeiro (Host) e isolam apenas as bibliotecas e a aplicação. 
    - **Performance**: Um container inicia em milissegundos, enquanto uma VM leva minutos.
    - **Tecnologias de Suporte**: O isolamento no Linux é garantido via C-groups (gerenciamento de hardware) e Namespaces (isolamento lógico de processos e rede).

---

## 4. Modelos de Serviço em Nuvem e Disponibilidade
A aula expandiu os conceitos de virtualização para o cenário da Cloud Computing, discutindo como grandes empresas como AWS, Azure e Google entregam infraestrutura.

- **Modelos de Serviço**:
    - **IaaS (Infraestrutura como Serviço)**: Aluguel do hardware bruto virtualizado (CPU, RAM, Storage).
    - **PaaS (Plataforma como Serviço)**: O provedor entrega o ambiente de execução e banco de dados pronto para o código do desenvolvedor.
    - **SaaS (Software como Serviço)**: O usuário consome a aplicação final via navegador (ex: Gmail, Office 365).
- **Disponibilidade e Redundância**:
    - **Hot-Swap**: Capacidade de trocar discos ou memórias com o servidor em funcionamento, garantindo que o sistema não pare durante manutenções.
    - **Clusters e Redundância**: Uso de múltiplos servidores físicos agindo como um só para suportar picos de demanda ou falhas de hardware.
    - **Discussão User-End**: Debate sobre serviços de jogos como Xbox Live e GeForce Now, que operam em modelos híbridos onde o processamento pesado (GPU) ocorre na nuvem e o usuário recebe apenas a transmissão (streaming).

---

## Glossário
- **Hypervisor**: Software que gerencia a criação e execução de máquinas virtuais (VMM).
- **Kernel**: Núcleo do sistema operacional que gerencia a comunicação entre software e hardware.
- **Hot-Swap**: Tecnologia que permite a substituição de componentes de hardware sem desligar o sistema.
- **On-Premises**: Infraestrutura de TI instalada localmente nas dependências da organização.
- **Snapshot**: Captura do estado exato de uma máquina virtual em um ponto no tempo para recuperação futura.
- **Bare Metal**: Hardware físico sem sistema operacional instalado previamente.
- **C-groups**: Recurso do Linux usado pelo Docker para limitar o uso de recursos físicos.
- **Namespaces**: Recurso do Linux que isola o que um processo pode "ver" (rede, arquivos, usuários).
