---
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

## 3. O Ecossistema Enterprise: Curiosidade sobre JS e o Rigor do Java
Foi traçada uma análise contextual da evolução das linguagens de mercado e do ecossistema corporativo:

- **Curiosidade Histórica (A Evolução do JavaScript):** Como curiosidade de mercado, o professor comentou a evolução do JS, que nasceu na Netscape como script leve para navegadores e deu uma grande virada quando o Google o utilizou no Gmail (e mais tarde com o motor V8 e Node.js), provando sua flexibilidade.
- **Java e a Filosofia da JVM (Foco da Disciplina):** Criado sob o lema *"Write Once, Run Anywhere"*, o Java compila código-fonte para bytecode interpretado pela Java Virtual Machine (JVM). Tibério explicou que a verbosidade e a formalidade do Java não são burocracia desnecessária, mas sim escolhas deliberadas de engenharia de software para garantir contratos de tipos explícitos, manutenibilidade e segurança em sistemas corporativos de grande porte.

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

### 💻 Como Compilar e Executar no Terminal (Multiplataforma)

```bash
# 🐧 Linux (Terminal Bash / OpenJDK)
javac Aluno.java && java Aluno

# 🪟 Windows (PowerShell / CMD)
javac Aluno.java; java Aluno

# 🍏 macOS (Terminal Zsh / OpenJDK)
javac Aluno.java && java Aluno
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
