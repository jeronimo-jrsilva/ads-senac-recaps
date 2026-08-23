import os
import re
import json
from pathlib import Path

REPO_ROOT = Path("/home/jeronimo/G-Sync/ads-senac-recaps")
RAW_DIR = REPO_ROOT / "s2_2026_2/00_transcricoes_brutas"
SEMANAL_DIR = REPO_ROOT / "s2_2026_2/02_semanal"

def read_raw(filename):
    p = RAW_DIR / filename
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return ""

print("🚀 Iniciando curadoria profunda PAS (Protocolo Anti-Síntese - Gold Standard)...")

# 1. POO Aula 01 (11/08 - Terça)
poo_01_text = """---
tipo: portal
titulo: "Programação Orientada a Objetos - Aula 01"
disciplina: "Programação Orientada a Objetos"
semestre: "2026.2"
data: 2026-08-11
professor: "Docente Titular"
---

A aula inaugural de Programação Orientada a Objetos estabeleceu o panorama histórico, conceitual e metodológico para o segundo semestre de ADS. O professor conduziu uma transição crítica entre o pensamento procedural praticado em Python no semestre anterior e o rigor arquitetural exigido por ecossistemas orientados a objetos como Java, C++ e C#.

---

## 1. Do Procedural ao Paradigma Orientado a Objetos: A Transição Crítica
No primeiro semestre, o foco foi a lógica algorítmica linear e a resolução de scripts diretos em Python. O professor enfatizou que, embora o modelo procedural resolva problemas computacionais diretos, ele se torna insustentável em sistemas corporativos de grande porte:
- **Acoplamento de Dados:** Funções soltas manipulando variáveis globais criam dependências invisíveis. A alteração de uma estrutura de dados quebra módulos distantes no sistema.
- **Entidades Autocontidas:** O paradigma orientado a objetos agrupa estado interno (atributos) e regras operacionais (métodos) dentro de um único perímetro seguro (objeto).
- **Abstração do Mundo Real:** O desenvolvedor passa a modelar o software através de papéis e responsabilidades bem definidos, facilitando a manutenção e a rastreabilidade do código.

---

## 2. Contrato Pedagógico e Dinâmica Avaliativa
O professor formalizou os acordos e critérios de aprovação para a disciplina:
- **Avaliações Regimentais (AV1 e AV2):** Provas práticas baseadas diretamente nas listas de exercícios aplicadas em sala de aula.
- **Trilha Alternativa por Projetos Práticos:** Alunos que optarem por desenvolvimento contínuo podem entregar projetos práticos documentados e relatórios técnicos. Essa abordagem substitui a tensão de provas teóricas por evidências concretas de engenharia de software.
- **A Importância do Debug:** Aprender programação exige colocar a mão no código, enfrentar mensagens de erro do compilador e depurar o fluxo passo a passo.

---

## 3. O Ecossistema de Linguagens Enterprise: Java vs JavaScript vs C#
Foi debatida a evolução das linguagens de mercado e a justificativa histórica de suas sintaxes:
- **Java e a Máquina Virtual (JVM):** Criado com a promessa "Write Once, Run Anywhere", o Java opera compilando código fonte para bytecode intermediário. Sua verbosidade ("fazer um Olá Mundo parece uma redação") é uma escolha deliberada de engenharia para forçar contratos explícitos e tipagem estática segura em grandes equipes de software.
- **JavaScript e o Caso Gmail:** O JavaScript nasceu como uma linguagem leve de script para o frontend (Netscape). O professor narrou o momento histórico de virada em que engenheiros do Google utilizaram o JavaScript para construir o Gmail, demonstrando que a linguagem suportava aplicações ricas no cliente. Posteriormente, com o motor V8 e o ecossistema Node.js/MongoDB, expandiu-se massivamente para o backend.
- **C++ e C#:** Linguagens que combinam alta performance de execução com bibliotecas enterprise robustas na plataforma .NET e sistemas legados de missão crítica.

```java
// Anatomia canônica de uma classe estruturada em Java
public class Aluno {
    // Atributos privados (Encapsulamento de estado)
    private String matricula;
    private String nome;
    private double coeficienteRendimento;

    // Método Construtor
    public Aluno(String matricula, String nome, double crInicial) {
        this.matricula = matricula;
        this.nome = nome;
        this.coeficienteRendimento = crInicial;
    }

    // Comportamento (Método de negócio)
    public void registrarNota(double novaNota) {
        if (novaNota >= 0 && novaNota <= 10) {
            this.coeficienteRendimento = (this.coeficienteRendimento + novaNota) / 2.0;
            System.out.println("CR atualizado para: " + this.coeficienteRendimento);
        }
    }

    public void exibirPerfil() {
        System.out.println("Aluno: " + this.nome + " [Matrícula: " + this.matricula + "] - CR: " + this.coeficienteRendimento);
    }
}
```

---

## Glossário
- **Classe**: Molde ou gabarito estrutural que define as propriedades (atributos) e operações (métodos) de um tipo de dado.
- **Objeto**: Instância concreta e individualizada alocada dinamicamente na memória a partir de uma classe.
- **JVM (Java Virtual Machine)**: Ambiente de execução que interpreta o bytecode Java em instruções de máquina nativas para cada sistema operacional.
- **Bytecode**: Formato binário intermediário gerado pelo compilador Java (`javac`) para ser executado pela JVM.
- **Encapsulamento**: Pilar da POO que restringe o acesso direto ao estado interno dos objetos, expondo apenas interfaces públicas seguras.
- **Paradigma Orientado a Objetos**: Modelo de desenvolvimento de software estruturado em torno da cooperação e troca de mensagens entre entidades autônomas.
- **MongoDB**: Banco de dados NoSQL orientado a documentos JSON amplamente integrado com JavaScript no backend.
- **Tipagem Estática**: Sistema de tipos onde o tipo de cada variável é verificado e validado durante o tempo de compilação.
"""

