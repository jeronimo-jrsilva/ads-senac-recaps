---
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

## 2. Exemplos Didáticos de Domínio: Veículo e Conta Bancária
Para consolidar os conceitos de regras de negócio e proteção de estado, o Professor Tibério apresentou e explicou dois exemplos clássicos de modelagem:

- **Exemplo Veículo:** Atributos de velocidade e marcha manipulados por métodos `acelerar()`, `frear()` e `trocarMarcha()`.
- **Exemplo Conta Bancária:** Encapsulamento de regras financeiras, demonstrando como métodos como `sacar()` garantem que operações só ocorram com saldo suficiente, impedindo a alteração direta e insegura do saldo por código externo.

---

## Glossario

- **Atributo**: Campo de dados de uma classe que armazena uma característica de estado do objeto [Wikipedia](https://pt.wikipedia.org/wiki/Atributo_(computa%C3%A7%C3%A3o)).
- **Método**: Sub-rotina associada a um objeto responsável por executar ações e manipular seu estado interno [Wikipedia](https://pt.wikipedia.org/wiki/M%C3%A9todo_(programa%C3%A7%C3%A3o)).
- **Instanciação**: Processo computacional de alocação de memória para a criação de um novo objeto a partir de sua classe.
- **Regra de Negócio**: Lógica que governa como os dados de um sistema podem ser criados, alterados e validados.
