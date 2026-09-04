---
tipo: portal
titulo: "Programação Orientada a Objetos - Aula 03"
disciplina: "Programação Orientada a Objetos"
semestre: "2026.2"
data: 2026-08-25
professor: "Tibério"
---

A terceira aula de **Programação Orientada a Objetos (POO)** com o Professor Tibério aprofundou a mecânica interna da JVM, o ciclo de vida de instâncias na memória e a fronteira entre dados voláteis e persistência em banco de dados.

---

## 1. Memória Volátil vs. Persistência de Dados
O Professor Tibério abriu o encontro esclarecendo a separação de responsabilidades arquiteturais:
- **Memória RAM (Volátil):** Onde os objetos em execução residem. Ao encerrar o processo da aplicação, todo o estado interno é destruído.
- **Camada de Persistência (Banco de Dados):** Onde as informações tornam-se perenes (tabelas, registros, integridade referencial). O professor pontuou que, embora a disciplina de Banco de Dados com o Professor Alexandre trate do modelo relacional, em POO é mandatório dominar como a linguagem organiza as referências antes da gravação no disco.

---

## 2. A Anatomia da JVM: Stack (Pilha) vs. Heap (Monte)
Um dos conceitos centrais fixados em sala foi a divisão de áreas de memória durante a criação de um objeto via operador `new`:

1. **Stack (Pilha de Execução):**
   - Armazena chamadas de métodos, variáveis primitivas locais e os **ponteiros de referência** (o endereço numérico onde o objeto real mora).
   - Gerenciamento rápido e automático (escopo de bloco).
2. **Heap (Monte de Memória):**
   - Espaço compartilhado onde os objetos são **materializados fisicamente** com todos os seus atributos.
   - O Garbage Collector monitora o Heap: quando nenhuma variável da Stack aponta para um endereço no Heap, o objeto torna-se elegível para coleta e liberação de memória.

```java
// Demonstração da divisão Stack vs. Heap
public class ExemploMemoria {
    public static void main(String[] args) {
        // 'nota' fica na Stack com valor 10
        int nota = 10;

        // 'servidor' é uma referência alocada na Stack
        // O objeto 'AtivoTI' completo nasce no Heap através do 'new'
        AtivoTI servidor = new AtivoTI(1, "PAT-8821", "Dell PowerEdge", "Ativo");
    }
}
```

---

## 3. A Fragilidade da Manipulação Direta e a Blindagem do Objeto
O docente retomou a comparação com a linguagem C:
- Em C, o uso indevido de ponteiros ou alocações manuais (`malloc`/`free`) pode corromper a memória de outros programas (*Segmentation Fault*).
- No Java, o desenvolvedor não gerencia ponteiros brutos diretamente, mas precisa garantir o **Encapsulamento Rígido**: privar os atributos de acesso público direto (`private`) para que regras de validação impeçam estados inconsistentes.

---

## 🚀 [Tópico Extra] Engenharia de Software & Compilação Profissional: Pacotes, `.class` e a Pasta `bin/`

> **Nota:** Este tópico aprofunda boas práticas de organização de projetos corporativos em Java. Em sala de aula, o professor compilou diretamente no terminal sem parâmetros adicionais, mas entender o que acontece nos bastidores evita bagunça e problemas clássicos de importação à medida que os projetos crescem.

---

### 🤔 1. Para que servem os arquivos `.class` e por que existe a pasta `bin/`?

* **O que são os arquivos `.class` (Bytecode)?**  
  O Java não gera executáveis nativos diretos da máquina (como `.exe` no Windows ou binários ELF no Linux). O compilador `javac` traduz o seu código legível (`.java`) em **Bytecode**, que são instruções intermediárias gravadas em arquivos com extensão `.class`. É esse arquivo `.class` que a JVM (*Java Virtual Machine*) lê, interpreta e executa via comando `java`.

* **Por que a pasta se chama `bin/`?**  
  A palavra **`bin`** é uma abreviação clássica do ecossistema Unix/Linux para **Binaries** (Binários/Executáveis). Em quase todos os sistemas e projetos de software (como `/usr/bin` no Linux, ou pastas de saída de IDEs como Eclipse, IntelliJ e VS Code), o diretório `bin/` ou `target/classes/` é a convenção padrão da indústria para abrigar tudo o que é **produto compilado**, mantendo o código-fonte original (`.java`) estritamente isolado.

---

### ⚖️ 2. Compilar Sem `-d` vs. Compilar Com `-d bin` (A Diferença Prática)

* **O que acontece sem `-d` (Modo Básico):**  
  Se você rodar apenas `javac Techlab/Main.java`, o compilador funcionará normalmente e criará os arquivos `.class` **jogados dentro da mesma pasta do código-fonte**. Isso funciona perfeitamente para testes rápidos, mas em projetos reais gera poluição visual, dificulta o controle de versão (`.gitignore`) e mistura arquivo de edição humana com arquivo de máquina.
* **O que acontece com `-d bin` (Modo Profissional):**  
  Ao passar o parâmetro `-d bin` (*destination*), o `javac` cria a pasta `bin/`, replica a estrutura do pacote (`bin/Techlab/`) e deposita exclusivamente os `.class` lá dentro. Seu diretório de código-fonte permanece 100% limpo.

