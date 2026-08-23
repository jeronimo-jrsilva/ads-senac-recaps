import os
import json
import re
from pathlib import Path

REPO_ROOT = Path("/home/jeronimo/G-Sync/ads-senac-recaps")
SEMANAL_DIR = REPO_ROOT / "s2_2026_2/02_semanal"
ESTRUT_DIR = REPO_ROOT / "s2_2026_2/01_estruturadas"

SEMANAL_DIR.mkdir(parents=True, exist_ok=True)
(SEMANAL_DIR / "W_01").mkdir(parents=True, exist_ok=True)
(SEMANAL_DIR / "W_02").mkdir(parents=True, exist_ok=True)
ESTRUT_DIR.mkdir(parents=True, exist_ok=True)

# Limpar arquivos antigos para não sobrar resquícios
for f in (SEMANAL_DIR / "W_01").glob("*.md"): f.unlink()
for f in (SEMANAL_DIR / "W_02").glob("*.md"): f.unlink()
for f in ESTRUT_DIR.glob("*.md"): f.unlink()

# Configurações Oficiais das Semanas
w1_config = {
    "title": "Semana 1: Abertura do Semestre, POO em Java e Fundamentos de C",
    "text": "Início do 2º semestre (2026.2). Alinhamento pedagógico de POO com Prof. Tibério, primeiros passos e modelo de compilação em Linguagem C com Prof. Vinícius e comunicação institucional da coordenação."
}
w2_config = {
    "title": "Semana 2: Projeto Integrador, Prática de POO/C e Projeto de Extensão",
    "text": "Imersão em Projeto Integrador com Prof. Thiago (visão de gerência de projetos), modelagem prática de POO em Java, listas de exercícios e operadores lógicos em C com Prof. Vinícius, mentoria de projetos e Projeto de Extensão aos sábados."
}

with open(SEMANAL_DIR / "W_01/week_config.json", "w", encoding="utf-8") as f:
    json.dump(w1_config, f, ensure_ascii=False, indent=2)

with open(SEMANAL_DIR / "W_02/week_config.json", "w", encoding="utf-8") as f:
    json.dump(w2_config, f, ensure_ascii=False, indent=2)

# Grade Oficial:
# Segunda: Projeto Integrador | Prof. Thiago
# Terça: Programação Orientada a Objetos | Prof. Tibério
# Quarta / Quinta: Linguagem C | Prof. Vinícius
# Sexta: Banco de Dados Relacional | Prof. Alexandre
# Sábado: Projeto de Extensão
# Outros: Comunicações institucionais e alinhamentos gerais