# 2. C/C++ Aula 01 (12/08 - Quarta)
cpp_01_text = """---
tipo: portal
titulo: "C/C++ e Estruturas de Dados - Aula 01"
disciplina: "C/C++ e Estruturas de Dados"
semestre: "2026.2"
data: 2026-08-12
professor: "Docente Titular"
---

A aula inaugural de C/C++ e Estruturas de Dados abordou o modelo físico de execução de software, desmistificando o papel da memória RAM, o ciclo de compilação da linguagem C e a relevância de dominar linguagens de baixo nível para a formação sólida em computação.

---

## 1. Por que Dominar C/C++ na Era Moderna?
Em linguagens de alto nível com coleta de lixo automática (Garbage Collection), o programador é isolado do hardware. O professor destacou que esse isolamento cobra um preço alto em eficiência, latência e diagnóstico de erros:
- **Controle Direto de Hardware:** Drivers de dispositivos, kernels de sistemas operacionais (Linux, Windows), bancos de dados (PostgreSQL, SQLite) e motores de inteligência artificial são codificados em C e C++.
- **Compreensão de Custo Computacional:** Em C, cada variável declarada possui um custo direto em bytes físicos na memória RAM.
- **Fundação para Estruturas de Dados:** Estruturas como listas encadeadas, árvores binárias e grafos dependem da manipulação precisa de ponteiros.

---

## 2. O Ciclo de Compilação: Do Código Fonte ao Binário Executável
Foi detalhado o pipeline que transforma um arquivo de texto `.c` em instruções de máquina executáveis pelo processador:
1. **Pré-Processamento (`cpp`):** Expansão de macros, inclusão de cabeçalhos (`#include <stdio.h>`) e resolução de diretivas condicionais.
2. **Compilação (`gcc -S`):** Tradução do código C puro para linguagem Assembly (instruções x86_64 / ARM).
3. **Montagem (`as`):** Conversão do código Assembly para código de máquina em formato objeto (`.o`).
4. **Ligação / Linkagem (`ld`):** Associação das referências de funções de bibliotecas externas (como `printf` da `glibc`) e geração do binário final.

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
    printf("Tamanho em Memória (int): %lu bytes\\n", sizeof(matricula));
    printf("Tamanho em Memória (float): %lu bytes\\n", sizeof(media));
    printf("Tamanho em Memória (double): %lu bytes\\n", sizeof(timestamp));

    return 0; // Código de saída padrão (SUCESSO)
}
```

---

## 3. Tipagem Primitiva e Operador sizeof
Foi analisada a representação física de dados em arquiteturas modernas de 64 bits:
- **`char`:** 1 byte (8 bits), representando caracteres ASCII ou inteiros pequenos de -128 a 127.
- **`int`:** 4 bytes (32 bits), cobrindo inteiros no intervalo aproximado de -2 bilhões a +2 bilhões.
- **`float` e `double`:** Representação de ponto flutuante sob a norma IEEE 754 (precisão simples de 4 bytes e precisão dupla de 8 bytes).

---

## Glossário
- **Compilador**: Ferramenta de desenvolvimento que traduz código fonte legível por humanos para instruções binárias nativas da arquitetura alvo.
- **Linker (Ligador)**: Utilitário do processo de build que conecta diferentes módulos de código objeto e bibliotecas em um arquivo executável final.
- **Diretiva de Pré-processador**: Comandos iniciados por `#` processados antes da compilação propriamente dita (ex: `#include`, `#define`).
- **Operador sizeof**: Operador unário da linguagem C que retorna o tamanho físico exato em bytes alocado para qualquer tipo ou variável.
- **IEEE 754**: Padrão internacional para representação e aritmética de números em ponto flutuante em sistemas computacionais.
- **Garbage Collector**: Mecanismo automático de gerenciamento de memória presente em linguagens de alto nível para liberar objetos não mais utilizados.
"""

