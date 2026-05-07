---
tipo: portal
titulo: "Arquitetura de Computadores - Aula 09 (Consolidado)"
disciplina: "Arquitetura de Computadores"
semestre: "2026.1"
data: 2026-05-06
professor: "Thyago"
---

Esta sessão de Arquitetura de Computadores focou na gestão de infraestruturas Windows, explorando a transição de ambientes descentralizados para o controle corporativo via domínios. O Professor Thyago detalhou como a escolha entre **Workgroups** e **Active Directory** impacta diretamente o esforço administrativo e a segurança da rede.

---

## 1. Ambientes de Rede: Workgroup vs. Domínio
A escolha da estrutura de rede define como as identidades e recursos são gerenciados no ecossistema Windows.

- **Workgroup (Grupo de Trabalho):** Um modelo de administração descentralizada. 
    - **Soberania Local:** Cada computador possui seu próprio banco de dados de usuários e senhas (SAM).
    - **Esforço Administrativo:** Se um usuário precisa acessar dez máquinas, a conta deve ser criada manualmente em cada uma delas. 
    - **Cenário:** Adequado apenas para redes com menos de 10-15 dispositivos onde não há necessidade de controle central.
- **Domínio (Active Directory):** Um modelo de administração centralizada.
    - **Single Sign-On (SSO):** O usuário possui uma única credencial que permite acesso a qualquer computador ou recurso da rede (desde que autorizado).
    - **Escalabilidade:** Ideal para redes corporativas, facilitando a gestão de milhares de usuários a partir de um único ponto.

---

## 2. Papéis e Estrutura no Domínio
O gerenciamento via domínio introduz papéis específicos para os servidores, garantindo redundância e especialização de serviços.

- **DC (Domain Controller):** O servidor central que armazena a base de dados do Active Directory. Ele é responsável por autenticar usuários e aplicar políticas globais.
- **Servidor Membro (Member Server):** Servidores que fazem parte da estrutura do domínio mas não autenticam usuários. Eles hospedam serviços específicos, como Servidores de Arquivos, Impressão ou Bancos de Dados, utilizando a segurança centralizada do AD.
- **Replicação de DCs:** Em arquiteturas com múltiplos controladores de domínio, os dados são sincronizados automaticamente. Embora o padrão de replicação possa levar até 3 horas, o processo pode ser forçado para atualização instantânea em casos críticos.

---

## 3. Governança via Políticas (GPOs)
O domínio permite a implementação de **GPOs (Group Policy Objects)**, que são regras aplicadas a computadores ou usuários.

- **Hierarquia:** Organização através de Unidades Organizacionais (OUs), permitindo que diferentes setores (ex: Financeiro, TI) tenham restrições distintas.
- **Controle de Ambiente:** Através das GPOs, o administrador pode bloquear o acesso ao painel de controle, gerenciar atualizações de software e configurar mapeamentos de rede de forma automática para todos os usuários do setor.

---

## 4. Hardware e Investimento
Foi reforçada a necessidade de utilizar hardware homologado (Dell, HP, IBM) para ambientes de produção. 

- **Confiabilidade:** O uso de servidores profissionais (como modelos de Torre ou Rack) garante redundância de fontes, controladoras RAID nativas e suporte técnico especializado, diferenciando-se de máquinas montadas para uso doméstico.
- **Regras de Trabalho:** O professor aproveitou para reforçar as diretrizes das entregas finais, focando na documentação técnica e na qualidade das apresentações em vídeo.

---

## Glossário Técnico
- **Workgroup:** Grupo de computadores em uma rede local que compartilham recursos sem um controle central.
- **Active Directory (AD):** Serviço de diretório da Microsoft para gestão centralizada de usuários e recursos.
- **Domain Controller (DC):** Servidor responsável pela autenticação e gestão do banco de dados do domínio.
- **SSO (Single Sign-On):** Tecnologia que permite acesso a múltiplos sistemas com uma única autenticação.
- **GPO (Group Policy Object):** Regras de configuração centralizada aplicadas a usuários e computadores em um domínio.
- **Servidor Membro:** Servidor integrado ao domínio que fornece serviços específicos (arquivos, banco de dados).
- **Replicação:** Sincronização de dados entre diferentes controladores de domínio para garantir consistência.
