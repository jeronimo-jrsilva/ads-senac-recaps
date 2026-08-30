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

## Glossário
- **JVM (Java Virtual Machine)**: Ambiente de execução que interpreta o bytecode compilado do Java e gerencia a memória física da máquina.
- **Heap**: Região de memória da JVM destinada à alocação dinâmica de instâncias de objetos e arrays.
- **Stack**: Estrutura LIFO de memória rápida que armazena os quadros de execução dos métodos e referências locais.
- **Garbage Collector**: Mecanismo automático da plataforma Java que identifica e recicla objetos que não possuem mais referências ativas no Heap.