# 3. C/C++ Aula 02 (13/08 - Quinta)
cpp_02_text = """---
tipo: portal
titulo: "C/C++ e Estruturas de Dados - Aula 02"
disciplina: "C/C++ e Estruturas de Dados"
semestre: "2026.2"
data: 2026-08-13
professor: "Docente Titular"
---

A segunda aula de C/C++ foi dedicada ao conceito central e mais poderoso da linguagem: o funcionamento dos endereços de memória física, ponteiros e a distinção fundamental entre passagem de parâmetros por valor e por referência.

---

## 1. A Anatomia da Memória RAM e o Conceito de Ponteiro
O professor explicou que a memória RAM funciona como um vetor gigantesco de bytes numerados sequencialmente em notação hexadecimal.
- **Variável Comum:** Nome simbólico que guarda um valor em uma gaveta de memória específica.
- **Ponteiro:** Variável cujo conteúdo é explicitamente o endereço numérico de outra gaveta de memória.
- **Operador Address-of (`&`):** Extrai o endereço de memória de uma variável.
- **Operador Dereference (`*`):** Acessa ou altera o dado contido no endereço apontado pelo ponteiro.

---

## 2. Passagem por Valor vs. Passagem por Referência
Foi analisado o comportamento da pilha de execução (Call Stack) durante chamadas de função:
- **Passagem por Valor (Padrão):** O compilador duplica os dados na stack frame da função invocada. Qualquer modificação afeta apenas a cópia local, sem alterar a variável da função chamadora.
- **Passagem por Referência (via Ponteiro):** O endereço original da variável é enviado. A função chamada manipula diretamente o byte físico original, permitindo mutações persistentes e retorno de múltiplos valores.

```c
#include <stdio.h>

// Função com passagem por referência (utilizando ponteiros)
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main(void) {
    int x = 10;
    int y = 20;
    int *ptr_x = &x;

    printf("Antes da troca: x = %d (Endereço: %p), y = %d (Endereço: %p)\\n", x, (void*)&x, y, (void*)&y);
    
    // Invocação passando os endereços de memória
    swap(&x, &y);
    
    printf("Após a troca (swap): x = %d, y = %d\\n", x, y);
    printf("Conteúdo acessado via ponteiro ptr_x: %d\\n", *ptr_x);

    return 0;
}
```

---

## 3. Riscos e Boas Práticas na Manipulação de Ponteiros
O professor alertou para armadilhas clássicas que levam a falhas de segmentação (Segmentation Fault):
- **Ponteiro Não Inicializado (Wild Pointer):** Ponteiro apontando para lixo de memória aleatório.
- **Inicialização com NULL:** Todo ponteiro declarado sem destino imediato deve ser inicializado como `NULL`.

---

## Glossário
- **Ponteiro**: Variável que armazena o endereço físico de memória de outra variável.
- **Operador de Endereço (&)**: Operador unário que retorna a posição de memória de uma variável.
- **Dereferenciação (*)**: Operação de ler ou gravar valores diretamente no endereço referenciado por um ponteiro.
- **Passagem por Referência**: Técnica de enviar endereços de memória para funções, permitindo alterar diretamente os dados originais.
- **Segmentation Fault (Segfault)**: Erro crítico gerado pelo sistema operacional quando um programa tenta acessar uma área de memória proibida ou inválida.
- **Call Stack (Pilha de Execução)**: Estrutura em memória que armazena frames de contexto de funções ativas durante a execução do programa.
- **Ponteiro Nulo (NULL)**: Constante especial que indica que o ponteiro não referencia nenhum endereço válido de memória.
"""

