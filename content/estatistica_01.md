---
tipo: portal
titulo: "Estatística com Python - Aula 01"
disciplina: "Estatística com Python"
semestre: "2026.1"
data: 2026-04-27
professor: "Nator Junior"
---

A aula inaugural do módulo de Estatística e Análise de Dados marcou a unificação plena das turmas e a introdução dos fundamentos teóricos que sustentam a ciência de dados. O Professor Nator Junior estabeleceu os conceitos de amostragem, classificação de variáveis e a lógica matemática por trás dos algoritmos estatísticos que serão implementados via Python e Pandas.

---

## 1. Unificação e Dinâmica de Turma
Com a chegada de cerca de 50 alunos da "Turma 2", a sessão iniciou com apresentações focadas no perfil dos estudantes. Foram identificados subgrupos interessados em:
- **Segurança da Informação:** Foco em Red Team e Blue Team.
- **Investimentos e Mercado Financeiro:** Interesse em automação de análise de ativos via IA.
- **Transição de Carreira:** Profissionais de diversas áreas migrando para tecnologia.

---

## 2. Fundamentos de Estatística: População vs Amostra
O professor definiu a estatística como a ciência de coletar, organizar e interpretar dados para tomada de decisão sob incerteza.

- **População:** O conjunto total de todos os indivíduos ou elementos que compartilham uma característica comum (ex: todos os 900 moradores de um condomínio).
- **Amostra:** Um subconjunto representativo da população. Foi enfatizado que, se a técnica de amostragem for adequada, o resultado da amostra é representativo da população (ex: 650 moradores entrevistados).
- **Inferência Estatística:** O processo de tirar conclusões sobre a população com base nos dados da amostra.

---

## 3. Classificação de Variáveis
A correta identificação dos dados é vital para escolher o método de análise adequado no Pandas.

### Variáveis Quantitativas (Numéricas)
- **Discretas:** Valores inteiros, geralmente contagens (ex: número de filhos, quantidade de smartphones).
- **Contínuas:** Valores reais que podem assumir qualquer valor em um intervalo (ex: massa, temperatura, altura). No Python, associam-se ao tipo `float`.

### Variáveis Qualitativas (Categorias)
- **Nominais:** Não possuem uma ordem intrínseca (ex: cor dos olhos, estado civil, disciplinas acadêmicas).
- **Ordinais:** Possuem uma hierarquia ou ordem lógica (ex: nível de escolaridade, classe social, gravidade de um sintoma).

---

## 4. Organização de Dados e Frequência
Foi introduzido o conceito de **Rol**, que é a sequência ordenada de dados brutos (geralmente de forma crescente). A ordenação é o primeiro passo para o cálculo de frequências.

- **Frequência Simples (Absoluta):** Número de vezes que um valor específico aparece no conjunto.
- **Frequência Relativa:** A razão entre a frequência simples e o total da amostra.
- **Tratamento de Dados Faltantes:** O professor alertou sobre a importância de lidar com valores nulos (`NaN`). Estratégias citadas incluem preenchimento com a média ou moda para não distorcer a análise final.

---

## 5. Reconstrução Lógica: Somatórios e Loops
Para desmistificar fórmulas complexas, o professor relacionou a notação matemática de Somatório ($\sum$) com as estruturas de repetição em Python.

```python
# Conjunto de dados (Amostra de notas)
notas = [8.0, 9.1, 7.5, 2.1, 8.5, 7.4, 8.9, 7.6, 7.8, 8.0]

# Implementação via Lógica Pura (Simulando o Somatório)
soma = 0
count = 0
for n in notas:
    soma += n
    count += 1

media = soma / count
print(f"Soma Total (Σ): {soma}")
print(f"Média Aritmética: {media:.2f}")

# Exemplo de representação lógica de uma equação complexa
# Soma de quadrados (preparando para variância)
soma_quadrados = 0
for n in notas:
    soma_quadrados += n**2
print(f"Soma dos Quadrados: {soma_quadrados:.2f}")
```

---

## Glossário Técnico
- **Amostragem:** Técnica de seleção de elementos de uma população.
- **Dados Brutos:** Dados coletados que ainda não passaram por processamento ou organização.
- **Rol:** Lista de dados organizada de forma crescente ou decrescente.
- **Frequência Relativa:** Percentual que um dado representa em relação ao todo.
- **Variável Discreta:** Variável numérica que assume valores em pontos isolados da reta real.
- **Variável Contínua:** Variável numérica que pode assumir qualquer valor em um intervalo.
