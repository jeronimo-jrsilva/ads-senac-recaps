---
tipo: portal
titulo: "Programação Orientada a Objetos - Aula 06"
disciplina: "Programação Orientada a Objetos"
semestre: "2026.2"
data: 2026-09-15
professor: "Tibério"
---

A sexta aula de **Programação Orientada a Objetos (POO)** com o Professor Tibério avançou nos pilares de abstração da linguagem Java, introduzindo formalmente o conceito de **Classes Abstratas** (`abstract class`), regras de instanciação e a definição de modelos conceituais para garantir padronização em hierarquias de software corporativo.

---

## 1. O Conceito de Classe Abstrata
O Professor Tibério esclareceu a diferença fundamental entre uma classe concreta e uma classe abstrata:
- Uma classe comum define tanto os atributos quanto a implementação completa de todos os seus métodos, podendo ser diretamente instanciada através do operador `new`.
- A **Classe Abstrata**, por sua vez, serve como uma **matriz conceitual**: ela existe para definir atributos e comportamentos comuns a uma família de objetos, mas **não pode ser diretamente instanciada** em memória.
- **A analogia do reino animal:** Não existe na natureza um animal genérico chamado apenas de "Animal"; existem instâncias concretas de `Cachorro`, `Gato` ou `Cavalo`. Portanto, `Animal` deve ser uma classe abstrata contendo o contrato e os atributos fundamentais que todas as subclasses obrigatoriamente herdarão.

```java
package Techlab;

// Classe base conceitual: impede 'new AtivoTI()' diretamente
public abstract class AtivoTI {
    protected int id;
    protected String patrimonio;
    protected String modelo;
    protected String status;

    public AtivoTI(int id, String patrimonio, String modelo, String status) {
        this.id = id;
        this.patrimonio = patrimonio;
        this.modelo = modelo;
        this.status = status;
    }

    // Método concreto compartilhado por todos os herdeiros
    public String getStatus() {
        return status;
    }
}
```

---

## 2. Garantia de Padronização e Requisitos de Mercado
Foi debatido o papel da abstração no ciclo de vida de projetos de grande porte:
- Classes abstratas garantem que nenhum desenvolvedor crie instâncias incompletas de entidades base.
- Permitem a extensão segura de funcionalidades, impondo regras contratuais uniformes para todas as subclasses que vierem a ser criadas no sistema.