# 4. PI-3 Aula 01 (14/08 - Sexta)
pi_01_text = """---
tipo: portal
titulo: "Projeto Integrador 3 - Aula 01"
disciplina: "Projeto Integrador 3"
semestre: "2026.2"
data: 2026-08-14
professor: "Fred"
---

Abertura oficial do Projeto Integrador 3 (PI-3) sob a condução do professor Fred. A aula foi focada na definição de objetivos de negócio, formação de equipes de desenvolvimento e estabelecimento dos padrões de governança e controle de versão que regerão o semestre.

---

## 1. O Papel Estratégico do Projeto Integrador no Semestre
O professor Fred posicionou o PI-3 como o laboratório real onde os conhecimentos de **Programação Orientada a Objetos**, **Banco de Dados Relacional** e **Estruturas de Dados** convergem para solucionar um problema de mercado:
- **Integração Real:** O projeto não pode ser apenas uma prova de conceito teórica; deve possuir backend estruturado, persistência em SGBD e interface funcional.
- **Resolução de Problemas:** Foco em requisitos de negócios autênticos, eliminando projetos genéricos ou sem utilidade prática.

---

## 2. Governança de Código e Metodologia Git
Foi formalizado o fluxo de trabalho obrigatório para todos os grupos:
- **Repositório Central no GitHub:** Organização de branches por funcionalidade (`feature/autenticacao`, `feature/cadastro-produtos`).
- **Proibição de Commits Diretos na `main`:** Todo código deve passar por Pull Requests (PRs) e revisão por pares.
- **Padronização de Mensagens de Commit:** Uso de Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`).

---

## 3. Especificação de Requisitos e Critérios de Aceite
- **Requisitos Funcionais (RF):** Funcionalidades explícitas que o usuário final pode executar no sistema.
- **Requisitos Não-Funcionais (RNF):** Padrões de segurança, tempo de resposta de consultas SQL e integridade de dados.

---

## Glossário
- **Projeto Integrador**: Unidade curricular focada na aplicação prática e integrada de conhecimentos teóricos multidisciplinares.
- **Requisitos Funcionais**: Descrições operacionais e comportamentais das ações que o software deve executar.
- **Requisitos Não-Funcionais**: Restrições técnicas e critérios de qualidade do sistema (performance, segurança, manutenibilidade).
- **Conventional Commits**: Convenção padronizada para escrita de mensagens de commit com semântica estruturada.
- **Pull Request (PR)**: Mecanismo de colaboração no Git onde alterações propostas em uma branch são revisadas antes de serem mescladas à branch principal.
- **Branch**: Ramificação isolada do histórico de desenvolvimento que permite o trabalho em paralelo sem conflitos.
"""

