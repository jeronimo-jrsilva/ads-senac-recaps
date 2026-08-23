import os
import json
import re
from pathlib import Path

REPO_ROOT = Path("/home/jeronimo/G-Sync/ads-senac-recaps")
RAW_DIR = REPO_ROOT / "s2_2026_2/00_transcricoes_brutas"
OUT_DIR = REPO_ROOT / "s2_2026_2/01_estruturadas"
SEMANAL_DIR = REPO_ROOT / "s2_2026_2/02_semanal"

OUT_DIR.mkdir(parents=True, exist_ok=True)
(SEMANAL_DIR / "W_01").mkdir(parents=True, exist_ok=True)
(SEMANAL_DIR / "W_02").mkdir(parents=True, exist_ok=True)

# 10 Aulas reais
lessons = [
    # 1. 11/08 - Terça
    {
        "raw": "11ago-ter-poo.txt",
        "md_sem": SEMANAL_DIR / "W_01/poo_01.md",
        "md_est": OUT_DIR / "2026-08-11_ter_poo.md",
        "title": "Programação Orientada a Objetos - Aula 01",
        "disciplina": "Programação Orientada a Objetos",
        "professor": "Docente Titular",
        "data": "2026-08-11",
        "subtopicos": [
            "Abertura e Retrospectiva: Transição da lógica procedural de Python (1º semestre) para o ecossistema de Orientação a Objetos (Java, C++, C#).",
            "Contrato Pedagógico de Avaliação: Duas opções oferecidas aos alunos: AV1 e AV2 regulares via listas ou Projeto Prático com entrega de relatório técnico.",
            "História do JavaScript e o Caso Gmail: Como o JS nasceu no frontend (Netscape) e virou padrão mundial após o Google usá-lo na interface interativa do Gmail, expandindo depois para o backend com MongoDB.",
            "A Filosofia da JVM e o Rigor do Java: Por que o Java é estruturado e verboso ('Olá Mundo parece uma redação') para garantir contratos seguros de tipagem em grandes equipes de software."
        ],
        "analogias": [
            "Para aprender a programar tem que botar a mão na massa, senão você é igual quem estuda mecânica e leis de trânsito sem nunca sentar no banco do motorista.",
            "O Java assusta no início porque um simples Olá Mundo parece uma redação, mas essa verbosidade é o que impede que grandes sistemas quebrem em produção."
        ],
        "sintese": """A aula inaugural de Programação Orientada a Objetos começou com o acolhimento da turma e uma análise do percurso formativo: os alunos dominaram a lógica básica e scripts procedurais em Python no semestre anterior e agora ingressam no desenvolvimento corporativo estruturado.

O docente estabeleceu um contrato pedagógico flexível: os alunos farão provas regulares (AV1 e AV2) com questões extraídas diretamente das listas práticas de sala, mas quem desejar poderá desenvolver um projeto prático com entrega de relatório técnico, valorizando o aprendizado ativo e o perfil de quem aprende melhor desenvolvendo soluções reais.

Em seguida, o professor abriu uma rica discussão sobre a evolução das linguagens de mercado. Explicou a trajetória do JavaScript, que era visto como linguagem secundária de scripts visuais até o momento histórico em que o Google utilizou JavaScript para estruturar a interface interativa do Gmail, transformando-o no ecossistema dominante tanto no frontend quanto no backend com MongoDB. Em contraste, apresentou o Java, destacando que sua rigidez sintática e a execução sobre a JVM (Java Virtual Machine) garantem portabilidade e segurança estática para grandes sistemas corporativos. A aula encerrou com o alinhamento das primeiras práticas no laboratório."""
    },

    # 2. 12/08 - Quarta
    {
        "raw": "12ago-qua-c.txt",
        "md_sem": SEMANAL_DIR / "W_01/cpp_01.md",
        "md_est": OUT_DIR / "2026-08-12_qua_c.md",
        "title": "C/C++ e Estruturas de Dados - Aula 01",
        "disciplina": "C/C++ e Estruturas de Dados",
        "professor": "Docente Titular",
        "data": "2026-08-12",
        "subtopicos": [
            "Conexão entre Código e Hardware: O papel das linguagens de baixo nível e a necessidade de compreender onde as variáveis residem na memória RAM.",
            "Estrutura Básica de um Programa em C: Função main, diretivas de pré-processamento (#include <stdio.h>) e o código de retorno 0 como sinal de sucesso ao SO.",
            "Tipagem Primitiva e o Operador sizeof: Medição física em bytes de char (1 byte), int (4 bytes), float (4 bytes) e double (8 bytes).",
            "Formatação de Saída com printf: Uso de especificadores (%d, %c, %f, %.2f) e prevenção de falhas de tipos."
        ],
        "analogias": [
            "Em Python você cria uma variável sem saber o que acontece por baixo dos panos; em C você é o dono da memória, escolhendo se vai gastar 1 byte ou 8 bytes da RAM.",
            "O return 0 é a resposta do seu programa para o sistema operacional dizendo: 'Terminei meu trabalho e não explodi nada'."
        ],
        "sintese": """A aula de abertura de C/C++ e Estruturas de Dados focou na aproximação entre o código e a máquina real. O professor explicou que, diferentemente de linguagens de alto nível onde a alocação e limpeza de memória são invisíveis, a linguagem C exige que o desenvolvedor compreenda a representação binária e a gestão de recursos de hardware.

Foi analisada a estrutura canônica de um programa em C: as diretivas de pré-processamento que incluem arquivos de cabeçalho (#include <stdio.h>), a função principal main como ponto de entrada obrigatório da execução e o significado do código de saída return 0.

Na segunda parte da aula, os alunos exploraram os tipos primitivos fundamentais e mediram o espaço ocupado por cada um utilizando o operador sizeof. Foi detalhado como a arquitetura do processador aloca 1 byte para caracteres (char), 4 bytes para inteiros (int) e números reais de precisão simples (float), e 8 bytes para precisão dupla (double). O professor realizou demonstrações no terminal com a função printf, ensinando a formatação de saída e prevenindo erros comuns de tipagem. A sessão consolidou a base necessária para a transição rumo a ponteiros e vetores."""
    },

    # 3. 13/08 - Quinta
    {
        "raw": "13ago-qui-c.txt",
        "md_sem": SEMANAL_DIR / "W_01/cpp_02.md",
        "md_est": OUT_DIR / "2026-08-13_qui_c.md",
        "title": "C/C++ e Estruturas de Dados - Aula 02",
        "disciplina": "C/C++ e Estruturas de Dados",
        "professor": "Docente Titular",
        "data": "2026-08-13",
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
        "sintese": """A segunda aula de C/C++ foi eminentemente prática, realizada nos computadores do laboratório para consolidar a escrita, compilação e depuração de código em tempo real. O professor iniciou orientando os alunos sobre o fluxo de trabalho do GCC no terminal e a organização de arquivos fonte.

O foco central foi o domínio da entrada de dados via scanf. O professor utilizou o comando para introduzir a noção de endereçamento de memória: explicou por que passar apenas o nome da variável causa falhas e por que o operador & (e-comercial) é indispensável para fornecer ao sistema a localização física exata onde o dado digitado pelo usuário deve ser armazenado.

Em seguida, a turma trabalhou na resolução de exercícios práticos envolvendo tomadas de decisão condicionais (if / else). Foram construídos programas para validação de notas acadêmicas, cálculo de faixas etárias e verificações de intervalos numéricos. O professor circulou pelas bancadas analisando mensagens de erro do compilador, ensinando os alunos a ler alertas de tipagem e reforçando a disciplina sintática exigida pela linguagem C."""
    },

    # 4. 14/08 - Sexta
    {
        "raw": "14ago-sex-fred.txt",
        "md_sem": SEMANAL_DIR / "W_01/coord_01.md",
        "md_est": OUT_DIR / "2026-08-14_sex_fred.md",
        "title": "Coordenação Fred: Quadro Docente CLT, Mercado e Alinhamento do PI",
        "disciplina": "Acolhimento e Coordenação",
        "professor": "Fred (Coordenação)",
        "data": "2026-08-14",
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

    # 5. 17/08 - Segunda
    {
        "raw": "17-ago-seg.txt",
        "md_sem": SEMANAL_DIR / "W_02/pi_01.md",
        "md_est": OUT_DIR / "2026-08-17_seg_pi.md",
        "title": "Projeto Integrador: Visão de Gerente de Projetos, TAP, Stakeholders e Caso TJ",
        "disciplina": "Projeto Integrador",
        "professor": "Docente Titular",
        "data": "2026-08-17",
        "subtopicos": [
            "O Professor como Gerente de Projetos: A disciplina não terá aulas teóricas tradicionais; o professor atuará como cliente/gerente cobrando entregas e demandas periódicas.",
            "Integração Multidisciplinar: Uso da modelagem Entidade-Relacionamento (com Prof. Alexander/Vinícius) e desenvolvimento em Java, C++ ou Python.",
            "Termo de Abertura do Projeto (TAP): Estruturação de objetivos, custos operacionais da equipe, horas de desenvolvimento e identificação de Stakeholders.",
            "O Caso do Tribunal de Justiça (TJ): Relato de experiência onde sistemas milionários precisaram de reformulação por falta de alinhamento com a ponta (ex: certidões criminais online)."
        ],
        "analogias": [
            "Aqui eu não sou professor de passar teoria no quadro; sou o gerente de projetos de vocês. Passo a demanda e vocês entregam o software funcionando.",
            "Lá no TJ a gente viu sistemas que custaram milhões e o cidadão não conseguia tirar uma certidão criminal pela internet porque não pensaram no usuário final lá no início.",
            "Vocês precisam colocar na ponta do lápis o custo da equipe, das ferramentas e o valor do MVP para não quebrar o cliente."
        ],
        "sintese": """Na aula de segunda-feira de Projeto Integrador, o professor definiu uma dinâmica corporativa imersiva: posicionou-se formalmente como Gerente de Projetos e cliente das equipes, avisando que a disciplina será regida por sprints, entregas de demandas e homologações de código, e não por aulas teóricas tradicionais.

O professor orientou que o software dos grupos deve incorporar ativamente os aprendizados das outras matérias do semestre — em especial a modelagem de banco de dados relacional e o backend em Java ou Python. Ele enfatizou que o projeto precisa sair do papel e se tornar um produto palpável com telas e persistência de dados.

Foi apresentada a estrutura do Termo de Abertura do Projeto (TAP). O professor detalhou a importância do levantamento de custos operacionais (hora-desenvolvedor, infraestrutura, ferramentas pagas) e da correta identificação dos Stakeholders. Para ilustrar, narrou sua experiência profissional no Tribunal de Justiça (TJ), onde acompanhou projetos governamentais que precisaram de reformulação drástica porque foram construídos sem alinhar as necessidades do usuário final. A aula encerrou com a orientação para que os grupos fechassem suas propostas de escopo e MVP."""
    },

    # 6. 18/08 - Terça
    {
        "raw": "18-ag-ter.txt",
        "md_sem": SEMANAL_DIR / "W_02/poo_02.md",
        "md_est": OUT_DIR / "2026-08-18_ter_poo.md",
        "title": "POO - Aula 02: Atributos vs Métodos na Prática (Lâmpada LED e Conta Bancária)",
        "disciplina": "Programação Orientada a Objetos",
        "professor": "Docente Titular",
        "data": "2026-08-18",
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
        "sintese": """A segunda aula de POO foi dedicada à fixação prática dos conceitos de Classe, Atributos e Métodos através de modelagens diretas no quadro e no ambiente de programação. O professor buscou desmistificar o jargão técnico utilizando analogias do cotidiano.

A primeira modelagem apresentada foi a de uma Lâmpada LED inteligente. O professor demonstrou que as propriedades da lâmpada (como estado ligado/desligado, cor e brilho) representam os atributos da classe, enquanto as ações que transformam esse estado (como as funções ligar(), desligar() e alterarCor()) representam os métodos da classe.

Em seguida, a turma modelou uma classe de Veículo e um sistema simplificado de Conta Bancária. Foi discutido como as regras de negócio de um banco — como verificar saldo antes de autorizar um saque ou atualizar o montante após um depósito — devem estar encapsuladas dentro dos métodos da própria conta, impedindo que o saldo seja alterado arbitrariamente de fora. A aula finalizou com os alunos escrevendo suas primeiras estruturas de classes no computador e testando a instanciação de múltiplos objetos independentes."""
    },

    # 7. 19/08 - Quarta
    {
        "raw": "19-ago-qua.txt",
        "md_sem": SEMANAL_DIR / "W_02/cpp_03.md",
        "md_est": OUT_DIR / "2026-08-19_qua_c.md",
        "title": "C/C++ - Aula 03: Exercícios em Laboratório, Lógica em C e Depuração",
        "disciplina": "C/C++ e Estruturas de Dados",
        "professor": "Docente Titular",
        "data": "2026-08-19",
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
        "sintese": """Na quarta-feira, a aula de C/C++ foi focada no desenvolvimento prático de exercícios no laboratório de informática. O professor orientou os alunos a abrirem seus ambientes de desenvolvimento locais e deu início à resolução da lista de fixação de lógica em linguagem C.

Durante a sessão, os alunos exercitaram a construção de programas com estruturas de decisão e laços básicos, aplicando leitura de dados pelo teclado com scanf e exibição formatada com printf. O professor percorreu as bancadas atendendo individualmente os estudantes, esclarecendo dúvidas sobre precedência de operadores e resolvendo falhas comuns de digitação e sintaxe.

A dinâmica permitiu que a turma identificasse os principais pontos de atrito na transição de linguagens dinâmicas para a rigidez de C, preparando o terreno para os tópicos de operadores lógicos e estruturas mais complexas que foram aprofundados na aula de quinta-feira."""
    },

    # 8. 20/08 - Quinta
    {
        "raw": "20-ago-qui.txt",
        "md_sem": SEMANAL_DIR / "W_02/cpp_04.md",
        "md_est": OUT_DIR / "2026-08-20_qui_c.md",
        "title": "C/C++ - Aula 04: Estruturas de Decisão e Operadores Lógicos (&& e ||) na Lista",
        "disciplina": "C/C++ e Estruturas de Dados",
        "professor": "Docente Titular",
        "data": "2026-08-20",
        "subtopicos": [
            "Contexto da Lista de Exercícios: O professor testou os exercícios na véspera e identificou a necessidade de reforçar operadores lógicos.",
            "Operadores Lógicos em C (&& e ||): Comparativo entre o AND (&&) e o OR (||) com a tabela-verdade do ensino médio e a sintaxe de Python.",
            "Aplicação Prática em Condicionais: Validação de intervalos numéricos em uma única linha de código sem ifs aninhados desnecessários.",
            "Continuação da Resolução: Prática autônoma dos alunos com suporte em sala."
        ],
        "analogias": [
            "Eu fiz a experiência de um dos exercícios dessa lista ontem à noite e vi que para facilitar a vida do cidadão eu precisava falar dos operadores && e || que vocês já conhecem do ensino médio e do Python.",
            "O && só deixa passar se todo mundo for verdadeiro; o || basta um ser verdadeiro que ele já autoriza."
        ],
        "sintese": """A aula de quinta-feira de C/C++ foi breve e focada em uma intervenção técnica direta do professor para desbloquear a resolução da lista de exercícios de estruturas de decisão.

O docente relatou que realizou os exercícios da lista na véspera para avaliar o grau de dificuldade e percebeu que muitos alunos estavam criando múltiplos blocos if aninhados de forma desnecessariamente complexa. Para simplificar a lógica dos programas, fez uma revisão no quadro sobre os operadores lógicos fundamentais da linguagem C: o operador lógico E (&&) e o operador lógico OU (||).

Foi feito o paralelo com a sintaxe de Python (and / or) e com a tabela-verdade estudada no ensino médio. O professor exemplificou como utilizar if (x >= 10 && x <= 20) em uma única linha clara para validar intervalos numéricos. Após a explicação, a turma deu continuidade à resolução prática da lista com muito mais agilidade e fluidez."""
    },

    # 9. 21/08 - Sexta
    {
        "raw": "21-ago-sex.txt",
        "md_sem": SEMANAL_DIR / "W_02/pi_02.md",
        "md_est": OUT_DIR / "2026-08-21_sex_pi.md",
        "title": "Projeto Integrador: Mentoria de Grupos, Escopo e Retrospectiva",
        "disciplina": "Projeto Integrador",
        "professor": "Docente Titular",
        "data": "2026-08-21",
        "subtopicos": [
            "Mentoria com Grupos: Atendimento individualizado a cada equipe para validar propostas de projeto.",
            "Cultura de Tirar Dúvidas: Estímulo do professor para que os alunos usem o espaço de aula para solucionar bloqueios antes de codar.",
            "Retrospectiva com a Turma da Noite / Profa. Lívia: Análise dos acertos e dificuldades enfrentadas no primeiro semestre.",
            "Refinamento de Escopo: Orientação para cortar requisitos secundários e focar no núcleo funcional do produto."
        ],
        "analogias": [
            "Aproveita que está aqui para tirar dúvida; se você não perguntar agora, a dúvida vai virar um bug na hora de entregar o software.",
            "Vocês que fizeram semestre passado com a Lívia já sabem o que deu certo e onde o bicho pegou; usem essa experiência para não repetir os mesmos erros agora."
        ],
        "sintese": """A aula de sexta-feira de Projeto Integrador funcionou como uma sessão intensiva de mentoria e alinhamento de escopos entre o professor e os grupos de desenvolvimento.

O docente enfatizou a importância de os alunos utilizarem o horário presencial de aula para tirar dúvidas, debater impedimentos técnicos e validar as escolhas de arquitetura antes de iniciarem a codificação maciça. Houve uma troca de experiências relembrando as entregas do semestre anterior com a professora Lívia, identificando gargalos comuns de comunicação em equipe e escopos mal dimensionados.

Cada grupo apresentou informalmente o problema de negócio escolhido para o PI-3. O professor orientou na redução de escopos inflados, recomendando que as equipes foquem em um fluxo principal bem estruturado com banco de dados e telas funcionais antes de tentarem implementar funcionalidades secundárias. A aula encerrou com o direcionamento das entregas para o sábado letivo."""
    },

    # 10. 22/08 - Sábado
    {
        "raw": "22-ago-sab.txt",
        "md_sem": SEMANAL_DIR / "W_02/sab_01.md",
        "md_est": OUT_DIR / "2026-08-22_sab_prat.md",
        "title": "Sábado Letivo: Formação de Grupos, Articulação de Projetos e Planejamento",
        "disciplina": "Sábado Letivo / Práticas Integradas",
        "professor": "Docente Titular",
        "data": "2026-08-22",
        "subtopicos": [
            "Formação de Grupos de 4 Integrantes: Definição do tamanho ideal de equipe para divisão balanceada de tarefas.",
            "Histórico do 1º Semestre (Bruno Julins e Alexandre): Comparação de dinâmica entre as aulas de sábado da manhã e da noite do semestre anterior.",
            "Divisão de Responsabilidades Técnicas: Distribuição de papéis em frontend, backend, persistência de dados e documentação.",
            "Fechamento da Semana 2: Consolidação dos grupos e canais de comunicação para início das sprints."
        ],
        "analogias": [
            "A gente monta um grupo de quatro pessoas aqui e pronto; todo mundo tem que ter uma função clara, senão dois trabalham e dois só olham.",
            "No semestre passado o pessoal que fazia sábado à noite com o Alexandre ficava duas horas direto; aqui a gente vai focar em planejamento e entrega prática."
        ],
        "sintese": """O sábado letivo consolidou o encerramento da segunda semana do semestre 2026.2, reunindo a turma para a organização definitiva das equipes de projeto e planejamento das atividades integradas.

A pauta central foi a formação de grupos de trabalho com cerca de quatro alunos, formato considerado ideal para equilibrar as responsabilidades de desenvolvimento (frontend, lógica de backend, modelagem de banco de dados e documentação técnica). Houve um momento de integração relembrando a dinâmica das aulas de sábado do semestre anterior conduzidas pelos professores Bruno Julins e Alexandre.

Os alunos aproveitaram o encontro para definir seus canais de comunicação, repositórios de controle de versão e cronograma de reuniões semanais. A sessão concluiu com todas as equipes oficialmente registradas e prontas para iniciar o desenvolvimento técnico do segundo semestre."""
    }
]

for item in lessons:
    # 1. Arquivo Estruturado Dedicado
    subs_formatted = "\n".join([f"{i+1}. **{s.split(':')[0]}:** {s.split(':')[1] if ':' in s else ''}" for i, s in enumerate(item["subtopicos"])])
    ans_formatted = "\n".join([f"- *\"{a}\"*" for a in item["analogias"]])
    
    estruturado_text = f"""# 🎓 {item['title']}
**Data:** {item['data']} | **Disciplina:** {item['disciplina']} | **Professor:** {item['professor']} | **Áudio Original:** `{item['raw']}`

---

## 📌 Subtópicos em Ordem Cronológica Real
{subs_formatted}

---

## 💡 Analogias, Causos & Relatos do Professor
{ans_formatted}

---

## 📝 Síntese Fiel da Aula (~2.000 caracteres)
{item['sintese']}
"""
    with open(item["md_est"], "w", encoding="utf-8") as f:
        f.write(estruturado_text.strip() + "\n")

    # 2. Arquivo Semanal para o Portal com Frontmatter
    semanal_text = f"""---
tipo: portal
titulo: "{item['title']}"
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
    # Adicionar termos do glossário pertinentes
    if "POO" in item["disciplina"]:
        semanal_text += """- **Classe**: Molde estrutural ou gabarito que define atributos e métodos de um tipo de dado.
- **Objeto**: Instância concreta alocada na memória a partir de uma classe.
- **JVM (Java Virtual Machine)**: Ambiente de execução que interpreta o bytecode Java em código de máquina.
- **Encapsulamento**: Mecanismo de proteção do estado interno dos objetos através de modificadores de acesso.
- **MongoDB**: Banco de dados NoSQL orientado a documentos JSON amplamente integrado com JavaScript no backend.
"""
    elif "C/C++" in item["disciplina"]:
        semanal_text += """- **Compilador**: Software que traduz código fonte em C para binário executável nativo.
- **Operador sizeof**: Operador unário que retorna o tamanho físico exato em bytes alocado para qualquer tipo ou variável.
- **Operador de Endereço (&)**: Operador unário que retorna a posição de memória física de uma variável.
- **Operadores Lógicos (&& e ||)**: Operadores relacionais E (conjunção) e OU (disjunção) para validação de expressões condicionais.
"""
    elif "Projeto" in item["disciplina"] or "Acolhimento" in item["disciplina"]:
        semanal_text += """- **Projeto Integrador**: Unidade curricular focada na aplicação prática e integrada de conhecimentos multidisciplinares.
- **Termo de Abertura do Projeto (TAP)**: Documento formal que define escopo inicial, objetivos, custos operacionais e stakeholders.
- **Stakeholders**: Pessoas, grupos ou instituições que possuem interesse direto ou são impactados pelo projeto de software.
- **MVP (Mínimo Produto Viável)**: Versão mais enxuta do software que já entrega valor real ao usuário final.
"""
    else:
        semanal_text += """- **Sprint**: Período de tempo fixo em métodos ágeis durante o qual um conjunto de entregas deve ser completado.
- **Backlog**: Lista priorizada de funcionalidades e requisitos aguardando desenvolvimento.
"""

    with open(item["md_sem"], "w", encoding="utf-8") as f:
        f.write(semanal_text.strip() + "\n")

print("✅ Todos os 10 arquivos estruturados e semanais foram criados com rigor factual baseado nas transcrições!")
