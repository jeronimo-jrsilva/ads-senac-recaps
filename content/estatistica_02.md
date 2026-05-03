---
tipo: portal
titulo: "Estatística com Python - Aula 02"
disciplina: "Estatística com Python"
semestre: "2026.1"
data: 2026-04-28
professor: "Nator Junior"
---

A segunda aula do módulo de Estatística focou na transição do Python puro para o ecossistema de análise de dados profissional. O Professor Nator Junior detalhou os ambientes de desenvolvimento, a importância da documentação em Markdown e as estruturas de dados específicas da biblioteca Pandas, estabelecendo o fluxo de trabalho "Data-First".

---

## 1. Ecossistema e Ambientes de Programação (IDEs)
O professor discutiu a versatilidade do **VS Code** como a IDE mais popular do mercado devido aos seus plugins para múltiplas linguagens (Python, PHP, JS, SQL). No entanto, para projetos de ciência de dados, foram apresentadas alternativas focadas:

- **Anaconda:** Um framework completo para Data Science que já inclui as principais bibliotecas.
- **Mini-Conda:** Versão compacta e modular do Anaconda.
- **Jupyter Notebook:** Ambiente que permite unir código, texto (Markdown) e visualizações em um único arquivo `.ipynb`.

---

## 2. Documentação Técnica com Markdown
Foi enfatizado que um bom analista de dados deve saber documentar suas descobertas. O **Markdown** foi apresentado como a linguagem de formatação padrão para notebooks.

- **Sintaxe Visual:** Uso de `#` para títulos (lasanha), `**` para negrito e links internos.
- **Vantagem:** Facilita a leitura por stakeholders não técnicos, transformando scripts em relatórios executivos.

---

## 3. Introdução à Biblioteca Pandas
O Pandas é a ferramenta definitiva para manipulação de dados tabulares. O professor explicou o conceito de biblioteca como um conjunto de funções prontas disponibilizadas pela comunidade.

- **Importação:** O padrão de mercado é `import pandas as pd`. O "pd" é um apelido (alias) para facilitar a chamada dos métodos.
- **Pandas vs Python Puro:** Enquanto no Python puro precisamos de loops e condicionais manuais, o Pandas oferece funções vetorizadas que executam cálculos complexos (média, moda, variância) em uma única linha.

---

## 4. Estruturas de Dados: Series
A **Series** é a estrutura unidimensional do Pandas, similar a uma lista ou coluna de Excel, mas com superpoderes estatísticos.

- **Indexação Customizada:** Diferente da lista comum, uma Series permite índices não numéricos (ex: nomes, datas, tuplas).
- **Atributos vs Métodos:**
    - `data=`: Atributo que define os valores.
    - `.mean()`: Método para média.
    - `.std()`: Método para desvio padrão.
    - `.var()`: Método para variância.

---

## 5. Reconstrução de Código: Manipulação de Series
Exemplos práticos demonstrados em aula utilizando o Pandas.

```python
import pandas as pd

# 1. Criando uma Series a partir de uma lista
notas = [8.0, 9.1, 7.5, 2.1, 8.5]
notas_series = pd.Series(data=notas)

# 2. Acessando estatísticas instantâneas
print(f"Média das Notas: {notas_series.mean()}")
print(f"Desvio Padrão: {notas_series.std()}")
print(f"Variância: {notas_series.var()}")

# 3. Series com Índices Customizados
precos = pd.Series(
    data=[2.50, 5.50, 1.20],
    index=["Banana", "Big Mac", "Prato Feito"]
)
print(f"Preço do Big Mac: {precos['Big Mac']}")

# 4. Exemplo de Atributos Nomeados vs Posicionais
# No Pandas, podemos omitir 'data=' se a ordem for respeitada,
# mas nomear os atributos é uma boa prática de clareza (Princípio Nator).
df_exemplo = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
```

---

## 6. Lógica de Atributos e Funções
O professor detalhou como o Python lida com parâmetros pré-definidos em funções, justificando por que usamos `data=lista` na criação de Series:
- **Parâmetros Padrão:** Valores que a função assume se nada for passado.
- **Sobrescrita:** Ao passar um argumento, o valor padrão é ignorado.
- **Clareza de Código:** Nomear atributos evita erros em funções com muitos parâmetros opcionais.

---

## Glossário Técnico
- **Média**: Valor que representa o centro de um conjunto de dados, calculado pela soma de todos os valores dividida pelo total de elementos. <a href="https://pt.wikipedia.org/wiki/Média">Wikipedia</a>
- **Desvio Padrão**: Medida que indica o quanto os dados de um conjunto estão afastados da média. Um desvio baixo indica dados próximos à média; um desvio alto indica grande dispersão. <a href="https://pt.wikipedia.org/wiki/Desvio_padrão">Wikipedia</a>
- **Variância**: Medida de dispersão que mostra o quão distantes os valores estão da média. Matematicamente, é o quadrado do desvio padrão. <a href="https://pt.wikipedia.org/wiki/Variância">Wikipedia</a>
- **IDE (Integrated Development Environment)**: Ambiente integrado para desenvolvimento de software.
- **Vetorização**: Capacidade do Pandas de aplicar uma operação a toda uma coluna simultaneamente.
- **Series**: Objeto unidimensional do Pandas que contém um array de dados e um array de rótulos (índice).
- **Alias**: Apelido dado a uma biblioteca no momento da importação (ex: pd).
- **IPYNB**: Extensão de arquivo do Jupyter Notebook (Interactive Python Notebook).