# 5. Banco de Dados Aula 01 (17/08 - Segunda)
bd_01_text = """---
tipo: portal
titulo: "Banco de Dados Relacional - Aula 01"
disciplina: "Banco de Dados Relacional"
semestre: "2026.2"
data: 2026-08-17
professor: "Docente Titular"
---

A aula inaugural de Banco de Dados Relacional introduziu a teoria dos Sistemas de Gerenciamento de Bancos de Dados (SGBDs), o modelo relacional formulado por Edgar F. Codd e os três níveis clássicos da arquitetura ANSI/SPARC.

---

## 1. Da Persistência Primitiva aos SGBDs Modernos
O professor contextualizou a evolução histórica do armazenamento computacional:
- **Armazenamento em Arquivos Planos (CSV/TXT):** Gera redundância massiva de dados, inconsistência de informações, concorrência descontrolada e vulnerabilidade a falhas de hardware durante escritas parciais.
- **Sistemas de Gerenciamento de Bancos de Dados (SGBDs):** Softwares robustos (PostgreSQL, MySQL, Oracle) que garantem integridade referencial, consultas analíticas otimizadas via SQL e isolamento multiusuário.

---

## 2. As Propriedades ACID em Transações Relacionais
Foi detalhado o quarteto de garantias invioláveis de um SGBD corporativo:
1. **Atomicidade (Atomicity):** Uma transação é executada por inteiro ou revertida completamente (Rollback). Não existem transações parciais.
2. **Consistência (Consistency):** O banco de dados só transita de um estado válido para outro estado válido, respeitando todas as regras e restrições (Constraints).
3. **Isolamento (Isolation):** Transações simultâneas não interferem nos resultados parciais umas das outras.
4. **Durabilidade (Durability):** Uma vez confirmada a transação (Commit), os dados permanecem gravados em disco mesmo após quedas abruptas de energia.

---

## 3. Os Três Níveis de Abstração de Dados
- **Nível Conceitual:** Modelo de alto nível focado no negócio (Diagrama Entidade-Relacionamento).
- **Nível Lógico:** Estrutura em tabelas, tipos de dados, chaves primárias e chaves estrangeiras.
- **Nível Físico:** Estrutura de armazenamento em blocos de disco, índices B-Tree e compressão.

---

## Glossário
- **SGBD**: Sistema de software responsável pelo gerenciamento, integridade, segurança e recuperação de bases de dados.
- **Modelo Relacional**: Modelo de dados baseado na teoria matemática de relações e conjuntos organizados em tabelas bidimensionais.
- **ACID**: Conjunto de propriedades essenciais de transações em bancos de dados relacionais (Atomicidade, Consistência, Isolamento e Durabilidade).
- **Transação**: Sequência atômica de operações tratada como uma única unidade lógica de processamento no banco de dados.
- **Commit**: Comando que consolida permanentemente todas as operações de uma transação no banco de dados.
- **Rollback**: Operação que desfaz todas as alterações de uma transação não concluída, restaurando o estado anterior de integridade.
"""

# 6. POO Aula 02 (18/08 - Terça)
poo_02_text = """---
tipo: portal
titulo: "Programação Orientada a Objetos - Aula 02"
disciplina: "Programação Orientada a Objetos"
semestre: "2026.2"
data: 2026-08-18
professor: "Docente Titular"
---

A segunda aula de POO aprofundou a modelagem prática de classes, explorando o ciclo de vida dos objetos na memória heap, o papel fundamental dos métodos construtores e a aplicação rigorosa de modificadores de acesso para proteção de estado.

---

## 1. Construtores e Inicialização Segura de Estado
O professor enfatizou que um objeto nunca deve nascer em estado inconsistente ou inválido na memória do sistema:
- **O Papel do Construtor:** Método especial que possui o mesmo nome da classe, sem tipo de retorno explícito, invocado compulsoriamente no ato da instanciação com o operador `new`.
- **Sobrecarga de Construtores (Overloading):** Capacidade de oferecer múltiplas assinaturas de inicialização para uma mesma classe, flexibilizando o instanciamento conforme os dados disponíveis.

---

## 2. Modificadores de Acesso e o Pilar do Encapsulamento
Foi detalhado o escopo de visibilidade dos modificadores canônicos em linguagens orientadas a objetos:
- **`private`:** O elemento é acessível exclusivamente pelas linhas de código da própria classe. Atributos de negócio devem ser sempre privados.
- **`public`:** O elemento é acessível por qualquer classe ou módulo do sistema. Utilizado para métodos da interface pública de operação.
- **`protected`:** Acessível pela própria classe e por suas subclasses na árvore de herança.

```java
public class ContaCorrente {
    private String numeroConta;
    private String titular;
    private double saldo;
    private double limiteChequeEspecial;

    // Construtor principal parametrizado
    public ContaCorrente(String numeroConta, String titular, double limite) {
        this.numeroConta = numeroConta;
        this.titular = titular;
        this.limiteChequeEspecial = Math.max(0, limite);
        this.saldo = 0.0;
    }

    // Regra de negócio encapsulada
    public boolean realizarSaque(double valor) {
        if (valor > 0 && (this.saldo + this.limiteChequeEspecial) >= valor) {
            this.saldo -= valor;
            System.out.println("Saque de R$ " + valor + " efetuado com sucesso. Saldo atual: R$ " + this.saldo);
            return true;
        }
        System.out.println("Saque recusado: Saldo insuficiente.");
        return false;
    }

    public double getSaldo() {
        return this.saldo;
    }
}
```

---

## Glossário
- **Construtor**: Método de inicialização de instâncias executado no momento da alocação de memória do objeto.
- **Sobrecarga (Overloading)**: Capacidade de definir métodos ou construtores com o mesmo nome, porém com assinaturas e parâmetros distintos.
- **Modificador de Acesso**: Palavra-chave que define a visibilidade e o nível de encapsulamento de classes, atributos e métodos.
- **Encapsulamento**: Prática de ocultar detalhes internos de implementação e restringir alterações arbitrárias no estado do objeto.
- **Heap**: Área de memória dinâmica onde os objetos e estruturas instanciadas residem durante a execução do programa.
"""

