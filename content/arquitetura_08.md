---
tipo: portal
titulo: "Arquitetura de Computadores - Aula 08"
disciplina: "Arquitetura de Computadores"
semestre: "2026.1"
data: 2026-04-29
professor: "Thyago"
---

A oitava sessão de Arquitetura de Computadores mergulhou na camada física da comunicação de dados, explorando o hardware de conectorização, a hierarquia de switches e os fundamentos de infraestrutura de rede que sustentam os ambientes de virtualização vistos anteriormente. O Professor Thyago enfatizou que o desempenho de servidores e bancos de dados é diretamente limitado pela qualidade e topologia do cabeamento estruturado.

---

## 1. Camada Física e Meios de Transmissão
A aula iniciou com o detalhamento dos componentes que compõem o canal físico por onde os elétrons (dados) trafegam.

- **Cabo UTP (Unshielded Twisted Pair)**: O padrão azul comum, cujos pares são trançados para mitigar o efeito de *crosstalk* (interferência eletromagnética entre fios adjacentes).
- **Conectorização**: Diferenciação entre RJ45 (dados) e RJ11 (voz/telefonia).
- **Velocidades Nominais**: Evolução da Ethernet de 10 Mbps e 100 Mbps (Fast Ethernet) para o padrão atual de 1 Gbps (Gigabit Ethernet) e superiores.

---

## 2. A Evolução do Hardware de Interconexão: Hub vs. Switch
O professor explicou por que o Hub foi descontinuado em favor do Switch, focando na inteligência do hardware.

- **Hub (O "Burro")**: Não possui memória. Ele replica o sinal recebido para todas as portas (*broadcast* indiscriminado), causando colisões e gargalos severos de throughput.
- **Switch (O "Inteligente")**: Possui memória interna e capacidade de aprendizado. Ele constrói uma tabela baseada no **Endereço MAC** (endereço físico de 12 dígitos hexadecimais), permitindo comunicações *unicast* (diretas de origem para destino) e eliminando colisões de pacotes.

---

## 3. Cabeamento Estruturado: Patch Panels e Keystones
Para ambientes profissionais como Data Centers (Amazon, Microsoft, Bancos), a organização física é um requisito de conformidade.

- **Keystone**: A tomada fêmea de rede instalada na parede.
- **Patch Panel**: Painel centralizador no rack que organiza os cabos vindos das tomadas. Ele permite a manobra rápida de pontos sem danificar os cabos permanentes.
- **Manobra de Rede**: O uso de cabos curtos (*patch cords*) ligando o Patch Panel ao Switch. Sem o Patch Panel, os cabos ficariam soltos, sujeitos a danos físicos e dificultando a identificação de falhas em redes escaláveis.

---

## 4. Hierarquia de Switches e Performance
A infraestrutura de TI corporativa é dividida em camadas para evitar o travamento (*crash*) do hardware sob alta carga:

- **Switches de Acesso**: Onde se conectam os desktops, notebooks e access points. São dispositivos de entrada com pouca memória de processamento.
- **Switches de Distribuição**: Intermediam o tráfego entre as salas ou andares.
- **Switches de Core (Núcleo)**: Equipamentos robustos (Layer 3), muitas vezes com fontes redundantes e capacidade de roteamento, que sustentam o tráfego pesado de servidores e armazenamento (*Storage*).

> [!example] Crash por Memória
> O professor relatou um caso real onde um switch Gigabit de entrada travou ao tentar transmitir simultaneamente imagens de Windows (10 para 10 máquinas). A falha não foi a velocidade da porta, mas a incapacidade da memória do hardware de gerenciar o volume massivo de quadros.

---

## 5. Modos de Comunicação e Sinais
- **Simplex**: Transmissão em apenas um sentido (ex: rádio FM).
- **Half-Duplex**: Transmissão e recepção alternadas (ex: rádio-comunicadores/walkie-talkie).
- **Full-Duplex**: Transmissão e recepção simultâneas, padrão nos switches modernos.
- **Multicast**: Sinal direcionado a um grupo específico de máquinas (ex: comunicação interna de um cluster de servidores).

---

## Glossário Técnico
- **Crosstalk**: Interferência de sinal causada pela proximidade de fios.
- **Endereço MAC**: Identificador físico global e único gravado na placa de rede.
- **Throughput**: Velocidade real de entrega de dados em uma rede.
- **Patch Panel**: Equipamento passivo de organização de cabos em racks.
- **Keystone**: Módulo conector utilizado em espelhos de parede ou caixas de sobrepor.
- **Full-Duplex**: Capacidade de um canal de enviar e receber dados simultaneamente.
- **Access Point (AP)**: Dispositivo que converte sinal de rede cabeada em sinal wireless (Wi-Fi).
- **Rede Mesh**: Tecnologia de expansão de sinal Wi-Fi onde os APs formam uma malha inteligente de cobertura.