aulas = [
    # SEMANA 1
    {
        "file_sem": SEMANAL_DIR / "W_01/poo_01.md",
        "file_est": ESTRUT_DIR / "2026-08-11_ter_poo.md",
        "raw": "11ago-ter-poo.txt",
        "titulo": "POO - Aula 01: Transição Paradigmática, Avaliação e Histórico de Linguagens",
        "disciplina": "Programação Orientada a Objetos",
        "professor": "Tibério",
        "data": "2026-08-11",
        "dia_semana": "Ter",
        "subtopicos": [
            "Abertura e Transição de Paradigma: Passagem da lógica procedural de Python (1º semestre) para a modelagem orientada a objetos.",
            "Contrato Pedagógico e Opções Avaliativas: Realização de AV1/AV2 ou desenvolvimento de Projeto Prático com Relatório Técnico para quem aprende desenvolvendo.",
            "História do JavaScript e o Caso Gmail: Trajetória do JS no frontend (Netscape) até a virada histórica com o Gmail no Google e posterior migração para backend e MongoDB.",
            "Java e a Filosofia da JVM: A verbosidade estruturada de Java ('Olá Mundo parece uma redação') como garantia de tipagem estática e segurança em sistemas enterprise."
        ],
        "analogias": [
            "Para aprender a programar tem que botar a mão na massa, senão você é igual quem estuda trânsito e mecânica sem nunca sentar no banco do motorista.",
            "O Java assusta no início porque um simples Olá Mundo parece uma redação, mas essa verbosidade protege o sistema em projetos com centenas de desenvolvedores."
        ],
        "sintese": """A aula inaugural de Programação Orientada a Objetos com o professor Tibério começou com o acolhimento da turma e uma reflexão sobre a transição do primeiro para o segundo semestre de ADS: os alunos dominaram a lógica básica procedural em Python e agora ingressam no desenvolvimento corporativo estruturado em Java.

O professor Tibério estabeleceu um contrato pedagógico flexível: os alunos farão provas regulares (AV1 e AV2) com questões baseadas nas listas práticas de sala, mas quem desejar poderá desenvolver um projeto prático com entrega de relatório técnico, valorizando o aprendizado ativo e o perfil de quem aprende melhor desenvolvendo soluções reais.

Em seguida, o professor abriu uma rica discussão sobre a evolução das linguagens de mercado. Explicou a trajetória do JavaScript, que era visto como linguagem secundária de scripts visuais até o momento histórico em que o Google utilizou JavaScript para estruturar a interface interativa do Gmail, transformando-o no ecossistema dominante tanto no frontend quanto no backend com MongoDB. Em contraste, apresentou o Java, destacando que sua rigidez sintática e a execução sobre a JVM (Java Virtual Machine) garantem portabilidade e segurança estática para grandes sistemas corporativos. A aula encerrou com o alinhamento das primeiras práticas no laboratório."""
    },
    {
        "file_sem": SEMANAL_DIR / "W_01/c_01.md",
        "file_est": ESTRUT_DIR / "2026-08-12_qua_c.md",
        "raw": "12ago-qua-c.txt",
        "titulo": "Linguagem C - Aula 01: Memória, Hardware, Compilação e Tipos Primitivos",
        "disciplina": "Linguagem C",
        "professor": "Vinícius",
        "data": "2026-08-12",
        "dia_semana": "Qua",
        "subtopicos": [
            "Conexão entre Código e Hardware: O papel de Linguagem C no controle direto da memória RAM e na base de sistemas operacionais e bancos de dados.",
            "Estrutura Básica de um Programa em C: Função main, diretivas de pré-processamento (#include <stdio.h>) e o código de retorno 0 como sinal de sucesso ao SO.",
            "Tipagem Primitiva e o Operador sizeof: Medição física em bytes de char (1 byte), int (4 bytes), float (4 bytes) e double (8 bytes).",
            "Formatação de Saída com printf: Uso de especificadores (%d, %c, %f, %.2f) e prevenção de falhas de tipos."
        ],
        "analogias": [
            "Em Python você cria uma variável sem saber o que acontece por baixo dos panos; em C você é o dono da memória, escolhendo se vai gastar 1 byte ou 8 bytes da RAM.",
            "O return 0 é a resposta do seu programa para o sistema operacional dizendo: 'Terminei meu trabalho e não explodi nada'."
        ],
        "sintese": """A aula de abertura de Linguagem C com o professor Vinícius focou na aproximação entre o código e a máquina real. Seguindo a metodologia de trabalhar profundamente a base da linguagem na primeira metade do semestre, o professor explicou que em C o desenvolvedor é responsável direto pela representação binária e gestão de memória.

Foi analisada a estrutura canônica de um programa em C: as diretivas de pré-processamento que incluem arquivos de cabeçalho (#include <stdio.h>), a função principal main como ponto de entrada obrigatório da execução e o significado do código de saída return 0.

Na segunda parte da aula, os alunos exploraram os tipos primitivos fundamentais e mediram o espaço ocupado por cada um utilizando o operador sizeof. Foi detalhado como a arquitetura do processador aloca 1 byte para caracteres (char), 4 bytes para inteiros (int) e números reais de precisão simples (float), e 8 bytes para precisão dupla (double). O professor Vinícius realizou demonstrações no terminal com a função printf, ensinando a formatação de saída e prevenindo erros comuns de tipagem."""
    },
    {
        "file_sem": SEMANAL_DIR / "W_01/c_02.md",
        "file_est": ESTRUT_DIR / "2026-08-13_qui_c.md",
        "raw": "13ago-qui-c.txt",
        "titulo": "Linguagem C - Aula 02: Prática em Laboratório, Entrada de Dados e Condicionais",
        "disciplina": "Linguagem C",
        "professor": "Vinícius",
        "data": "2026-08-13",
        "dia_semana": "Qui",
        "subtopicos": [
            "Prática em Laboratório: Abertura do ambiente de compilação GCC e IDEs nos computadores dos alunos.",
            "Entrada de Dados com scanf: Por que o scanf exige o operador & (&variavel) e a introdução ao conceito de endereço físico de memória.",
            "Estruturas Condicionais: Resolução prática de exercícios com if, else if e else para cálculos de média e faixas etárias.",
            "Diagnóstico Coletivo de Erros: Análise de mensagens do compilador para falta de ponto-e-vírgula e leitura de lixo de memória."
        ],
        "analogias": [
            "Quando você passa o & para o scanf, você está dando o endereço da sua casa para a entrega chegar no lugar certo, e não apenas o seu nome.",
            "Ler uma variável não inicializada em C é como abrir uma gaveta em um hotel que não foi limpa: você vai achar o lixo que o programa anterior deixou lá."
        ],
        "sintese": """A segunda aula de Linguagem C com o professor Vinícius foi eminentemente prática, realizada nos computadores do laboratório para consolidar a escrita, compilação e depuração de código em tempo real. O professor orientou os alunos sobre o fluxo de trabalho do GCC no terminal e a organização de arquivos fonte.

O foco central foi o domínio da entrada de dados via scanf. O professor utilizou o comando para introduzir a noção de endereçamento de memória: explicou por que passar apenas o nome da variável causa falhas e por que o operador & (e-comercial) é indispensável para fornecer ao sistema a localização física exata onde o dado digitado pelo usuário deve ser armazenado.

Em seguida, a turma trabalhou na resolução de exercícios práticos envolvendo tomadas de decisão condicionais (if / else). Foram construídos programas para validação de notas acadêmicas, cálculo de faixas etárias e verificações de intervalos numéricos. O professor Vinícius circulou pelas bancadas analisando mensagens de erro do compilador, ensinando os alunos a ler alertas de tipagem e reforçando a disciplina sintática exigida pela linguagem C."""
    },
    {
        "file_sem": SEMANAL_DIR / "W_01/outros_01.md",
        "file_est": ESTRUT_DIR / "2026-08-14_sex_fred.md",
        "raw": "14ago-sex-fred.txt",
        "titulo": "Comunicação Institucional: Quadro Docente CLT e Alinhamento Acadêmico",
        "disciplina": "Outros",
        "professor": "Fred (Coordenação)",
        "data": "2026-08-14",
        "dia_semana": "Sex",
        "subtopicos": [
            "Contratação da Equipe de Tecnologia: Anúncio oficial de 10 professores contratados no regime CLT definitivo para o curso.",
            "Perfil dos Docentes: Todos os professores são atuantes no mercado de TI, garantindo alinhamento com práticas corporativas reais.",
            "Estruturação do Projeto Integrador: Condução do PI com o Professor Thiago e articulação com as matérias técnicas da semana.",
            "Espaço de Escuta: Perguntas e respostas sobre laboratórios, sábados letivos e suporte acadêmico."
        ],
        "analogias": [
            "Hoje nossa equipe de tecnologia conta com 10 professores em peso na casa, contratados via CLT, profissionais do mercado para atender todas as necessidades dos alunos de ADS.",
            "O Projeto Integrador não é uma disciplina isolada; é a espinha dorsal onde vocês colocam em prática o que estão vendo durante a semana inteira."
        ],
        "sintese": """Na sexta-feira, o coordenador Fred esteve presente em sala para realizar uma comunicação institucional e de alinhamento com os alunos de Análise e Desenvolvimento de Sistemas. O objetivo principal foi apresentar as diretrizes operacionais e as melhorias implementadas para o semestre 2026.2.

O ponto alto da fala de Fred foi o anúncio da consolidação do corpo docente: a instituição concluiu um processo seletivo estruturado e contratou 10 professores em regime CLT integral/horista para o eixo tecnológico, eliminando a rotatividade de contratos temporários e assegurando estabilidade para a graduação. Fred enfatizou que os professores selecionados possuem forte vivência no mercado de tecnologia, unindo rigor acadêmico a práticas contemporâneas de desenvolvimento de software.

Foi reforçada a estrutura do Projeto Integrador, destacando a liderança do Professor Thiago na orientação dos grupos e a necessidade de que os projetos entreguem valor real integrando banco de dados, lógica e engenharia de requisitos. Fred encerrou a sessão ouvindo demandas dos alunos sobre o calendário dos sábados letivos e a infraestrutura dos laboratórios."""
    },

    # SEMANA 2
    {
        "file_sem": SEMANAL_DIR / "W_02/pi_01.md",
        "file_est": ESTRUT_DIR / "2026-08-17_seg_pi.md",
        "raw": "17-ago-seg.txt",
        "titulo": "Projeto Integrador - Aula 01: Visão de Gerente de Projetos, TAP e Caso TJ",
        "disciplina": "Projeto Integrador",
        "professor": "Thiago",
        "data": "2026-08-17",
        "dia_semana": "Seg",
        "subtopicos": [
            "O Professor Thiago como Gerente de Projetos: A disciplina funcionará sob regime de gerência de projetos e demandas com entregas contínuas, e não aulas teóricas tradicionais.",
            "Integração Multidisciplinar: Aplicação prática da modelagem de banco de dados com Prof. Alexandre e desenvolvimento do backend.",
            "Termo de Abertura do Projeto (TAP): Estruturação de objetivos, custos operacionais da equipe, horas de desenvolvimento e identificação de Stakeholders.",
            "O Caso do Tribunal de Justiça (TJ): Relato de experiência onde sistemas governamentais precisaram de reformulação por falta de alinhamento com o usuário final."
        ],
        "analogias": [
            "Aqui eu não sou professor de passar teoria no quadro; sou o gerente de projetos de vocês. Passo a demanda e vocês entregam o software funcionando.",
            "Lá no TJ a gente viu sistemas que custaram milhões e o cidadão não conseguia tirar uma certidão criminal pela internet porque não pensaram no usuário final lá no início.",
            "Vocês precisam colocar na ponta do lápis o custo da equipe, das ferramentas e o valor do MVP para não quebrar o cliente."
        ],
        "sintese": """Na aula de segunda-feira de Projeto Integrador, o professor Thiago (mesmo docente de CADAC no semestre anterior) definiu uma dinâmica corporativa imersiva: posicionou-se formalmente como Gerente de Projetos e cliente das equipes, avisando que a disciplina será regida por sprints, entregas de demandas e homologações de código, e não por aulas teóricas tradicionais.

O professor Thiago orientou que o software dos grupos deve incorporar ativamente os aprendizados das outras matérias do semestre — em especial a modelagem de banco de dados relacional com o Prof. Alexandre e o backend em Java ou Python. Ele enfatizou que o projeto precisa sair do papel e se tornar um produto palpável com telas e persistência de dados.

Foi apresentada a estrutura do Termo de Abertura do Projeto (TAP). O professor detalhou a importância do levantamento de custos operacionais (hora-desenvolvedor, infraestrutura, ferramentas pagas) e da correta identificação dos Stakeholders. Para ilustrar, narrou sua experiência profissional no Tribunal de Justiça (TJ), onde acompanhou projetos governamentais que precisaram de reformulação drástica porque foram construídos sem alinhar as necessidades do usuário final. A aula encerrou com a orientação para que os grupos fechassem suas propostas de escopo e MVP."""
    },
    {
        "file_sem": SEMANAL_DIR / "W_02/poo_02.md",
        "file_est": ESTRUT_DIR / "2026-08-18_ter_poo.md",
        "raw": "18-ag-ter.txt",
        "titulo": "POO - Aula 02: Atributos vs Métodos na Prática (Lâmpada LED e Conta Bancária)",
        "disciplina": "Programação Orientada a Objetos",
        "professor": "Tibério",
        "data": "2026-08-18",
        "dia_semana": "Ter",
        "subtopicos": [
            "Diferença entre Atributos e Métodos: Características de estado estático vs ações e comportamentos operacionais de uma classe.",
            "Modelagem da Lâmpada LED: Demonstração no quadro com atributos (estado, cor) e funções de negócio (ligar, desligar, alterarCor).",
            "Modelagem de Veículos e Conta Bancária: Criação de classes para controle de velocidade (acelerar, frear) e operações financeiras (depósito, saldo, saque).",
            "Instanciação de Objetos: Criação de instâncias independentes em memória manipuladas através de chamadas de métodos."
        ],
        "analogias": [
            "Se você tem uma Lâmpada LED inteligente, os atributos são a cor atual e se ela está ligada ou desligada; a função é o comando que você manda no app para ligar e trocar a cor.",
            "Um carro não é apenas um monte de metal parado; ele tem estado (posição, velocidade) e comportamentos (acelerar, frear). É exatamente assim que desenhamos uma classe."
        ],
        "sintese": """A segunda aula de POO com o professor Tibério foi dedicada à fixação prática dos conceitos de Classe, Atributos e Métodos através de modelagens diretas no quadro e no ambiente de programação. O professor buscou desmistificar o jargão técnico utilizando analogias do cotidiano.

A primeira modelagem apresentada foi a de uma Lâmpada LED inteligente. O professor Tibério demonstrou que as propriedades da lâmpada (como estado ligado/desligado, cor e brilho) representam os atributos da classe, enquanto as ações que transformam esse estado (como as funções ligar(), desligar() e alterarCor()) representam os métodos da classe.

Em seguida, a turma modelou uma classe de Veículo e um sistema simplificado de Conta Bancária. Foi discutido como as regras de negócio de um banco — como verificar saldo antes de autorizar um saque ou atualizar o montante após um depósito — devem estar encapsuladas dentro dos métodos da própria conta, impedindo que o saldo seja alterado arbitrariamente de fora. A aula finalizou com os alunos escrevendo suas primeiras estruturas de classes no computador e testando a instanciação de múltiplos objetos independentes."""
    },
    {
        "file_sem": SEMANAL_DIR / "W_02/c_03.md",
        "file_est": ESTRUT_DIR / "2026-08-19_qua_c.md",
        "raw": "19-ago-qua.txt",
        "titulo": "Linguagem C - Aula 03: Exercícios em Laboratório, Lógica em C e Depuração",
        "disciplina": "Linguagem C",
        "professor": "Vinícius",
        "data": "2026-08-19",
        "dia_semana": "Qua",
        "subtopicos": [
            "Organização do Laboratório: Abertura das pastas de trabalho locais e verificação do compilador.",
            "Revisão de Dúvidas de Sintaxe: Ajustes em declarações de variáveis, leitura com scanf e impressão formatada.",
            "Resolução de Listas de Lógica em C: Exercícios envolvendo cálculos matemáticos e condicionais encadeadas.",
            "Atendimento Individual nas Bancadas: Identificação de falhas de digitação, escopo e compilação."
        ],
        "analogias": [
            "Abram a pasta de vocês e vamos direto para o código. Não adianta só assistir aula, tem que travar no exercício e descobrir por que o GCC tá reclamando.",
            "C não perdoa falta de atenção em ponto-e-vírgula e tipos de variáveis; o compilador é seu amigo mais rigoroso."
        ],
        "sintese": """Na quarta-feira, a aula de Linguagem C com o professor Vinícius foi focada no desenvolvimento prático de exercícios no laboratório de informática. O professor orientou os alunos a abrirem seus ambientes de desenvolvimento locais e deu início à resolução da lista de fixação de lógica em linguagem C.

Durante a sessão, os alunos exercitaram a construção de programas com estruturas de decisão e laços básicos, aplicando leitura de dados pelo teclado com scanf e exibição formatada com printf. O professor Vinícius percorreu as bancadas atendendo individualmente os estudantes, esclarecendo dúvidas sobre precedência de operadores e resolvendo falhas comuns de digitação e sintaxe.

A dinâmica permitiu que a turma identificasse os principais pontos de atrito na transição de linguagens dinâmicas para a rigidez de C, preparando o terreno para os tópicos de operadores lógicos e estruturas mais complexas que foram aprofundados na aula de quinta-feira."""
    },
    {
        "file_sem": SEMANAL_DIR / "W_02/c_04.md",
        "file_est": ESTRUT_DIR / "2026-08-20_qui_c.md",
        "raw": "20-ago-qui.txt",
        "titulo": "Linguagem C - Aula 04: Estruturas de Decisão e Operadores Lógicos (&& e ||) na Lista",
        "disciplina": "Linguagem C",
        "professor": "Vinícius",
        "data": "2026-08-20",
        "dia_semana": "Qui",
        "subtopicos": [
            "Contexto da Lista de Exercícios: O professor Vinícius testou os exercícios na véspera e identificou a necessidade de reforçar operadores lógicos.",
            "Operadores Lógicos em C (&& e ||): Comparativo entre o AND (&&) e o OR (||) com a tabela-verdade do ensino médio e a sintaxe de Python.",
            "Aplicação Prática em Condicionais: Validação de intervalos numéricos em uma única linha de código sem ifs aninhados desnecessários.",
            "Continuação da Resolução: Prática autônoma dos alunos com suporte em sala."
        ],
        "analogias": [
            "Eu fiz a experiência de um dos exercícios dessa lista ontem à noite e vi que para facilitar a vida do cidadão eu precisava falar dos operadores && e || que vocês já conhecem do ensino médio e do Python.",
            "O && só deixa passar se todo mundo for verdadeiro; o || basta um ser verdadeiro que ele já autoriza."
        ],
        "sintese": """A aula de quinta-feira de Linguagem C com o professor Vinícius foi breve e focada em uma intervenção técnica direta do professor para desbloquear a resolução da lista de exercícios de estruturas de decisão.

O docente relatou que realizou os exercícios da lista na véspera para avaliar o grau de dificuldade e percebeu que muitos alunos estavam criando múltiplos blocos if aninhados de forma desnecessariamente complexa. Para simplificar a lógica dos programas, fez uma revisão no quadro sobre os operadores lógicos fundamentais da linguagem C: o operador lógico E (&&) e o operador lógico OU (||).

Foi feito o paralelo com a sintaxe de Python (and / or) e com a tabela-verdade estudada no ensino médio. O professor Vinícius exemplificou como utilizar if (x >= 10 && x <= 20) em uma única linha clara para validar intervalos numéricos. Após a explicação, a turma deu continuidade à resolução prática da lista com muito mais agilidade e fluidez."""
    },
    {
        "file_sem": SEMANAL_DIR / "W_02/bd_02.md",
        "file_est": ESTRUT_DIR / "2026-08-21_sex_bd.md",
        "raw": "21-ago-sex.txt",
        "titulo": "Banco de Dados Relacional - Aula 01: Mentoria de Modelagem e Alinhamento",
        "disciplina": "Banco de Dados Relacional",
        "professor": "Alexandre",
        "data": "2026-08-21",
        "dia_semana": "Sex",
        "subtopicos": [
            "Mentoria com Grupos: Atendimento individualizado do Prof. Alexandre a cada equipe para validar a base de dados dos projetos.",
            "Cultura de Tirar Dúvidas: Estímulo do professor para que os alunos usem o espaço de aula para solucionar bloqueios antes de iniciar a modelagem pesada.",
            "Retrospectiva do Semestre Passado: Análise com os alunos das dificuldades enfrentadas no primeiro semestre para evitar os mesmos erros.",
            "Refinamento de Escopo e Dados: Orientação para cortar requisitos secundários e focar no núcleo relacional do produto."
        ],
        "analogias": [
            "Aproveita que está aqui para tirar dúvida; se você não perguntar agora, a dúvida vai virar um bug na hora de entregar o banco de dados.",
            "Quem já fez projetos no semestre passado sabe onde o bicho pegou; usem essa experiência para acertar de primeira agora."
        ],
        "sintese": """A aula de sexta-feira de Banco de Dados Relacional com o professor Alexandre funcionou como uma sessão intensiva de mentoria e alinhamento de escopos de dados com os grupos.

O professor Alexandre enfatizou a importância de os alunos utilizarem o horário presencial de aula para tirar dúvidas, debater impedimentos técnicos e validar as escolhas de modelagem antes de iniciarem a criação de tabelas e relacionamentos. Houve uma troca de experiências relembrando as dificuldades do semestre anterior, identificando gargalos comuns de modelagem e requisitos mal dimensionados.

Cada grupo apresentou informalmente a proposta de dados para o projeto do semestre. O professor orientou na redução de complexidades desnecessárias, recomendando que as equipes foquem em um modelo relacional consistente e bem normalizado antes de adicionarem entidades secundárias. A aula encerrou com o direcionamento das atividades para o sábado letivo."""
    },
    {
        "file_sem": SEMANAL_DIR / "W_02/extensao_01.md",
        "file_est": ESTRUT_DIR / "2026-08-22_sab_extensao.md",
        "raw": "22-ago-sab.txt",
        "titulo": "Projeto de Extensão - Aula 01: Formação de Grupos e Planejamento Integrado",
        "disciplina": "Projeto de Extensão",
        "professor": "Docente Titular",
        "data": "2026-08-22",
        "dia_semana": "Sáb",
        "subtopicos": [
            "Formação de Equipes (Regra dos Grupos de 4 Alunos): Definição do tamanho ideal de equipe para divisão balanceada de tarefas no Projeto de Extensão.",
            "Histórico do 1º Semestre: Comparação sobre a dinâmica das aulas de sábado do semestre anterior (turmas com Bruno Julins e Alexandre).",
            "Divisão de Responsabilidades Técnicas: Distribuição de papéis em documentação de extensão, contato com a comunidade, desenvolvimento e dados.",
            "Fechamento da Semana 2: Consolidação dos grupos e canais de comunicação para início das atividades de extensão."
        ],
        "analogias": [
            "A gente monta um grupo de quatro pessoas aqui e pronto; todo mundo tem que ter uma função clara, senão dois trabalham e dois só olham.",
            "No semestre passado o pessoal que fazia sábado à noite com o Alexandre ficava duas horas direto; aqui a gente vai focar em planejamento e entrega prática."
        ],
        "sintese": """O sábado letivo consolidou o encerramento da segunda semana do semestre 2026.2, reunindo a turma para a organização definitiva das equipes de Projeto de Extensão e planejamento das atividades comunitárias integradas.

A pauta central foi a formação de grupos de trabalho com cerca de quatro alunos, formato considerado ideal para equilibrar as responsabilidades de desenvolvimento e articulação externa do projeto de extensão. Houve um momento de integração relembrando a dinâmica das aulas de sábado do semestre anterior conduzidas pelos professores Bruno Julins e Alexandre.

Os alunos aproveitaram o encontro para definir seus canais de comunicação, repositórios de controle de versão e cronograma de reuniões semanais. A sessão concluiu com todas as equipes oficialmente registradas e prontas para iniciar as atividades de extensão do segundo semestre."""
    }
]