---

### 📦 3. Quem Deve Ter a Declaração `package Techlab;` no Cabeçalho?

* **Regra Fundamental de Ouro:**  
  Se um arquivo está localizado fisicamente dentro da pasta `Techlab/`, ele **OBRIGATORIAMENTE** deve ter `package Techlab;` como a primeiríssima linha de código (antes de imports e declaração da classe).
* **O `Main` também precisa ter `package`?**  
  **SIM!** Se o `Main.java` estiver dentro da pasta `Techlab/` junto com `AtivoTI.java` e `ChamadoSuporte.java`, ele **deve ter** `package Techlab;` no cabeçalho.
  - Como todos estão no mesmo pacote, o `Main` enxerga as classes `AtivoTI` e `ChamadoSuporte` **diretamente, sem precisar de `import`**.
* **E se o `Main.java` estivesse na raiz (fora da pasta `Techlab/`)?**  
  - Nesse caso, o `Main.java` não teria `package` nenhum (estaria no *default package*).
  - Porém, para usar as classes, ele precisaria declarar explicitamente no topo: `import Techlab.AtivoTI;` e `import Techlab.ChamadoSuporte;`.
  - **Recomendação padrão:** Manter todos os arquivos do módulo juntos dentro da pasta do pacote (`Techlab/`) com o respectivo `package Techlab;` em todos eles.

---

### 📂 4. Estrutura de Pastas Recomendada (Raiz do Projeto)

Você deve estar localizado na **pasta raiz do projeto** (fora da pasta `Techlab/`) ao executar os comandos no terminal:

```text
meu_projeto/                 <── [Você executa o terminal AQUI]
├── Techlab/                 <── Código-fonte (.java - edição humana)
│   ├── AtivoTI.java         <── Tem: package Techlab; na linha 1
│   ├── ChamadoSuporte.java  <── Tem: package Techlab; na linha 1
│   └── Main.java            <── Tem: package Techlab; na linha 1
└── bin/                     <── Gerado automaticamente pelo compilador (.class - Bytecode)
    └── Techlab/
        ├── AtivoTI.class
        ├── ChamadoSuporte.class
        └── Main.class
```

---

### ⚙️ 5. O Que Significam os Parâmetros `-d` e `-cp`?

* **`-d bin` (Destination Directory / Diretório de Destino):**
  - Instrui o `javac` a ler a declaração `package Techlab;` dentro dos arquivos e salvar todos os arquivos compilados (`.class`) organizados dentro de `bin/Techlab/`.
  - O compilador cria a pasta `bin/Techlab/` automaticamente se ela não existir.

* **`-cp bin` (Classpath / Caminho de Classes):**
  - Informa à Máquina Virtual Java (`java`) onde fica a raiz dos pacotes compilados na hora de rodar.
  - Como indicamos `-cp bin`, o Java busca a classe principal através do seu nome qualificado completo: `Techlab.Main` (isto é, procura `bin/Techlab/Main.class`).

---

### 💻 6. Comandos Multiplataforma (Executados na Raiz)

```bash
# 🐧 Linux (Terminal Bash / OpenJDK)
javac -d bin Techlab/AtivoTI.java Techlab/ChamadoSuporte.java Techlab/Main.java && java -cp bin Techlab.Main

# 🪟 Windows (PowerShell / CMD)
javac -d bin Techlab\AtivoTI.java Techlab\ChamadoSuporte.java Techlab\Main.java; java -cp bin Techlab.Main

# 🍏 macOS (Terminal Zsh / OpenJDK)
javac -d bin Techlab/AtivoTI.java Techlab/ChamadoSuporte.java Techlab/Main.java && java -cp bin Techlab.Main
```

> **Dica Pro:** No Linux e macOS, você pode compilar todos os arquivos do pacote de uma só vez usando curinga:  
> `javac -d bin Techlab/*.java && java -cp bin Techlab.Main`

---

## Glossário
- **JVM (Java Virtual Machine)**: Ambiente de execução que interpreta o bytecode compilado do Java e gerencia a memória física da máquina.
- **Bytecode (`.class`)**: Conjunto de instruções binárias intermediárias geradas pelo compilador Java (`javac`) para serem executadas pela JVM de forma portável.
- **Package (Pacote Java)**: Declaração no topo do arquivo (`package nome;`) que define o namespace e exige que o arquivo resida em um diretório com o mesmo nome.
- **Pasta `bin/`**: Convenção clássica da computação (abreviação de *binaries*) para abrigar executáveis e arquivos compilados, separando-os do código-fonte.
- **Heap**: Região de memória da JVM destinada à alocação dinâmica de instâncias de objetos e arrays.
- **Stack**: Estrutura LIFO de memória rápida que armazena os quadros de execução dos métodos e referências locais.
- **Garbage Collector**: Mecanismo automático da plataforma Java que identifica e recicla objetos que não possuem mais referências ativas no Heap.
- **Classpath**: Parâmetro do Java (`-cp`) que informa à JVM onde encontrar as classes compiladas (`.class`) e pacotes para execução.
- **Diretório de Destino (`-d`)**: Opção do compilador `javac` que especifica a pasta onde a árvore de pacotes e arquivos binários `.class` será organizada.
