---
tipo: portal
titulo: "Estatística com Python - Aula 04 (Consolidado)"
disciplina: "Estatística com Python"
semestre: "2026.1"
data: 2026-05-05
professor: "Nator Junior"
---

Esta aula focou na automatização de transformações de dados utilizando ferramentas avançadas do ecossistema Pandas. O Professor Nator Junior demonstrou como sair da manipulação manual para um fluxo de trabalho programático, utilizando **Funções Lambda** e os métodos de aplicação vetorizada (**Apply** e **Map**), além de consolidar técnicas de fatiamento e ordenação para análise de datasets reais.

---

## 1. Configuração de Ambiente: Anaconda vs. Miniconda
Para a prática profissional de Data Science, a recomendação é o uso de distribuições que já integram o ecossistema científico do Python (NumPy, SciPy, Pandas, Matplotlib).

- **Anaconda:** Distribuição robusta e completa, incluindo o "Navigator" (interface gráfica). Ideal para iniciantes ou máquinas potentes, pois já traz milhares de pacotes pré-instalados.
- **Miniconda:** Versão minimalista focada apenas no gerenciador de pacotes `conda` e no Python. É a escolha preferida de engenheiros que desejam controle total sobre as dependências e economia de recursos de hardware.

---

## 2. Funções Anônimas (Lambda)
As funções `lambda` permitem criar lógicas de processamento rápidas sem a necessidade de uma declaração formal via bloco `def`. Elas são fundamentais no Pandas para realizar transformações "on-the-fly".

- **Sintaxe:** `lambda argumentos: expressão`
- **Flexibilidade:** Podem ser usadas para limpeza de strings, cálculos matemáticos rápidos ou conversões de tipos dentro de uma única linha de código.
- **Exemplo:** `lambda x: x.upper() if isinstance(x, str) else x` (Converte para maiúsculas apenas se o dado for uma string).

---

## 3. Transformação de Dados: apply e map
O domínio desses métodos permite realizar operações complexas em DataFrames e Series sem recorrer a loops `for` lentos, aproveitando a otimização interna do Pandas.

### 3.1 Método apply()
Aplica uma função ao longo de um eixo (colunas por padrão). É a ferramenta mais versátil para aplicar lógicas customizadas em toda uma coluna de uma só vez.
- **Uso:** `df['coluna'].apply(função_ou_lambda)`
- **Eficiência:** Internamente, o Pandas tenta otimizar a execução, tornando-a mais rápida que iterações manuais em grandes volumes de dados.

### 3.2 Método map()
Utilizado exclusivamente em Series para substituir valores de acordo com um mapeamento pré-definido. É ideal para tradução de categorias ou codificação de variáveis qualitativas.
- **Uso:** `series.map({valor_antigo: valor_novo})` ou via função lambda para transformações unidimensionais simples.

---

## 4. Exercício Prático: População do Ceará (2019)
A aula encerrou com um estudo de caso utilizando dados reais da população cearense, consolidando o fluxo: **Filtro -> Ordenação -> Fatiamento Final**.

1. **Filtragem:** Seleção rigorosa por UF ('CE') e Ano (2019) usando máscaras booleanas.
2. **Ordenação:** Uso do `sort_values(by='populacao')`. Por padrão, a ordenação é crescente, movendo os maiores valores para o final do DataFrame.
3. **Seleção de Top 10 (iloc):** 
   - Para extrair as 10 cidades mais populosas de um dataset ordenado de forma crescente, utilizamos a lógica de índices negativos: `df.iloc[-10:]`.
   - O índice `-1` representa o registro de maior valor (ex: Fortaleza), e o fatiamento `-10:` garante a captura dos 10 registros finais.

---

## Glossário Técnico
- **Lambda:** Função anônima definida em uma única linha.
- **apply:** Método que aplica uma função ao longo de um eixo de um DataFrame.
- **map:** Método que mapeia valores de uma Series de acordo com um dicionário ou função.
- **sort_values:** Função do Pandas para ordenar DataFrames baseada em uma ou mais colunas.
- **Anaconda:** Distribuição de Python focada em ciência de dados e machine learning.
- **Vetorização:** Aplicação de uma operação a um conjunto inteiro de valores de uma só vez.
- **Filtro Booleano:** Técnica de filtragem de dados usando condições lógicas que resultam em True ou False.