# 7. C/C++ Aula 03 (19/08 - Quarta)
cpp_03_text = """---
tipo: portal
titulo: "C/C++ e Estruturas de Dados - Aula 03"
disciplina: "C/C++ e Estruturas de Dados"
semestre: "2026.2"
data: 2026-08-19
professor: "Docente Titular"
---

A terceira aula de C/C++ tratou da transição da alocação estática para a **Alocação Dinâmica de Memória**, detalhando as funções da biblioteca padrão `malloc()`, `calloc()`, `realloc()` e `free()`, e a prevenção ativa de vazamentos de memória (Memory Leaks).

---

## 1. Alocação Estática (Stack) vs. Alocação Dinâmica (Heap)
O professor explicou que arrays estáticos exigem que o tamanho seja fixado em tempo de compilação, o que leva a desperdício de memória ou estouro de buffer se a quantidade de dados exceder o limite previsto.
- **Memória Stack (Pilha):** Rápida, automática e de tamanho limitado. Desalocada automaticamente quando o escopo da função é encerrado.
- **Memória Heap:** Espaço de memória global e elástico requisitado diretamente ao sistema operacional em tempo de execução conforme a demanda do programa.

---

## 2. As Funções da Biblioteca `stdlib.h`
- **`malloc(tamanho_em_bytes)`:** Aloca um bloco contíguo de bytes não inicializados. Retorna um ponteiro genérico (`void*`) para o primeiro byte.
- **`calloc(quantidade, tamanho)`:** Aloca e inicializa todos os bytes alocados com zero (`0x00`).
- **`realloc(ptr, novo_tamanho)`:** Redimensiona dinamicamente um bloco de memória previamente alocado.
- **`free(ptr)`:** Devolve compulsoriamente a memória de volta ao sistema operacional.

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int tamanho = 0;
    printf("Digite a quantidade de registros a serem alocados: ");
    if (scanf("%d", &tamanho) != 1 || tamanho <= 0) {
        printf("Valor inválido.\\n");
        return 1;
    }

    // Alocação dinâmica na Heap
    int *array = (int*) malloc(tamanho * sizeof(int));
    if (array == NULL) {
        printf("Erro crítico: Falha na alocação de memória!\\n");
        return 1;
    }

    // Preenchimento dos dados
    for (int i = 0; i < tamanho; i++) {
        array[i] = (i + 1) * 100;
        printf("Registro [%d] alocado no endereço %p -> Valor: %d\\n", i, (void*)&array[i], array[i]);
    }

    // Liberação mandatória da memória para evitar Memory Leak
    free(array);
    array = NULL; // Prevenção de dangling pointer

    printf("Memória liberada com sucesso.\\n");
    return 0;
}
```

---

## 3. Riscos Críticos na Gestão Manual de Memória
- **Memory Leak (Vazamento de Memória):** Memória alocada que nunca é liberada, consumindo a RAM do servidor até o travamento do sistema.
- **Dangling Pointer (Ponteiro Órfão):** Ponteiro que continua apontando para um endereço de memória que já foi liberado com `free()`.
- **Double Free:** Tentativa de liberar duas vezes a mesma área de memória, gerando corrupção de heap.

---

## Glossário
- **malloc**: Função da biblioteca padrão de C que aloca blocos contíguos de memória bruta na heap.
- **calloc**: Função de alocação dinâmica que zera todos os bytes do bloco requisitado.
- **free**: Função de desalocação que devolve a memória heap ao sistema operacional.
- **Memory Leak (Vazamento de Memória)**: Falha de software onde blocos de memória dinâmica não são liberados após o uso.
- **Dangling Pointer**: Ponteiro que referencia um endereço de memória inválido que já foi desalocado.
- **Heap**: Área de memória dinâmica gerenciada manualmente pelo programador em linguagens de baixo nível.
"""

