---
tipo: portal
titulo: "Lógica de Programação em Python - Aula 10"
disciplina: "Lógica de Programação em Python"
semestre: "2026.1"
data: 2026-03-24
professor: "Nator Junior"
---

Esta sessão aprofunda o estudo de coleções em Python, introduzindo os dicionários como ferramentas de organização semântica. O foco recai sobre a estrutura de chave-valor e a criação de arquiteturas de dados compostas, preparando o terreno para o desenvolvimento de sistemas de gestão complexos.

---

## 1. Dicionários: Estruturas de Chave-Valor
Diferente das listas, os dicionários oferecem uma forma mais intuitiva e rotulada de acessar informações:

- **Acesso Semântico**: Utilização de etiquetas (chaves) em vez de índices numéricos para recuperar valores.
- **Declaração e Sintaxe**: Uso de chaves `{}` para definir o dicionário, associando identificadores a dados.
# Exemplo Prático:
```python
# Criando um dicionário
aluno = {
    "nome": "Jeronimo",
    "idade": 42,
    "curso": "ADS"
}

# Acessando valor via chave
print(aluno["nome"]) # Saída: Jeronimo
```

---

## 2. Manipulação Dinâmica de Dados
A flexibilidade dos dicionários permite a atualização constante das informações em tempo de execução:

- **Atribuição Direta**: Facilidade para criar ou atualizar chaves existentes através do operador de atribuição.
- **Remoção de Entradas**: Uso do comando `del` para excluir permanentemente chaves e seus respectivos valores.
- **Aninhamento de Tipos**: Suporte para que valores sejam outras coleções, permitindo hierarquias complexas.

```python
# Atualizando e Adicionando dados
aluno["idade"] = 43      # Atualiza
aluno["email"] = "jr@email.com" # Cria nova chave

# Removendo dado
del aluno["curso"]
```

---

## 3. Estruturas Compostas e Modelagem
A combinação de coleções simula o comportamento de bancos de dados relacionais e é ideal para gerenciar turmas ou estoques:

- **Listas de Dicionários**: Técnica para gerenciar múltiplos registros de forma estruturada.
```python
turma = [
    {"nome": "Ana", "nota": 10},
    {"nome": "Bruno", "nota": 8},
    {"nome": "Carla", "nota": 9}
]

# Percorrendo a lista de dicionários
for aluno in turma:
    print(f"Aluno: {aluno['nome']} | Nota: {aluno['nota']}")
```

---

## 4. Planejamento Acadêmico e Avaliações
O encerramento do conteúdo técnico é acompanhado pelas diretrizes para as composições de notas do semestre:

- **Trabalhos Práticos**: Exigência de aplicação integral de variáveis, condicionais, laços e estruturas de dados.
- **Desenvolvimento de Minissistemas**: Foco na autonomia técnica para resolver problemas propostos através de código funcional.
- **Composição da Média**: Divisão da pontuação entre projetos práticos e avaliação teórica individual.

---

## Glossario

- **Dicionário (Dict)**: Estrutura de dados que armazena pares de chave e valor, onde cada chave é única. [Wikipedia](https://pt.wikipedia.org/wiki/Dicion%C3%A1rio_(tipo_de_dado))
- **Chave-Valor**: Paradigma de armazenamento onde um identificador único mapeia para um dado específico.
- **Semântica**: No contexto de código, refere-se ao significado e clareza das instruções para seres humanos.
- **Estrutura Composta**: Agrupamento de diferentes tipos de dados e coleções em uma única variável complexa.