for item in aulas:
    subs_formatted = "\n".join([f"{i+1}. **{s.split(':')[0]}:** {s.split(':')[1] if ':' in s else ''}" for i, s in enumerate(item["subtopicos"])])
    ans_formatted = "\n".join([f"- *\"{a}\"*" for a in item["analogias"]])
    
    # 1. Arquivo estruturado
    estruturado_text = f"""# 🎓 {item['titulo']}
**Data:** {item['data']} ({item['dia_semana']}) | **Disciplina:** {item['disciplina']} | **Professor:** {item['professor']} | **Áudio Original:** `{item['raw']}`

---

## 📌 Subtópicos em Ordem Cronológica Real
{subs_formatted}

---

## 💡 Analogias, Causos & Relatos em Sala
{ans_formatted}

---

## 📝 Síntese Fiel da Aula (~2.000 caracteres)
{item['sintese']}
"""
    with open(item["file_est"], "w", encoding="utf-8") as f:
        f.write(estruturado_text.strip() + "\n")

    # 2. Arquivo semanal para o portal
    semanal_text = f"""---
tipo: portal
titulo: "{item['titulo']}"
disciplina: "{item['disciplina']}"
semestre: "2026.2"
data: {item['data']}
professor: "{item['professor']}"
---

## 📌 Roteiro da Aula em Ordem Cronológica
{subs_formatted}

---

## 💡 Analogias e Casos Reais Contados em Sala
{ans_formatted}

---

## 📝 Síntese Fiel dos Acontecimentos
{item['sintese']}

---

## Glossário
"""
    if item["disciplina"] == "Programação Orientada a Objetos":
        semanal_text += """- **Classe**: Molde estrutural ou gabarito que define atributos e métodos de um tipo de dado.
- **Objeto**: Instância concreta alocada na memória a partir de uma classe.
- **JVM (Java Virtual Machine)**: Ambiente de execução que interpreta o bytecode Java em código de máquina nativo.
- **Encapsulamento**: Mecanismo de proteção do estado interno dos objetos através de modificadores de acesso.
- **MongoDB**: Banco de dados NoSQL orientado a documentos JSON amplamente integrado com JavaScript no backend.
"""
    elif item["disciplina"] == "Linguagem C":
        semanal_text += """- **Compilador**: Software que traduz código fonte em C para binário executável nativo.
- **Operador sizeof**: Operador unário que retorna o tamanho físico exato em bytes alocado para qualquer tipo ou variável.
- **Operador de Endereço (&)**: Operador unário que retorna a posição de memória física de uma variável.
- **Operadores Lógicos (&& e ||)**: Operadores relacionais E (conjunção) e OU (disjunção) para validação de expressões condicionais.
"""
    elif item["disciplina"] == "Projeto Integrador":
        semanal_text += """- **Projeto Integrador**: Unidade curricular focada na aplicação prática e integrada de conhecimentos multidisciplinares.
- **Termo de Abertura do Projeto (TAP)**: Documento formal que define escopo inicial, objetivos, custos operacionais e stakeholders.
- **Stakeholders**: Pessoas, grupos ou instituições que possuem interesse direto ou são impactados pelo projeto de software.
- **MVP (Mínimo Produto Viável)**: Versão mais enxuta do software que já entrega valor real ao usuário final.
"""
    elif item["disciplina"] == "Banco de Dados Relacional":
        semanal_text += """- **SGBD**: Sistema de software responsável pelo gerenciamento, integridade e segurança de bases de dados.
- **Modelo Relacional**: Modelo de dados baseado em tabelas bidimensionais e integridade referencial.
- **Normalização**: Processo de organização dos dados em tabelas para evitar redundância e anomalias de atualização.
"""
    elif item["disciplina"] == "Projeto de Extensão":
        semanal_text += """- **Projeto de Extensão**: Ação acadêmica que articula o conhecimento técnico desenvolvido na faculdade com demandas reais da comunidade.
- **Sprint**: Período de tempo fixo em métodos ágeis durante o qual um conjunto de entregas deve ser completado.
"""
    else:
        semanal_text += """- **Comunicação Institucional**: Alinhamento administrativo e pedagógico conduzido pela coordenação do curso.
"""

    with open(item["file_sem"], "w", encoding="utf-8") as f:
        f.write(semanal_text.strip() + "\n")

print("✅ Todos os arquivos foram reorganizados rigorosamente na Grade Oficial do Semestre 2!")
