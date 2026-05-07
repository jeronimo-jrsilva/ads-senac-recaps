---
tipo: portal
titulo: "Estatística com Python - Aula 03 (Consolidado)"
disciplina: "Estatística com Python"
semestre: "2026.1"
data: 2026-05-04
professor: "Nator Junior"
---

Esta aula aprofunda a manipulação técnica de dados utilizando a biblioteca **Pandas**, focando na transição do **NumPy** para estruturas de dados mais versáteis e no domínio das funções de indexação e filtragem. O Professor Nator Junior enfatizou que o Pandas não é apenas uma biblioteca de tabelas, mas um motor de análise que permite tratar volumes massivos de dados com sintaxe expressiva e alta performance.

---

## 1. Fundamentos: Pandas vs. NumPy
A adoção do **Pandas** justifica-se pela alta abstração e pelas funções integradas para limpeza e análise de dados estruturados. Enquanto o **NumPy** foca em operações matemáticas brutas e arrays homogêneos, o **Pandas** oferece flexibilidade para lidar com tipos heterogêneos e rótulos (labels).

- **Series:** Estrutura unidimensional, análoga a uma coluna rotulada. Possui métodos vetorizados e suporte nativo a dados faltantes (`NaN`).
- **DataFrames:** Conjunto de Series compartilhando o mesmo índice. É a estrutura bidimensional central, assemelhando-se a uma planilha SQL ou Excel, mas com poder computacional de processamento em memória.

---

## 2. Indexação Técnica: loc vs. iloc
O domínio do fatiamento (**slicing**) é essencial para o trabalho estatístico. A distinção entre rótulos e posições é o primeiro passo para a precisão analítica e para evitar o erro comum de confusão entre índices numéricos e nominais.

### 2.1 Indexação por Rótulo (loc)
O método `loc` acessa dados através dos nomes explícitos das linhas e colunas. É o método preferido quando o dataset possui índices semânticos (ex: datas ou nomes de cidades).
- **Sintaxe:** `df.loc[index_label, column_label]`
- **Filtragem Dinâmica:** Permite passar condições booleanas. Exemplo: `df.loc[df['calorias'] >= 200]` seleciona todas as observações onde a densidade calórica atinge o critério.

### 2.2 Indexação por Posição (iloc)
O método `iloc` acessa dados estritamente pela posição numérica, ignorando rótulos. É ideal para seleções baseadas em "top N" ou para amostragem sistemática.
- **Referência:** `df.iloc[0]` para a primeira linha e `df.iloc[-1]` para a última.
- **Regra do Fatiamento:** No `iloc`, o limite superior é **excluído**. `df.iloc[0:5]` retorna as linhas de 0 a 4.

---

## 3. Lógica de Filtros e Operadores Booleanos
A filtragem complexa é construída sobre a lógica booleana, permitindo cruzamentos de dados precisos. Diferente do Python puro, o Pandas exige o uso de operadores bitwise e parênteses para agrupar condições.

- **AND (&):** Interseção de condições (ex: `(ano == 2019) & (uf == 'CE')`).
- **OR (|):** União de condições (ex: `(status == 'A') | (status == 'B')`).
- **NOT (~):** Inversão de filtro (ex: `~df['nome'].isna()`).

A regra de sintaxe é rígida: o uso de parênteses em cada condição é obrigatório para evitar ambiguidades de precedência de operadores.

---

## 4. Ingestão de Dados e Automação
A função `read_csv` foi introduzida como a porta de entrada para bases de dados externas. O professor destacou que parâmetros como `sep`, `encoding` e `usecols` são fundamentais para lidar com datasets de fontes diversas sem corromper os dados.

```python
import pandas as pd

# Exemplo de Ingestão com Tratamento Inicial
df = pd.read_csv("dataset.csv", sep=";", encoding="utf-8")

# Verificação de Integridade
print(df.info()) # Resumo da estrutura e tipos
print(df.head(10)) # Visualização das 10 primeiras observações
```

---

## Glossário Técnico
- **DataFrame:** Estrutura bidimensional de dados rotulados, similar a uma tabela.
- **Series:** Objeto unidimensional que contém uma sequência de valores e um array associado de rótulos (índice).
- **loc:** Indexador baseado em rótulos/labels para seleção de dados.
- **iloc:** Indexador baseado em posição inteira para seleção de dados.
- **Fatiamento (Slicing):** Técnica de extração de subconjuntos de dados.
- **Vetorização:** Processo de aplicar operações a um array inteiro de uma vez, sem loops explícitos.
- **Boolean Masking:** Técnica de usar arrays de valores booleanos para filtrar dados em um DataFrame.