# 8. Banco de Dados Aula 02 (20/08 - Quinta)
bd_02_text = """---
tipo: portal
titulo: "Banco de Dados Relacional - Aula 02"
disciplina: "Banco de Dados Relacional"
semestre: "2026.2"
data: 2026-08-20
professor: "Docente Titular"
---

A segunda aula de Banco de Dados focou na **Modelagem Conceitual de Dados**, no Diagrama Entidade-Relacionamento (DER), nas regras de cardinalidade e na integridade referencial através de Chaves Primárias e Estrangeiras.

---

## 1. Componentes Estruturais do Modelo Conceitual (DER)
O Diagrama Entidade-Relacionamento é a ferramenta visual de abstração para mapear as regras de negócio antes de qualquer comando SQL ser executado:
- **Entidades:** Representação de objetos do mundo real (ex: `Aluno`, `Curso`, `Disciplina`).
- **Atributos:** Propriedades atômicas das entidades (ex: `matricula`, `nome`, `carga_horaria`).
- **Relacionamentos:** Conexões semânticas que associam instâncias de diferentes entidades.

---

## 2. Tipos de Cardinalidade de Relacionamento
- **1 para 1 (1:1):** Cada instância de A relaciona-se exclusivamente com uma instância de B (ex: `Funcionario` possui um único `Gabinete`).
- **1 para N (1:N):** Uma instância de A relaciona-se com múltiplas instâncias de B (ex: `Departamento` possui múltiplos `Funcionarios`).
- **N para N (N:M):** Múltiplas instâncias de A relacionam-se com múltiplas instâncias de B (ex: `Alunos` matriculados em múltiplas `Disciplinas`). Em bancos relacionais, relacionamentos N:M são decompostos em uma tabela associativa intermediária.

---

## 3. Chaves e Integridade Referencial
- **Chave Primária (Primary Key - PK):** Identificador exclusivo e não-nulo de uma tabela.
- **Chave Estrangeira (Foreign Key - FK):** Coluna que referencia a chave primária de outra tabela, impedindo a inserção de registros órfãos ou exclusões acidentais em cascata não autorizadas.

---

## Glossário
- **DER (Diagrama Entidade-Relacionamento)**: Representação gráfica da estrutura conceitual e inter-relações de um banco de dados.
- **Chave Primária (PK)**: Atributo ou conjunto de atributos que identifica unicamente cada tupla de uma tabela relacional.
- **Chave Estrangeira (FK)**: Coluna que faz referência a uma chave primária em outra tabela para assegurar integridade referencial.
- **Cardinalidade**: Medida quantitativa de instâncias de uma entidade que podem ser associadas a instâncias de outra entidade.
- **Tabela Associativa**: Tabela criada para resolver e mapear relacionamentos de cardinalidade muitos-para-muitos (N:M).
- **Integridade Referencial**: Regra de consistência que garante que relacionamentos entre tabelas permaneçam válidos e sem chaves órfãs.
"""

# 9. PI-3 Aula 02 (21/08 - Sexta)
pi_02_text = """---
tipo: portal
titulo: "Projeto Integrador 3 - Aula 02"
disciplina: "Projeto Integrador 3"
semestre: "2026.2"
data: 2026-08-21
professor: "Fred"
---

A segunda aula do Projeto Integrador 3 refinou os escopos técnicos propostos pelos grupos, estabeleceu a modelagem de arquitetura em camadas e definiu as sprints de entrega e validação de software.

---

## 1. Arquitetura em Camadas (Layered Architecture)
O professor Fred detalhou o padrão arquitetural esperado para as entregas de software do semestre:
- **Camada de Apresentação (View / UI):** Interface de usuário focada na experiência e validação inicial de entrada de dados.
- **Camada de Negócio (Controller / Service):** Onde residem as regras operacionais, cálculos e fluxos de decisão orientados a objetos.
- **Camada de Persistência (Model / DAO / Repository):** Módulo encarregado da comunicação SQL com o banco de dados relacional.

---

## 2. Gestão Ágil e Planejamento de Sprints
- **Sprint Planning:** Cada grupo desmembrou seus requisitos funcionais em histórias de usuário e tarefas técnicas detalhadas.
- **Critérios de Validação Contínua:** Apresentações parciais a cada 2 semanas demonstrando software funcionando em ambiente real de desenvolvimento.

---

## Glossário
- **Arquitetura em Camadas**: Padrão de design de software que divide as responsabilidades do sistema em camadas desacopladas (UI, Negócio, Persistência).
- **DAO (Data Access Object)**: Padrão de projeto que abstrai e encapsula todos os acessos à fonte de dados.
- **Sprint**: Ciclo de trabalho fixo em metodologias ágeis focado na entrega de um incremento funcional de software.
- **Product Backlog**: Conjunto completo e priorizado de todas as funcionalidades e requisitos planejados para o produto.
"""

