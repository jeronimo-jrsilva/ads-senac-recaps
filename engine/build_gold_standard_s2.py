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

# 10 Aulas no padrão Gold Standard rigoroso (estilo 2026.1)
aulas_gold = [
    # -------------------------------------------------------------
    # SEMANA 1 (W_01)
    # -------------------------------------------------------------
    {
        "file_sem": SEMANAL_DIR / "W_01/poo_01.md",
        "file_est": ESTRUT_DIR / "2026-08-11_ter_poo.md",
        "content": """---
tipo: portal
titulo: "Programação Orientada a Objetos - Aula 01"
disciplina: "Programação Orientada a Objetos"
semestre: "2026.2"
data: 2026-08-11
professor: "Tibério"
---

A aula inaugural de Programação Orientada a Objetos com o Professor Tibério estabeleceu o marco conceitual e metodológico para o segundo semestre de ADS. A transição da lógica linear e procedural praticada em Python no semestre anterior para a disciplina estrutural de linguagens orientadas a objetos como Java, C++ e C# foi apresentada como o divisor de águas entre scripts pontuais e sistemas corporativos de grande porte.

---

## 1. Da Lógica Procedural à Engenharia de Objetos
O Professor Tibério contextualizou que a programação procedural separa dados e algoritmos, expondo variáveis soltas e gerando alto risco de efeitos colaterais em bases de código complexas:
- **O Fim do Acoplamento Desordenado:** No paradigma de objetos, dados e funções deixam de trafegar soltos pelo programa. Eles são encapsulados em entidades autônomas chamadas **Objetos**.
- **Atributos e Comportamentos:** Uma classe define a estrutura de dados (atributos) e o conjunto restrito de ações autorizadas a manipulá-los (métodos).
- **Abstração de Domínio:** O desenvolvedor modela o software mapeando conceitos do mundo real para gabaritos computacionais coesos.

---

## 2. Contrato Didático: Avaliações vs. Projetos Práticos
Foi definido o contrato pedagógico do semestre, valorizando diferentes perfis de aprendizado técnico:
- **Avaliações Regimentais (AV1 e AV2):** Provas práticas baseadas diretamente nas listas de exercícios resolvidos em sala de aula.
- **Trilha de Projeto com Relatório Técnico:** Os alunos que optarem por desenvolvimento prático poderão entregar um software documentado e com código funcional em substituição ou bonificação das provas teóricas.
- **A Analogia do Volante:** Tibério reforçou que estudar programação exige "tempo de teclado". Aprender a programar sem depurar código é como estudar leis de trânsito e mecânica sem nunca sentar no banco do motorista.

---

## 3. O Ecossistema Enterprise: O Caso Gmail, JS e o Rigor do Java
Foi traçada uma análise histórica da evolução das linguagens de mercado:
- **A Virada Histórica do JavaScript:** O JS nasceu na Netscape como linguagem de script para o navegador. Tibério narrou o momento de virada em que o Google utilizou JavaScript para estruturar o Gmail, provando que a linguagem suportava aplicações ricas no cliente. Posteriormente, com o motor V8 e MongoDB, conquistou o backend corporativo.
- **Java e a Filosofia da JVM:** Criado sob o lema "Write Once, Run Anywhere", o Java compila código fonte para bytecode. Tibério explicou que a verbosidade do Java ("fazer um Olá Mundo parece uma redação") é uma escolha deliberada de engenharia para forçar contratos explícitos e segurança estática de tipos em sistemas de missão crítica.

```java
// Estrutura canônica de uma classe em Java demonstrando contratos explícitos
public class Aluno {
    private String matricula;
    private String nome;
    private double rendimentoAcademico;

    public Aluno(String matricula, String nome, double rendimentoInicial) {
        this.matricula = matricula;
        this.nome = nome;
        this.rendimentoAcademico = rendimentoInicial;
    }

    public void atualizarRendimento(double novaNota) {
        if (novaNota >= 0 && novaNota <= 10) {
            this.rendimentoAcademico = (this.rendimentoAcademico + novaNota) / 2.0;
            System.out.println("CR atualizado: " + this.rendimentoAcademico);
        }
    }

    public void exibirDados() {
        System.out.println("Aluno: " + this.nome + " [Matrícula: " + this.matricula + "]");
    }
}
```

---

## Glossario
- **Classe**: Molde estrutural ou gabarito que define atributos e métodos de um tipo de dado [Wikipedia](https://pt.wikipedia.org/wiki/Classe_(programa%C3%A7%C3%A3o)).
- **Objeto**: Instância concreta alocada na memória a partir de uma classe [Wikipedia](https://pt.wikipedia.org/wiki/Objeto_(ci%C3%AAncia_da_computa%C3%A7%C3%A3o)).
- **JVM (Java Virtual Machine)**: Ambiente de execução que interpreta o bytecode Java em código de máquina nativo [Wikipedia](https://pt.wikipedia.org/wiki/M%C3%A1quina_virtual_Java).
- **Bytecode**: Formato binário intermediário executado por máquinas virtuais como a JVM.
- **Encapsulamento**: Mecanismo de proteção do estado interno dos objetos através de modificadores de acesso [Wikipedia](https://pt.wikipedia.org/wiki/Encapsulamento_(computa%C3%A7%C3%A3o)).
- **MongoDB**: Banco de dados NoSQL orientado a documentos JSON amplamente integrado com JavaScript no backend.
- **Tipagem Estática**: Sistema onde o tipo de cada variável é verificado em tempo de compilação.
"""
    },
    {
        "file_sem": SEMANAL_DIR / "W_01/c_01.md",
        "file_est": ESTRUT_DIR / "2026-08-12_qua_c.md",
        "content": """---
tipo: portal
titulo: "Linguagem C - Aula 01"
disciplina: "Linguagem C"
semestre: "2026.2"
data: 2026-08-12
professor: "Vinícius"
---

A aula inaugural de Linguagem C com o Professor Vinícius focou na aproximação direta entre o código e o hardware da máquina. O professor adotou a estratégia pedagógica de aprofundar os conceitos puros de C até a metade do semestre para garantir que a turma domine o controle de memória RAM antes de avançar para estruturas mais complexas.

---

## 1. Por que Aprender C na Era Moderna?
Em linguagens de alto nível com coleta automática de lixo (Garbage Collection), o desenvolvedor é isolado da gerência de recursos. O Professor Vinícius demonstrou por que o controle de baixo nível continua sendo a fundação de toda a indústria de software:
- **Controle Físico da Memória:** Em C, o programador decide exatamente quantos bytes serão alocados e gerenciados na memória RAM.
- **Infraestrutura Crítica:** Kernels de sistemas operacionais (Linux, Windows, macOS), bancos de dados relacionais e motores de renderização gráfica dependem do desempenho determinístico da linguagem C.
- **Disciplina de Engenharia:** A rigorosidade de C obriga o aluno a compreender a distinção entre stack, heap e endereços de memória.

---

## 2. A Anatomia do Programa em C e o Ciclo de Compilação
Foi analisada a estrutura canônica de um código em C e as fases de compilação via GCC:
- **Diretivas de Pré-Processador (`#include <stdio.h>`):** Inclusão dos protótipos de entrada e saída padrão antes da compilação real.
- **A Função `main` e Códigos de Saída:** A convenção `return 0` como sinal padronizado para o sistema operacional de que o programa concluiu sua execução sem falhas.

```c
#include <stdio.h>

int main(void) {
    // Declaração de tipos primitivos fundamentais
    int matricula = 202601;
    char turma = 'B';
    float media = 8.75f;
    double timestamp = 1723456789.123;

    printf("=== REGISTRO ACADÊMICO SENAC ===\\n");
    printf("Matrícula: %d | Turma: %c\\n", matricula, turma);
    printf("Média Semestral: %.2f\\n", media);
    
    // Inspeção de tamanho em bytes
    printf("Tamanho em Memória (int): %lu bytes\\n", sizeof(matricula));
    printf("Tamanho em Memória (float): %lu bytes\\n", sizeof(media));
    printf("Tamanho em Memória (double): %lu bytes\\n", sizeof(timestamp));

    return 0; // Sinal de execução bem-sucedida
}
```

---

## 3. Tipos Primitivos e o Operador `sizeof`
A turma explorou a representação de dados na arquitetura x86_64:
- **`char` (1 byte):** Armazenamento de caracteres individuais ou inteiros na faixa de -128 a 127.
- **`int` (4 bytes):** Inteiros de 32 bits cobrindo a faixa aproximada de -2 bilhões a +2 bilhões.
- **`float` e `double`:** Ponto flutuante sob o padrão IEEE 754 (4 bytes para precisão simples e 8 bytes para precisão dupla).
- **Formatação com `printf`:** Uso rigoroso de especificadores de formato (`%d`, `%c`, `%f`, `%.2f`) para evitar leitura de lixo de memória.

---

## Glossario
- **Compilador**: Software que traduz código fonte em C diretamente para código de máquina executável [Wikipedia](https://pt.wikipedia.org/wiki/Compilador).
- **Operador sizeof**: Operador unário da linguagem C que retorna o tamanho físico em bytes alocado para qualquer tipo ou variável [Wikipedia](https://pt.wikipedia.org/wiki/Sizeof).
- **Diretiva de Pré-processador**: Instruções iniciadas com `#` processadas antes da compilação real do código.
- **IEEE 754**: Padrão internacional que governa a representação e aritmética de números em ponto flutuante [Wikipedia](https://pt.wikipedia.org/wiki/IEEE_754).
- **glibc**: Biblioteca padrão de C no ecossistema GNU/Linux que fornece funções essenciais como `printf` e `scanf`.
"""
    },
    {
        "file_sem": SEMANAL_DIR / "W_01/c_02.md",
        "file_est": ESTRUT_DIR / "2026-08-13_qui_c.md",
        "content": """---
tipo: portal
titulo: "Linguagem C - Aula 02"
disciplina: "Linguagem C"
semestre: "2026.2"
data: 2026-08-13
professor: "Vinícius"
---

A segunda aula de Linguagem C com o Professor Vinícius foi realizada no laboratório de informática, focando na escrita de código ao vivo, compilação no terminal e compreensão da entrada de dados via `scanf` e estruturas condicionais.

---

## 1. Entrada de Dados e o Operador de Endereço (`&`)
O Professor Vinícius utilizou o comando `scanf` para introduzir o conceito de endereçamento de memória:
- **A Analogia do Endereço de Entrega:** Quando passamos `&variavel` para o `scanf`, estamos fornecendo a coordenada física exata da memória RAM onde o dado digitado pelo usuário deve ser gravado.
- **Perigo da Omisssão do `&`:** Omitir o operador faz o programa passar o valor da variável (muitas vezes zero ou lixo) como se fosse um endereço, resultando em falha de segmentação (Segmentation Fault).

```c
#include <stdio.h>

int main(void) {
    int idade = 0;
    float nota = 0.0f;

    printf("Digite a idade do aluno: ");
    scanf("%d", &idade); // & fornece o endereço na memória RAM

    printf("Digite a nota da avaliação: ");
    scanf("%f", &nota);

    // Validação condicional simples
    if (nota >= 7.0f) {
        printf("Aluno com %d anos: APROVADO com média %.2f\\n", idade, nota);
    } else {
        printf("Aluno com %d anos: EM RECUPERAÇÃO com média %.2f\\n", idade, nota);
    }

    return 0;
}
```

---

## 2. Estruturas de Decisão (`if`, `else if`, `else`)
A turma trabalhou na resolução de exercícios de tomada de decisão:
- **Lógica de Múltiplos Ramos:** Construção de encadeamentos condicionais para cálculo de médias, descontos e validação de permissões.
- **Gaveta de Hotel e Lixo de Memória:** Vinícius alertou que variáveis não inicializadas em C contêm valores residuais deixados por outros programas que usaram aquele endereço de memória anteriormente.

---

## Glossario
- **Operador de Endereço (&)**: Operador unário que obtém a localização física de uma variável na memória RAM [Wikipedia](https://pt.wikipedia.org/wiki/Ponteiro_(programa%C3%A7%C3%A3o)).
- **scanf**: Função da biblioteca padrão de C para leitura formatada de dados a partir da entrada padrão (teclado).
- **Segmentation Fault**: Erro gerado pelo sistema operacional quando um programa tenta ler ou gravar em um endereço de memória não autorizado.
- **Lixo de Memória**: Conteúdo residual imprevisível presente em endereços de memória não inicializados.
"""
    },
    {
        "file_sem": SEMANAL_DIR / "W_01/outros_01.md",
        "file_est": ESTRUT_DIR / "2026-08-14_sex_fred.md",
        "content": """---
tipo: portal
titulo: "Outros - Aula 01"
disciplina: "Outros"
semestre: "2026.2"
data: 2026-08-14
professor: "Fred (Coordenação)"
---

Na sexta-feira, o coordenador Fred esteve presente em sala para uma sessão institucional de alinhamento com a turma de Análise e Desenvolvimento de Sistemas, trazendo novidades sobre a infraestrutura acadêmica e o corpo docente de 2026.2.

---

## 1. Consolidação do Corpo Docente CLT
O coordenador Fred anunciou uma reestruturação estratégica da faculdade para a área de tecnologia:
- **Quadro Permanente:** A instituição concluiu o processo seletivo e formalizou a contratação de 10 professores no regime CLT definitivo, eliminando a rotatividade de contratos temporários.
- **Docentes de Mercado:** Ressaltou que todos os professores contratados possuem atuação direta no mercado de TI, unindo rigor acadêmico aos desafios corporativos reais.

---

## 2. Diretrizes do Projeto Integrador e Apoio Acadêmico
- **Liderança no PI:** Foi confirmada a liderança do Professor Thiago na condução do Projeto Integrador, conectando banco de dados, lógica e programação de objetos em um projeto unificado.
- **Escuta com a Turma:** Fred abriu espaço para esclarecer dúvidas sobre os horários de sábado, laboratórios e cronograma de eventos do semestre.

---

## Glossario
- **Coordenação de Curso**: Órgão responsável pelo planejamento pedagógico, gestão de docentes e suporte acadêmico aos estudantes.
- **Regime CLT**: Modalidade formal de contratação de trabalho que assegura estabilidade e dedicação contínua ao corpo docente.
"""
    },

    # -------------------------------------------------------------
    # SEMANA 2 (W_02)
    # -------------------------------------------------------------
    {
        "file_sem": SEMANAL_DIR / "W_02/pi_01.md",
        "file_est": ESTRUT_DIR / "2026-08-17_seg_pi.md",
        "content": """---
tipo: portal
titulo: "Projeto Integrador - Aula 01"
disciplina: "Projeto Integrador"
semestre: "2026.2"
data: 2026-08-17
professor: "Thiago"
---

A aula inaugural de Projeto Integrador foi conduzida pelo Professor Thiago (mesmo docente da disciplina de CADAC no primeiro semestre). Thiago estabeleceu uma abordagem imersiva, posicionando-se como Gerente de Projetos e cliente exigente das equipes para simular o ambiente corporativo de software.

---

## 1. A Dinâmica de Gerência de Projetos
O Professor Thiago explicou que a disciplina não terá aulas teóricas expositivas no modelo convencional:
- **Cobrança por Demandas e Sprints:** Os grupos receberão metas e especificações periódicas, devendo entregar software funcional e documentação técnica.
- **Integração Real com Banco de Dados:** O sistema desenvolvido deverá aplicar a modelagem relacional orientada pelo Professor Alexandre e a lógica de backend em Java, C ou Python.
- **Do Papel para o Produto:** Projetos que ficarem apenas no plano teórico não serão aprovados; o software precisa rodar com persistência e telas.

---

## 2. Termo de Abertura do Projeto (TAP) e Gestão de Custos
Thiago introduziu a ferramenta formal de iniciação de projetos:
- **Estruturação do TAP:** Definição clara do escopo, objetivos de negócio, público-alvo e cronograma de marcos.
- **Custos Operacionais na Ponta do Lápis:** O professor destacou a necessidade de orçar horas de desenvolvimento, infraestrutura em nuvem e licenças de ferramentas para a construção do MVP (Mínimo Produto Viável).
- **Identificação de Stakeholders:** Mapeamento de todas as partes interessadas para evitar construir funcionalidades inúteis.

---

## 3. O Caso do Tribunal de Justiça (TJ)
Para ilustrar a gravidade de um escopo mal planejado, Thiago compartilhou sua vivência no Tribunal de Justiça:
- **Sistemas Desconectados da Ponta:** Projetos que consumiram milhões em recursos públicos mas que falharam ao entregar serviços básicos para a população (como a emissão online de certidões criminais), porque a equipe de desenvolvimento não ouviu o usuário final no início do projeto.

---

## Glossario
- **Termo de Abertura do Projeto (TAP)**: Documento formal que autoriza o início de um projeto, delimitando escopo, objetivos, custos e responsáveis [Wikipedia](https://pt.wikipedia.org/wiki/Termo_de_Abertura_do_Projeto).
- **Stakeholders**: Indivíduos, grupos ou organizações que possuem interesse ou são impactados pelas decisões do projeto [Wikipedia](https://pt.wikipedia.org/wiki/Stakeholder).
- **MVP (Mínimo Produto Viável)**: Versão funcional mais enxuta de um produto que permite testar hipóteses de negócio com usuários reais [Wikipedia](https://pt.wikipedia.org/wiki/Produto_vi%C3%A1vel_m%C3%ADnimo).
- **Projeto Integrador**: Eixo curricular de aplicação prática e integrada de múltiplos ramos da ciência da computação.
"""
    },
    {
        "file_sem": SEMANAL_DIR / "W_02/poo_02.md",
        "file_est": ESTRUT_DIR / "2026-08-18_ter_poo.md",
        "content": """---
tipo: portal
titulo: "Programação Orientada a Objetos - Aula 02"
disciplina: "Programação Orientada a Objetos"
semestre: "2026.2"
data: 2026-08-18
professor: "Tibério"
---

A segunda aula de POO com o Professor Tibério aprofundou a distinção prática entre Atributos (estado) e Métodos (comportamento) através de modelagens diretas no quadro e no computador.

---

## 1. Atributos vs. Métodos: O Caso da Lâmpada LED Inteligente
O Professor Tibério utilizou uma Lâmpada LED conectada para ensinar a arquitetura de uma classe:
- **Atributos de Estado:** Propriedades que guardam o estado atual do objeto (ex: `boolean ligada`, `String cor`, `int brilho`).
- **Métodos Operacionais:** Comandos que transformam e protegem esse estado (ex: `ligar()`, `desligar()`, `alterarCor()`).

```java
// Modelagem canônica da Lâmpada LED inteligente em Java
public class LampadaLED {
    // Atributos de estado (Privados)
    private boolean ligada;
    private String cor;
    private int brilho;

    public LampadaLED() {
        this.ligada = false;
        this.cor = "Branca";
        this.brilho = 100;
    }

    public void ligar() {
        this.ligada = true;
        System.out.println("Lâmpada ligada na cor " + this.cor);
    }

    public void desligar() {
        this.ligada = false;
        System.out.println("Lâmpada desligada.");
    }

    public void alterarCor(String novaCor) {
        if (this.ligada) {
            this.cor = novaCor;
            System.out.println("Cor alterada para: " + this.cor);
        } else {
            System.out.println("Erro: Não é possível mudar a cor de uma lâmpada apagada.");
        }
    }
}
```

---

## 2. Modelagem de Domínio: Veículo e Conta Bancária
A turma modelou classes de maior complexidade:
- **Classe Veículo:** Atributos de velocidade e marcha manipulados por métodos `acelerar()`, `frear()` e `trocarMarcha()`.
- **Classe Conta Bancária:** Encapsulamento de regras financeiras, garantindo que saques só ocorram se houver saldo suficiente, sem permitir que o saldo seja adulterado diretamente de fora.

---

## Glossario
- **Atributo**: Campo de dados de uma classe que armazena uma característica de estado do objeto [Wikipedia](https://pt.wikipedia.org/wiki/Atributo_(computa%C3%A7%C3%A3o)).
- **Método**: Sub-rotina associada a um objeto responsável por executar ações e manipular seu estado interno [Wikipedia](https://pt.wikipedia.org/wiki/M%C3%A9todo_(programa%C3%A7%C3%A3o)).
- **Instanciação**: Processo computacional de alocação de memória para a criação de um novo objeto a partir de sua classe.
- **Regra de Negócio**: Lógica que governa como os dados de um sistema podem ser criados, alterados e validados.
"""
    },
    {
        "file_sem": SEMANAL_DIR / "W_02/c_03.md",
        "file_est": ESTRUT_DIR / "2026-08-19_qua_c.md",
        "content": """---
tipo: portal
titulo: "Linguagem C - Aula 03"
disciplina: "Linguagem C"
semestre: "2026.2"
data: 2026-08-19
professor: "Vinícius"
---

A terceira aula de Linguagem C com o Professor Vinícius foi inteiramente dedicada à resolução intensiva de exercícios práticos de lógica no laboratório de informática, consolidando a escrita de algoritmos em C e o diagnóstico de mensagens do compilador.

---

## 1. Imersão Prática em Laboratório
O Professor Vinícius orientou os alunos a abrirem seus ambientes locais de desenvolvimento:
- **Metodologia Hands-on:** O aprendizado ocorreu diretamente no editor de código, enfrentando os bloqueios de sintaxe e ajustando a lógica a cada compilação.
- **Atendimento Individual nas Bancadas:** Vinícius percorreu a sala esclarecendo dúvidas sobre escopo de variáveis, precedência de operadores matemáticos e formatação com `printf`.

```c
#include <stdio.h>

int main(void) {
    int base = 0, altura = 0;
    float area = 0.0f;

    printf("Calculadora de Área de Retângulo\\n");
    printf("Digite a base: ");
    scanf("%d", &base);

    printf("Digite a altura: ");
    scanf("%d", &altura);

    if (base > 0 && altura > 0) {
        area = (float)(base * altura);
        printf("Área calculada com sucesso: %.2f unidades²\\n", area);
    } else {
        printf("Dimensões inválidas. Os valores devem ser estritamente positivos.\\n");
    }

    return 0;
}
```

---

## 2. Diagnóstico de Erros Comuns de Compilação
- **Ponto-e-Vírgula e Chaves:** Identificação de falhas de fechamento de blocos de código.
- **Casting Explícito:** Uso de `(float)` para evitar divisão inteira truncada em cálculos decimais.

---

## Glossario
- **Casting (Coerção de Tipo)**: Conversão explícita de um dado de um tipo para outro tipo na memória [Wikipedia](https://pt.wikipedia.org/wiki/Coer%C3%A7%C3%A3o_de_tipos).
- **Escopo de Variável**: Região do código fonte onde uma determinada variável é visível e acessível.
- **Precedência de Operadores**: Regras formais que determinam a ordem de avaliação de expressões matemáticas e lógicas [Wikipedia](https://pt.wikipedia.org/wiki/Ordem_de_opera%C3%A7%C3%B5es).
"""
    },
    {
        "file_sem": SEMANAL_DIR / "W_02/c_04.md",
        "file_est": ESTRUT_DIR / "2026-08-20_qui_c.md",
        "content": """---
tipo: portal
titulo: "Linguagem C - Aula 04"
disciplina: "Linguagem C"
semestre: "2026.2"
data: 2026-08-20
professor: "Vinícius"
---

A quarta aula de Linguagem C com o Professor Vinícius foi marcada por uma intervenção técnica objetiva no início da aula para simplificar a resolução da lista de exercícios de tomada de decisão.

---

## 1. Otimização Lógica: Operadores `&&` e `||`
O Professor Vinícius relatou que resolveu a lista de exercícios na véspera e percebeu que os alunos estavam se complicando ao aninhar múltiplos blocos `if` desnecessários:
- **Operador Lógico E (`&&`):** Exige que todas as condições sejam simultaneamente verdadeiras para autorizar o bloco.
- **Operador Lógico OU (`||`):** Basta que uma das condições seja verdadeira para disparar a execução.
- **Comparativo com Python e Ensino Médio:** Fez a ponte com a sintaxe `and` / `or` do Python e com a tabela-verdade da lógica proposicional.

```c
#include <stdio.h>

int main(void) {
    int valor = 0;

    printf("Digite um número inteiro: ");
    scanf("%d", &valor);

    // Validação elegante de intervalo em linha única
    if (valor >= 10 && valor <= 50) {
        printf("O valor %d está DENTRO do intervalo permitido [10, 50].\\n", valor);
    } else if (valor < 0 || valor > 100) {
        printf("Alerta: O valor %d é um caso extremo (< 0 ou > 100).\\n", valor);
    } else {
        printf("O valor %d está fora do intervalo principal.\\n", valor);
    }

    return 0;
}
```

---

## 2. Resolução da Lista em Sala
Com o reforço dos operadores lógicos, a turma prosseguiu na resolução dos problemas de intervalos numéricos e validações complexas com código mais limpo e conciso.

---

## Glossario
- **Operador Lógico E (&&)**: Conjunção lógica em C que retorna verdadeiro apenas se ambos os operandos forem verdadeiros [Wikipedia](https://pt.wikipedia.org/wiki/Conjun%C3%A7%C3%A3o_l%C3%B3gica).
- **Operador Lógico OU (||)**: Disjunção lógica em C que retorna verdadeiro se ao menos um dos operandos for verdadeiro [Wikipedia](https://pt.wikipedia.org/wiki/Disjun%C3%A7%C3%A3o_l%C3%B3gica).
- **Tabela-Verdade**: Tabela matemática utilizada na lógica booleana para mapear os resultados de operações lógicas [Wikipedia](https://pt.wikipedia.org/wiki/Tabela-verdade).
"""
    },
    {
        "file_sem": SEMANAL_DIR / "W_02/bd_01.md",
        "file_est": ESTRUT_DIR / "2026-08-21_sex_bd.md",
        "content": """---
tipo: portal
titulo: "Banco de Dados Relacional - Aula 01"
disciplina: "Banco de Dados Relacional"
semestre: "2026.2"
data: 2026-08-21
professor: "Alexandre"
---

A primeira aula de Banco de Dados Relacional com o Professor Alexandre funcionou como uma sessão de mentoria técnica e alinhamento de escopos de modelagem para os projetos do semestre.

---

## 1. Mentoria de Dados e Modelagem Conceitual
O Professor Alexandre atendeu as equipes de projeto para estruturar a base de dados relacional:
- **Cultura de Tirar Dúvidas:** Alexandre incentivou os alunos a utilizarem o horário presencial para sanar dúvidas conceituais antes de criarem tabelas e scripts SQL.
- **Alinhamento com o Semestre Passado:** Foi resgatada a experiência dos alunos no 1º semestre, identificando os principais erros cometidos em modelagem e entregas de dados para evitar reincidência.

---

## 2. Refinamento de Escopo Relacional
- **Foco no Núcleo de Dados:** O professor orientou os grupos a cortarem complexidades secundárias e priorizarem um esquema relacional consistente, com entidades e chaves bem definidas.
- **Preparação para os Sábados:** Alinhamento das demandas de modelagem que serão integradas às atividades de extensão e de projeto nos encontros de sábado.

---

## Glossario
- **Banco de Dados Relacional**: Sistema de armazenamento estruturado em tabelas com chaves primárias e relacionamentos [Wikipedia](https://pt.wikipedia.org/wiki/Banco_de_dados_relacional).
- **Modelo Relacional**: Teoria matemática de representação de dados baseada em relações formulada por Edgar F. Codd [Wikipedia](https://pt.wikipedia.org/wiki/Modelo_relacional).
- **Normalização**: Técnica de estruturação de tabelas para minimizar redundâncias e dependências anômalas [Wikipedia](https://pt.wikipedia.org/wiki/Normaliza%C3%A7%C3%A3o_de_dados).
"""
    },
    {
        "file_sem": SEMANAL_DIR / "W_02/extensao_01.md",
        "file_est": ESTRUT_DIR / "2026-08-22_sab_extensao.md",
        "content": """---
tipo: portal
titulo: "Projeto de Extensão - Aula 01"
disciplina: "Projeto de Extensão"
semestre: "2026.2"
data: 2026-08-22
professor: "Docente Titular"
---

O sábado letivo consolidou o encerramento da segunda semana de 2026.2 com foco na formação oficial das equipes do Projeto de Extensão e no planejamento das atividades comunitárias e tecnológicas integradas.

---

## 1. Organização das Equipes de Extensão
A turma formalizou a estrutura dos grupos de trabalho:
- **A Regra dos Grupos de 4 Integrantes:** Definição de equipes com cerca de quatro alunos para garantir equilíbrio na divisão de tarefas entre documentação, contato com a comunidade, desenvolvimento de software e banco de dados.
- **Histórico do 1º Semestre:** A turma relembrou a dinâmica das aulas de sábado do semestre anterior (conduzidas pelos professores Bruno Julins e Alexandre à noite), calibrando o ritmo para este semestre.

---

## 2. Planejamento e Canais de Comunicação
- **Distribuição de Papéis:** Cada integrante assumiu uma frente clara de atuação no projeto.
- **Fechamento dos Acordos:** Definição de repositórios no GitHub e cronograma de entregas quinzenais para as atividades de extensão.

---

## Glossario
- **Projeto de Extensão**: Ação acadêmica que articula o ensino universitário com a aplicação prática de soluções em benefício da sociedade [Wikipedia](https://pt.wikipedia.org/wiki/Extens%C3%A3o_universit%C3%A1ria).
- **Divisão de Responsabilidades**: Prática de engenharia de software onde tarefas de frontend, backend, banco e gestão são distribuídas de forma transparente na equipe.
"""
    }
]

for item in aulas_gold:
    with open(item["file_sem"], "w", encoding="utf-8") as f:
        f.write(item["content"].strip() + "\n")
    with open(item["file_est"], "w", encoding="utf-8") as f:
        f.write(item["content"].strip() + "\n")

print("✨ Todas as 10 aulas reconstruídas no Gold Standard com blocos de código e tópicos profundos!")
