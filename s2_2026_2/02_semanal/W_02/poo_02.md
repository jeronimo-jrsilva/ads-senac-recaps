---
tipo: portal
titulo: "Programação Orientada a Objetos - Aula 02"
disciplina: "Programação Orientada a Objetos"
semestre: "2026.2"
data: 2026-08-18
professor: "Tibério"
---

A segunda aula de **Programação Orientada a Objetos (POO)** com o Professor Tibério aprofundou a distinção fundamental entre **Atributos (estado)** e **Métodos (comportamento)**, estruturando as primeiras classes canônicas no Java e lançando a modelagem do projeto corporativo **Techlab**.

---

## 1. Atributos vs. Métodos: O Caso da Lâmpada LED Inteligente
O Professor Tibério utilizou uma Lâmpada LED conectada para ensinar a arquitetura elementar de uma classe:

- **Atributos de Estado:** Propriedades que guardam o estado atual do objeto em memória (ex: `boolean ligada`, `String cor`, `int brilho`).
- **Métodos Operacionais:** Comportamentos que transformam e protegem esse estado de forma controlada (ex: `ligar()`, `desligar()`, `alterarCor()`).

```java
// Modelagem canônica da Lâmpada LED inteligente em Java
public class LampadaLED {
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

## 2. Modelagem Corporativa: O Projeto Techlab (`AtivoTI`)
Para conectar os conceitos a sistemas reais de gestão de infraestrutura de TI, o docente introduziu a primeira versão da classe `AtivoTI`:

- **Atributos Privados:** `id`, `codigoPatrimonio`, `modelo`, `status`.
- **Construtor Primário:** Inicialização dos dados vitais do equipamento no momento da instanciação.
- **Getters e Setters:** Controle do ciclo de vida operacional do ativo (ex: transição de `"Ativo"` para `"Em Manutenção"`).

```java
package Techlab;

public class AtivoTI {
    private int id;
    private String codigoPatrimonio;
    private String modelo;
    private String status;

    public AtivoTI(int id, String codigoPatrimonio, String modelo, String status) {
        this.id = id;
        this.codigoPatrimonio = codigoPatrimonio;
        this.modelo = modelo;
        this.status = status;
    }

    public int getId() { return id; }
    public String getCodigoPatrimonio() { return codigoPatrimonio; }
    public String getModelo() { return modelo; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}
```

---

## Glossário
- **Atributo**: Campo de dados de uma classe que armazena uma característica de estado do objeto [Wikipedia](https://pt.wikipedia.org/wiki/Atributo_(computa%C3%A7%C3%A3o)).
- **Método**: Sub-rotina associada a um objeto responsável por executar ações e manipular seu estado interno [Wikipedia](https://pt.wikipedia.org/wiki/M%C3%A9todo_(programa%C3%A7%C3%A3o)).
- **Instanciação**: Processo computacional de alocação de memória no Heap para a criação de um novo objeto a partir de sua classe.
- **Regra de Negócio**: Lógica de aplicação que governa como os dados de um sistema podem ser criados, alterados e validados.
