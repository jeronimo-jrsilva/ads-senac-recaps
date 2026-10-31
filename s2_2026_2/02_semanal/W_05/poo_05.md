---
tipo: portal
titulo: "Programação Orientada a Objetos - Aula 05"
disciplina: "Programação Orientada a Objetos"
semestre: "2026.2"
data: 2026-09-08
professor: "Tibério"
---

A quinta aula de **Programação Orientada a Objetos (POO)** com o Professor Tibério aprofundou a ruptura entre o paradigma procedural (C) e o modelo orientado a objetos (Java), discutindo modelagem em escala, classes de domínio, reaproveitamento de código e implementação de herança através da palavra-chave `super`.

---

## 1. Do Script Procedural à Escala de Negócio (C vs Java)
O Professor Tibério abriu o encontro traçando um paralelo prático entre C e Java:
- Em linguagens procedurais como C, o foco reside na execução sequencial rápida de instruções e scripts para problemas delimitados.
- Em POO com Java, a complexidade sintática existe para viabilizar **escalabilidade e governança de regras de negócio**, permitindo que estruturas empresariais complexas sejam mapeadas em software sem que alterações pontuais quebrem todo o sistema.
- **A analogia dos jogos e menus dinâmicos:** Criar um menu de opções escrevendo linha por linha na tela é inviável em escala; da mesma forma que os dados de uma interface devem vir de um banco de dados estruturado, o código deve modelar entidades de domínio (como animais em um jogo de mundo aberto ou chamados de TI) através de classes reutilizáveis.

---

## 2. Conceito de Objeto e Atributos de Domínio
Um objeto em memória não é apenas um agrupamento arbitrário de variáveis, mas a materialização de uma entidade que possui:
- **Estado (Atributos):** Identificadores e características que descrevem a instância (`id`, `patrimonio`, `modelo`, `status`).
- **Comportamento (Métodos):** Operações que agem sobre aquele estado.
- **Identidade Única:** Diferenciação garantida no ciclo de vida da aplicação.

---

## 3. Herança Prática e Inicialização com `super()`
Foi explorada a extensão de classes para reaproveitar estruturas comuns e delegar a inicialização para a superclasse:

```java
package Techlab;

// Subclasse especializando AtivoTI
public class Notebook extends AtivoTI {
    private String processador;
    private int memoriaRam;

    // Construtor especializado chamando o construtor da superclasse
    public Notebook(int id, String patrimonio, String modelo, String status, String processador, int memoriaRam) {
        super(id, patrimonio, modelo, status); // Delega inicialização para AtivoTI
        this.processador = processador;
        this.memoriaRam = memoriaRam;
    }

    public String getProcessador() {
        return processador;
    }

    public int getMemoriaRam() {
        return memoriaRam;
    }
}
```

- O uso explícito de `super(...)` garante que os invariantes e regras estabelecidos pela classe base sejam respeitados antes da configuração dos atributos específicos da subclasse.