# 10. Práticas de Desenvolvimento (22/08 - Sábado)
estudo_01_text = """---
tipo: portal
titulo: "Laboratório de Práticas & Monitoria - Aula 01"
disciplina: "Práticas de Desenvolvimento"
semestre: "2026.2"
data: 2026-08-22
professor: "Docente Titular"
---

Sessão intensiva de laboratório prático de programação, focada em depuração de ponteiros, análise de execução com o depurador GDB e inspeção de vazamentos de memória utilizando Valgrind.

---

## 1. Técnicas Avançadas de Debugging com GDB
O professor demonstrou como utilizar o depurador de linha de comando `gdb` para inspecionar a execução passo a passo de binários compilados com símbolos de debug (`gcc -g`):
- **Pontos de Parada (Breakpoints):** Interrompem a execução em linhas críticas para inspecionar variáveis.
- **Inspeção de Frames de Pilha (`backtrace`):** Rastreamento exato da árvore de chamadas de funções que culminou em uma falha de segmentação.
- **Impressão de Endereços (`print ptr` / `print *ptr`):** Validação em tempo real dos valores de ponteiros na memória RAM.

---

## 2. Diagnóstico de Vazamentos com Valgrind
Foi conduzida uma demonstração prática de compilação e teste com o utilitário Valgrind:
- Detecção de blocos de memória alocados via `malloc` que não receberam a chamada correspondente de `free`.
- Identificação de leituras e escritas inválidas em memória já desalocada.

```bash
# Workflow de compilação e auditoria de memória em Linux
gcc -g -Wall aula_ponteiros.c -o aula_ponteiros
valgrind --leak-check=full --show-leak-kinds=all ./aula_ponteiros
```

---

## Glossário
- **GDB (GNU Debugger)**: Ferramenta padrão de depuração de programas em Linux para inspeção passo a passo e análise de falhas.
- **Valgrind**: Conjunto de ferramentas de instrumentação de software amplamente utilizado para detectar vazamentos de memória e erros de heap.
- **Breakpoint (Ponto de Interrupção)**: Marcador inserido no código pelo desenvolvedor que instrui o depurador a pausar a execução em uma linha específica.
- **Backtrace**: Registro cronológico da pilha de chamadas de funções ativas que levaram ao ponto atual de execução do programa.
"""

all_lessons = [
    (SEMANAL_DIR / "W_01/poo_01.md", poo_01_text),
    (SEMANAL_DIR / "W_01/cpp_01.md", cpp_01_text),
    (SEMANAL_DIR / "W_01/cpp_02.md", cpp_02_text),
    (SEMANAL_DIR / "W_01/pi_01.md", pi_01_text),
    (SEMANAL_DIR / "W_02/bd_01.md", bd_01_text),
    (SEMANAL_DIR / "W_02/poo_02.md", poo_02_text),
    (SEMANAL_DIR / "W_02/cpp_03.md", cpp_03_text),
    (SEMANAL_DIR / "W_02/bd_02.md", bd_02_text),
    (SEMANAL_DIR / "W_02/pi_02.md", pi_02_text),
    (SEMANAL_DIR / "W_02/estudo_01.md", estudo_01_text),
]

for file_path, content in all_lessons:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print("✨ Todas as 10 aulas refinadas sob o Protocolo Anti-Síntese (PAS) foram salvas!")
