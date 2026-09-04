---
tipo: portal
titulo: "Programação Orientada a Objetos - Aula 04"
disciplina: "Programação Orientada a Objetos"
semestre: "2026.2"
data: 2026-09-01
professor: "Tibério"
---

A quarta aula de **Programação Orientada a Objetos (POO)** com o Professor Tibério avançou na engenharia do projeto **Techlab**, explorando o **Polimorfismo Ad-hoc** através da sobrecarga de construtores (`Constructor Overloading`), a delegação de inicialização com `this()`, a associação estrutural de classes de domínio (`ChamadoSuporte` $\to$ `AtivoTI`), o encapsulamento com imutabilidade parcial e a sobrescrita do método `@Override toString()`.

---

## 1. Polimorfismo Ad-hoc e Sobrecarga de Construtores
O Professor Tibério introduziu o conceito de **Polimorfismo Ad-hoc** (sobrecarga de métodos e construtores), demonstrando como um mesmo identificador ou construtor pode assumir diferentes formas e comportamentos em função dos parâmetros fornecidos:

- **Construtor Completo:** Inicializa explicitamente todos os atributos do objeto (`id`, `patrimonio`, `modelo`, `status`).
- **Construtor Sobrecarregado (Polimorfismo Ad-hoc via `this()`):** Permite um fluxo de cadastro simplificado em que o `status` não é passado pelo usuário, aplicando o valor padrão `"Ativo"` através da delegação `this(id, patrimonio, modelo, "Ativo");`.

```java
package Techlab;

public class AtivoTI {
    private int id;
    private String patrimonio;
    private String modelo;
    private String status;

    // 1. Construtor Completo
    public AtivoTI(int id, String patrimonio, String modelo, String status) {
        this.id = id;
        this.patrimonio = patrimonio;
        this.modelo = modelo;
        this.status = status;
    }

    // 2. Construtor Sobrecarregado (Polimorfismo Ad-hoc com valor padrão)
    public AtivoTI(int id, String patrimonio, String modelo) {
        this(id, patrimonio, modelo, "Ativo");
    }

    // Imutabilidade Parcial: Apenas 'status' pode ser alterado; 'id', 'patrimonio' e 'modelo' são finais
    public String getStatus() { return this.status; }
    public void setStatus(String status) { this.status = status; }
    public String getModelo() { return this.modelo; }

    @Override
    public String toString() {
        return "Ativo TI [ID: " + this.id + " | Pat: " + this.patrimonio + 
               " | Modelo: " + this.modelo + " | Status: " + this.status + "]";
    }
}
```

---

## 2. Associação de Objetos e Composição no Domínio
O relacionamento entre entidades do sistema reflete a modelagem do mundo real corporativo:

- A classe `ChamadoSuporte` encapsula uma referência direta ao objeto `AtivoTI` que gerou o ticket (`private AtivoTI ativoRelacionado;`).
- Ao manipular o chamado, a aplicação acessa e atualiza o estado do equipamento em memória através de `chamado.getAtivoRelacionado().setStatus("Em Manutenção")`, preservando a consistência do grafo de objetos no *Heap*.

```java
package Techlab;

public class ChamadoSuporte {
    private int id;
    private String descricao;
    private String prioridade;
    private AtivoTI ativoRelacionado;

    public ChamadoSuporte(int id, String descricao, String prioridade, AtivoTI ativoRelacionado) {
        this.id = id;
        this.descricao = descricao;
        this.prioridade = prioridade;
        this.ativoRelacionado = ativoRelacionado;
    }

    public AtivoTI getAtivoRelacionado() {
        return this.ativoRelacionado;
    }

    @Override
    public String toString() {
        return "------------------------------------\n" +
               "Chamado #" + this.id + "\n" +
               "Descrição: " + this.descricao + "\n" +
               "Prioridade: " + this.prioridade + "\n" +
               "Equipamento Relacionado: " + this.ativoRelacionado + "\n" +
               "------------------------------------";
    }
}
```

---

## 3. Sobrescrita de Métodos Herdados: `@Override toString()` e Identidade
- **Eliminação do Hash Padrão:** Por padrão, o método `toString()` herdado de `java.lang.Object` imprime o endereço hash (`Techlab.AtivoTI@7a81197d`). A anotação `@Override` redefine o método para formatar uma saída limpa e profissional no console.
- **Identidade e o Método `equals()`:** Diferenciação essencial entre comparação por referência de ponteiro (`==`) e comparação por conteúdo lógico e semântico de atributos (`equals()`).

---

## Glossário
- **Polimorfismo Ad-hoc**: Tipo de polimorfismo que permite que funções ou métodos de mesmo nome operem sobre tipos ou listas de argumentos distintos (sobrecarga / *overloading*).
- **Sobrecarga de Construtores**: Capacidade de uma classe definir múltiplos construtores com diferentes assinaturas de parâmetros para atender a diferentes fluxos de instanciação.
- **Palavra-chave `this()`**: Chamada explícita utilizada na primeira linha de um construtor para delegar a inicialização a outro construtor da mesma classe.
- **Associação de Objetos**: Vínculo estrutural no qual um objeto mantém em seus atributos a referência para uma instância de outra classe.
- **Método `toString()`**: Método herdado da classe raiz `Object` que retorna a representação textual de uma instância no Java.
- **Método `equals()`**: Método utilizado para comparar a equivalência lógica entre dois objetos com base em seus atributos internos, superando a mera comparação de ponteiros (`==`).
