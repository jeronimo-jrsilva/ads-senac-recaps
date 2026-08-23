import os
import sys
import time
import json
import re
import subprocess
import unicodedata
from pathlib import Path

# Paths
REPO_ROOT = Path("/home/jeronimo/G-Sync/ads-senac-recaps")
RAW_DIR = REPO_ROOT / "s2_2026_2/00_transcricoes_brutas"
SEMANAL_DIR = REPO_ROOT / "s2_2026_2/02_semanal"
OUTPUT_HTML = REPO_ROOT / "portal/Recap_Master_S2.html"
TEMPLATE_PATH = REPO_ROOT / "engine/template_master_s2.html"
CSS_PATH = REPO_ROOT / "engine/styles.css"

SEMANAL_DIR.mkdir(parents=True, exist_ok=True)
(SEMANAL_DIR / "W_01").mkdir(parents=True, exist_ok=True)
(SEMANAL_DIR / "W_02").mkdir(parents=True, exist_ok=True)

# 1. Week Configs
w1_config = {
    "title": "Semana 1: Contrato Didático e Fundamentos de POO & C/C++",
    "text": "Abertura oficial do semestre 2026.2. Alinhamento de acordos pedagógicos, transição paradigmática de linguagens interpretadas (Python) para compiladas/orientadas a objetos, e imersão em POO, sintaxe e alocação de memória."
}
w2_config = {
    "title": "Semana 2: Modelagem, Banco de Dados Relacional e Estruturas Avançadas",
    "text": "Aprofundamento conceitual em arquiteturas de dados, modelo relacional, projeto integrador e práticas de encapsulamento e estruturas em C/C++."
}

with open(SEMANAL_DIR / "W_01/week_config.json", "w", encoding="utf-8") as f:
    json.dump(w1_config, f, ensure_ascii=False, indent=2)

with open(SEMANAL_DIR / "W_02/week_config.json", "w", encoding="utf-8") as f:
    json.dump(w2_config, f, ensure_ascii=False, indent=2)

# 2. Curadoria de Aulas
lessons_data = [
    # W_01
    {
        "file": SEMANAL_DIR / "W_01/poo_01.md",
        "title": "Programação Orientada a Objetos - Aula 01",
        "disciplina": "Programação Orientada a Objetos",
        "professor": "Docente Titular",
        "data": "2026-08-11",
        "content": """A aula inaugural de **Programação Orientada a Objetos (POO)** estabeleceu os alicerces teóricos e a justificativa histórica para a transição dos paradigmas procedural e estruturado para a modelagem orientada a objetos.

---

## 1. Do Procedural ao Paradigma Orientado a Objetos
No modelo estruturado clássico, dados e funções operam de forma desacoplada, expondo variáveis globais e facilitando efeitos colaterais indesejados à medida que a base de código cresce. A Orientação a Objetos reorganiza o sistema computacional em **entidades autocontidas** (Objetos) que agregam tanto o seu estado interno (atributos) quanto os seus comportamentos permitidos (métodos).

---

## 2. Contrato Didático e Metodologia de Avaliação
O docente detalhou a mecânica avaliativa do semestre:
- **Avaliações Regimentais (AV1 e AV2):** Foco na resolução prática de problemas e estruturação sintática.
- **Projetos Práticos Opcionais:** Possibilidade de substituição ou bonificação mediante entrega de relatórios e código de projetos individuais/integradores.
- **Participação Ativa:** A programação exige debug contínuo e enfrentamento direto da IDE, ultrapassando a mera observação passiva.

---

## 3. Ecossistema de Linguagens: Java vs JavaScript vs C#
Foi traçado um comparativo técnico e histórico entre as principais linguagens do mercado enterprise:
- **Java:** Linguagem estática e fortemente tipada rodando sobre a JVM (Java Virtual Machine). Famosa pelo seu rigor sintático ("Olá Mundo estruturado") e segurança de tipos em aplicações corporativas de grande escala.
- **JavaScript / Node.js:** Originalmente projetada para manipulação de DOM no frontend (criada para o Netscape e alavancada pelo time do Gmail/Google), evoluiu para o backend operando com estruturas orientadas a documentos e bancos NoSQL (como MongoDB).
- **C++ e C#:** Linguagens com forte aderência a controle de hardware e desenvolvimento na plataforma .NET.

```java
// Estrutura canônica de uma classe Java
public class Aluno {
    private String matricula;
    private String nome;

    public Aluno(String matricula, String nome) {
        this.matricula = matricula;
        this.nome = nome;
    }

    public void exibirDados() {
        System.out.println("Matrícula: " + this.matricula + " | Nome: " + this.nome);
    }
}
```

---

## Glossario
- **Classe**: Molde estrutural ou gabarito abstrato que define atributos e métodos de um tipo.
- **Objeto**: Instância concreta e alocada em memória de uma determinada classe.
- **JVM (Java Virtual Machine)**: Máquina virtual responsável pela execução de bytecode Java multiplataforma.
- **Encapsulamento**: Mecanismo de proteção do estado interno de um objeto através de modificadores de acesso.
- **Paradigma Orientado a Objetos**: Abordagem de engenharia de software baseada na interação entre entidades computacionais autônomas.
"""
    },
    {
        "file": SEMANAL_DIR / "W_01/cpp_01.md",
        "title": "C/C++ e Estruturas de Dados - Aula 01",
        "disciplina": "C/C++ e Estruturas de Dados",
        "professor": "Docente Titular",
        "data": "2026-08-12",
        "content": """Abertura da disciplina de **C/C++ e Estruturas de Dados**, focando no modelo de memória da máquina, processo de compilação e a anatomia de programas em C.

---

## 1. A Importância do C/C++ na Formação em Computação
Diferente de linguagens de alto nível com coleta de lixo automática (Garbage Collection), C e C++ exigem que o desenvolvedor compreenda a representação binária, o endereçamento de bytes na memória RAM e a hierarquia entre código fonte, assembly e binário executável.

---

## 2. Estrutura Canônica de um Programa em C
Análise da função `main`, diretivas de pré-processador (`#include`) e controle de fluxo básico:
- **`#include <stdio.h>`:** Inclusão dos protótipos de entrada e saída padrão.
- **`return 0;`:** Convenção do sistema operacional para indicar execução bem-sucedida (status code 0).

```c
#include <stdio.h>

int main() {
    int idade = 20;
    float media = 8.5;
    printf("Registro Acadêmico | Idade: %d, Média: %.2f\\n", idade, media);
    return 0;
}
```

---

## 3. Tipos Primitivos e Tamanho de Memória
Discussão sobre o operador `sizeof` e a representação de dados na arquitetura x86_64: `int` (4 bytes), `char` (1 byte), `float` (4 bytes), `double` (8 bytes).

---

## Glossario
- **Compilador**: Software que traduz código fonte em linguagem de alto nível diretamente para código de máquina executável.
- **Operador sizeof**: Operador unário em C que retorna o tamanho em bytes alocado para um tipo ou variável.
- **Diretiva de Pré-processador**: Instrução processada antes da compilação real (ex: `#include`, `#define`).
- **Stack (Pilha)**: Região de memória automática para variáveis locais e chamadas de função.
"""
    },
    {
        "file": SEMANAL_DIR / "W_01/cpp_02.md",
        "title": "C/C++ e Estruturas de Dados - Aula 02",
        "disciplina": "C/C++ e Estruturas de Dados",
        "professor": "Docente Titular",
        "data": "2026-08-13",
        "content": """Aprofundamento na manipulação de memória, passagem de parâmetros e introdução teórica e sintática a **Ponteiros** em C.

---

## 1. O Conceito de Endereço de Memória e Ponteiros
Toda variável declarada no programa ocupa um espaço físico na memória RAM referenciado por um endereço hexadecimal. Um **ponteiro** é uma variável especializada cujo valor é o endereço de memória de outra variável.
- **Operador `&` (Address-of):** Obtém o endereço de memória de uma variável.
- **Operador `*` (Dereference):** Acessa ou modifica o valor contido no endereço apontado.

```c
#include <stdio.h>

void dobraValor(int *ptr) {
    *ptr = (*ptr) * 2;
}

int main() {
    int numero = 25;
    printf("Valor antes: %d (Endereço: %p)\\n", numero, (void*)&numero);
    dobraValor(&numero);
    printf("Valor após ponteiro: %d\\n", numero);
    return 0;
}
```

---

## 2. Passagem por Valor vs Passagem por Referência
- **Por Valor:** O compilador cria uma cópia isolada na stack. Alterações locais não impactam a variável original.
- **Por Referência (Ponteiro):** Passa-se o endereço real da memória, permitindo mutabilidade de dados através de múltiplos escopos de funções.

---

## Glossario
- **Ponteiro**: Tipo especial de variável que armazena o endereço físico de outra variável na memória.
- **Dereferência (Operador *)**: Ação de ler ou escrever diretamente no endereço apontado pelo ponteiro.
- **Passagem por Referência**: Técnica de enviar o endereço de uma variável para uma função, evitando cópias e permitindo mutação.
- **Hexadecimal**: Sistema de numeração de base 16 amplamente utilizado para visualização legível de endereços de memória.
"""
    },
    {
        "file": SEMANAL_DIR / "W_01/pi_01.md",
        "title": "Projeto Integrador 3 - Aula 01",
        "disciplina": "Projeto Integrador 3",
        "professor": "Fred",
        "data": "2026-08-14",
        "content": """Abertura oficial da disciplina de **Projeto Integrador 3**, com alinhamento das metas semestrais, formação de grupos e definição de metodologias ágeis de entrega.

---

## 1. Escopo e Propósito do Projeto Integrador
O PI-3 atua como eixo articulador entre as disciplinas do semestre (*POO, Banco de Dados e C/C++*). A meta é o desenvolvimento de uma solução de software robusta, funcional e alinhada a necessidades reais de mercado ou gestão corporativa.

---

## 2. Requisitos de Governança e Metodologia
- **Git e GitHub:** Controle de versão obrigatório com branches por funcionalidade (`feature/xyz`).
- **Documentação de Requisitos:** Especificação formal de requisitos funcionais (RF) e não-funcionais (RNF).
- **Entregas Incrementais:** Validação de protótipos funcionais e modelagem de dados antes do fechamento final.

---

## Glossario
- **Requisitos Funcionais**: Descrições precisas das ações, comportamentos e regras de negócio que o software deve executar.
- **Branch**: Linha de desenvolvimento isolada no Git que permite implementar features sem desestabilizar a branch principal.
- **Projeto Integrador**: Unidade curricular focada na aplicação prática e integrada de conhecimentos teóricos multidisciplinares.
"""
    },
    # W_02
    {
        "file": SEMANAL_DIR / "W_02/bd_01.md",
        "title": "Banco de Dados Relacional - Aula 01",
        "disciplina": "Banco de Dados Relacional",
        "professor": "Docente Titular",
        "data": "2026-08-17",
        "content": """Introdução aos Sistemas de Gerenciamento de Bancos de Dados (**SGBDs**), modelo relacional de Edgar F. Codd e ciclo de vida de dados.

---

## 1. Da Persistência em Arquivos aos SGBDs
Discussão sobre as limitações de persistência manual em arquivos (redundância de dados, inconsistência, falta de concorrência e ausência de transações ACID) versus o poder analítico e a confiabilidade de um SGBD relacional.

---

## 2. Os Três Níveis de Abstração de Dados
1. **Nível Conceitual:** Visão de alto nível independente de tecnologia (Diagrama Entidade-Relacionamento).
2. **Nível Lógico:** Mapeamento em tabelas, colunas, tipos de dados e chaves relacionais.
3. **Nível Físico:** Armazenamento em disco, índices B-Tree e arquivos de dados.

---

## Glossario
- **SGBD**: Sistema de software responsável pelo gerenciamento, consulta, integridade e segurança de bases de dados.
- **Modelo Relacional**: Modelo de dados baseado na teoria de conjuntos e relações matemáticas organizadas em tabelas.
- **ACID**: Conjunto de propriedades essenciais de transações em bancos de dados: Atomicidade, Consistência, Isolamento e Durabilidade.
"""
    },
    {
        "file": SEMANAL_DIR / "W_02/poo_02.md",
        "title": "Programação Orientada a Objetos - Aula 02",
        "disciplina": "Programação Orientada a Objetos",
        "professor": "Docente Titular",
        "data": "2026-08-18",
        "content": """Consolidação dos pilares fundamentais da Orientação a Objetos: **Abstração, Encapsulamento, Métodos Construtores e Modificadores de Acesso**.

---

## 1. Construtores e Instanciação de Memória
O construtor é o método especial invocado no momento da instanciação (`new`) para inicializar o estado válido do objeto na memória heap.

```java
public class ContaBancaria {
    private String titular;
    private double saldo;

    public ContaBancaria(String titular, double saldoInicial) {
        this.titular = titular;
        this.saldo = Math.max(0, saldoInicial);
    }

    public boolean sacar(double valor) {
        if (valor > 0 && valor <= this.saldo) {
            this.saldo -= valor;
            return true;
        }
        return false;
    }
}
```

---

## 2. Modificadores de Acesso e Segurança de Estado
- **`private`:** Acesso restrito exclusivamente ao escopo da própria classe.
- **`public`:** Acesso livre por qualquer componente externo do sistema.
- **`protected`:** Acesso permitido para a classe e suas subclasses (herança).

---

## Glossario
- **Construtor**: Método de inicialização de instâncias executado no momento da alocação de memória do objeto.
- **Modificador de Acesso**: Palavra-chave que define a visibilidade e o nível de encapsulamento de classes, atributos e métodos.
- **Heap**: Área de memória dinâmica onde os objetos e estruturas instanciadas residem.
"""
    },
    {
        "file": SEMANAL_DIR / "W_02/cpp_03.md",
        "title": "C/C++ e Estruturas de Dados - Aula 03",
        "disciplina": "C/C++ e Estruturas de Dados",
        "professor": "Docente Titular",
        "data": "2026-08-19",
        "content": """Alocação Dinâmica de Memória em C e C++: Funções `malloc()`, `calloc()`, `free()` e operadores `new` e `delete`.

---

## 1. Alocação Estática vs Alocação Dinâmica
A alocação estática na stack possui tamanho fixo definido em tempo de compilação. A alocação dinâmica requisita blocos de memória na **heap** durante a execução do programa conforme a demanda real de dados.

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int n = 5;
    int *vetor = (int*) malloc(n * sizeof(int));

    if (vetor == NULL) {
        printf("Falha na alocação de memória!\\n");
        return 1;
    }

    for (int i = 0; i < n; i++) {
        vetor[i] = (i + 1) * 10;
        printf("vetor[%d] = %d\\n", i, vetor[i]);
    }

    // Liberação obrigatória de memória para evitar memory leak
    free(vetor);
    vetor = NULL;
    return 0;
}
```

---

## 2. Prevenção de Memory Leaks
Toda chamada a `malloc()` deve ter seu respectivo `free()`. O não desalocamento gera **vazamento de memória (memory leak)**, degradando o consumo de RAM do sistema ao longo do tempo.

---

## Glossario
- **malloc**: Função da biblioteca padrão de C (`stdlib.h`) que aloca um bloco contíguo de bytes não inicializados na heap.
- **free**: Função responsável por devolver o bloco de memória dinamicamente alocado de volta ao sistema operacional.
- **Memory Leak (Vazamento de Memória)**: Falha de programação onde a memória alocada na heap não é liberada após o término de seu uso.
- **NULL Pointer**: Ponteiro que não aponta para nenhum endereço de memória válido, utilizado como salvaguarda contra acessos indevidos.
"""
    },
    {
        "file": SEMANAL_DIR / "W_02/bd_02.md",
        "title": "Banco de Dados Relacional - Aula 02",
        "disciplina": "Banco de Dados Relacional",
        "professor": "Docente Titular",
        "data": "2026-08-20",
        "content": """Modelagem Conceitual de Dados: Diagrama Entidade-Relacionamento (**DER**), Cardinalidade (1:1, 1:N, N:M) e Chaves Primárias/Estrangeiras.

---

## 1. Componentes do Diagrama Entidade-Relacionamento (DER)
- **Entidades:** Objetos do mundo real sobre os quais os dados são coletados (ex: `Cliente`, `Pedido`).
- **Atributos:** Características descritivas das entidades (ex: `id`, `nome`, `cpf`).
- **Relacionamentos:** Associações e dependências de negócio entre entidades.

---

## 2. Chaves e Integridade Referencial
- **Chave Primária (PK):** Atributo identificador único e obrigatório de cada tupla em uma tabela.
- **Chave Estrangeira (FK):** Atributo que estabelece a ligação referencial com a chave primária de outra tabela, garantindo integridade e consistência.

---

## Glossario
- **DER (Diagrama Entidade-Relacionamento)**: Representação gráfica conceitual da estrutura de dados e suas inter-relações.
- **Chave Primária (PK)**: Campo ou conjunto de campos que identifica de forma inequívoca cada registro de uma tabela.
- **Chave Estrangeira (FK)**: Coluna que referencia a chave primária de outra tabela para manter a integridade relacional.
- **Cardinalidade**: Proporção numérica e restrição de ocorrências no relacionamento entre entidades (1:1, 1:N, N:M).
"""
    },
    {
        "file": SEMANAL_DIR / "W_02/pi_02.md",
        "title": "Projeto Integrador 3 - Aula 02",
        "disciplina": "Projeto Integrador 3",
        "professor": "Fred",
        "data": "2026-08-21",
        "content": """Validação de Propostas de Projeto e Definição de Arquitetura Técnica do PI-3.

---

## 1. Refinamento de Escopo e Viabilidade Técnica
Apresentação das primeiras ideias de cada equipe. Avaliação dos critérios de viabilidade:
- Conexão funcional entre backend orientado a objetos e banco relacional.
- Estruturação de APIs e tratamento consistente de erros.

---

## 2. Divisão de Papéis e Cronograma de Sprints
Definição do fluxo Scrum: Product Owner (PO), Scrum Master e equipe de desenvolvimento, com sprints de 2 semanas para entregas incrementais.

---

## Glossario
- **Sprint**: Período de tempo fixo (time-box) em métodos ágeis durante o qual um conjunto de entregas deve ser completado.
- **Scrum**: Framework ágil amplamente utilizado para gestão iterativa de projetos de desenvolvimento de software.
- **Backlog**: Lista priorizada de funcionalidades e requisitos aguardando desenvolvimento na fila do projeto.
"""
    },
    {
        "file": SEMANAL_DIR / "W_02/estudo_01.md",
        "title": "Laboratório de Práticas & Monitoria - Aula 01",
        "disciplina": "Práticas de Desenvolvimento",
        "professor": "Docente Titular",
        "data": "2026-08-22",
        "content": """Sessão prática em laboratório de informática focada em resolução de exercícios, compilação de ponteiros e depuração (debug) com `gdb`.

---

## 1. Exercícios de Fixação com Ponteiros
Implementação de algoritmos clássicos de manipulação de vetores dinâmicos, troca de valores (`swap`) e matrizes bidimensionais em C.

---

## 2. Práticas de Debug e Inspeção de Memória
Uso do depurador para visualizar frames de pilha (stack frames), endereços de ponteiros e validação de liberação de memória com `valgrind`.

---

## Glossario
- **GDB (GNU Debugger)**: Ferramenta de linha de comando para inspeção passo a passo e depuração de programas executáveis.
- **Valgrind**: Conjunto de ferramentas de análise de código e detecção de vazamentos de memória (memory leaks) em C/C++.
- **Stack Frame**: Bloco de memória alocado na stack para armazenar variáveis locais e contexto de retorno de uma função específica.
"""
    }
]

for lesson in lessons_data:
    with open(lesson["file"], "w", encoding="utf-8") as f:
        f.write(f'---\ntipo: portal\ntitulo: "{lesson["title"]}"\ndisciplina: "{lesson["disciplina"]}"\nsemestre: "2026.2"\ndata: {lesson["data"]}\nprofessor: "{lesson["professor"]}"\n---\n\n{lesson["content"]}\n')

print("✅ Todos os arquivos semanais gerados com sucesso!")

# 3. Execução do Motor de Build
def process_obsidian_callouts(md):
    def replace_callout(match):
        c_type = match.group(1).lower()
        title = match.group(2).strip()
        content = match.group(3).strip()
        lines = [line.replace('>', '', 1).strip() for line in content.split('\n')]
        clean_content = '<br>'.join(lines)
        icon = "💡"
        if c_type in ["caution", "warning", "danger"]: icon = "⚠️"
        elif c_type in ["important", "todo"]: icon = "❗"
        elif c_type in ["abstract", "summary"]: icon = "📋"
        elif c_type in ["tip", "hint"]: icon = "🎯"
        if not title: title = c_type.capitalize()
        return f'<div class="callout callout-{c_type}"><div class="callout-title">{icon} {title}</div><div class="callout-content">{clean_content}</div></div>'
    pattern = r'>\s*\[!(\w+)\]\s*(.*)\n((?:>\s*.*\n?)*)'
    return re.sub(pattern, replace_callout, md)

def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def convert_to_html(md):
    md = process_obsidian_callouts(md)
    def replace_pill(match):
        content = match.group(1).strip()
        return f'<span class="badge badge-poo">{content}</span>'
    md = re.sub(r'\[\[(.*?)\]\]', replace_pill, md)
    proc = subprocess.Popen(['pandoc', '-f', 'markdown', '-t', 'html'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out, _ = proc.communicate(input=md)
    return out

with open(CSS_PATH, 'r', encoding='utf-8') as f:
    master_css = f.read()

week_folders = sorted(list(SEMANAL_DIR.glob("W_*")))
global_glossary = {}
weeks_data = []
all_lessons_by_id = {}
ordered_lesson_ids = []

for folder in week_folders:
    w_id = folder.name
    w_num = w_id.replace("W_", "")
    config_path = folder / "week_config.json"
    config = {"title": f"Semana {w_num}", "text": "Consolidação das aulas da semana."}
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

    md_files = sorted(list(folder.glob("*.md")))
    lessons = []

    for p in md_files:
        with open(p, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        date_match = re.search(r'data:\s*([\d-]+)', raw_text)
        disc_match = re.search(r'disciplina:\s*"(.*?)"', raw_text)
        prof_match = re.search(r'professor:\s*"(.*?)"', raw_text)
        tit_match = re.search(r'titulo:\s*"(.*?)"', raw_text)

        date = date_match.group(1) if date_match else "2026-08-10"
        disc = disc_match.group(1) if disc_match else "Geral"
        prof = prof_match.group(1) if prof_match else "Docente"
        titulo = tit_match.group(1) if tit_match else p.stem

        l_id = f"lesson-{w_id}-{p.stem}"
        ordered_lesson_ids.append(l_id)

        badge_cls = "badge-poo"
        disc_lower = disc.lower()
        if "c++" in disc_lower or "linguagem c" in disc_lower: badge_cls = "badge-cpp"
        elif "banco" in disc_lower or "dados" in disc_lower: badge_cls = "badge-bd"
        elif "projeto" in disc_lower: badge_cls = "badge-pi"

        parts = re.split(r'##\s*Gloss[aá]rio', raw_text, flags=re.IGNORECASE)
        if len(parts) > 1:
            matches = re.finditer(r'-\s*\*\*(.*?)\*\*[:\s]*(.*?)(?=\n-\s*\*\*|\Z)', parts[1], re.DOTALL)
            for m in matches:
                term = m.group(1).strip()
                norm = term.lower()
                definition = convert_to_html(m.group(2).strip())
                if norm not in global_glossary:
                    global_glossary[norm] = {"term": term, "def": definition, "sources": []}
                global_glossary[norm]["sources"].append({"id": l_id, "name": f"{disc} ({date})"})

        body_md = parts[0].split('---', 2)[-1].strip()
        body_html = convert_to_html(body_md)

        lesson_obj = {
            "id": l_id,
            "title": titulo,
            "disciplina": disc,
            "professor": prof,
            "data": date,
            "badge_cls": badge_cls,
            "html": body_html,
            "week_id": w_id
        }
        lessons.append(lesson_obj)
        all_lessons_by_id[l_id] = lesson_obj

    weeks_data.append({
        "id": w_id,
        "title": config.get("title", f"Semana {w_num}"),
        "desc": config.get("text", ""),
        "lessons": lessons
    })

# Nav map
nav_map = {
    "dashboard": {"label": "Dashboard", "prev": None, "next": ordered_lesson_ids[0] if ordered_lesson_ids else None}
}
for i, l_id in enumerate(ordered_lesson_ids):
    prev_id = ordered_lesson_ids[i - 1] if i > 0 else "dashboard"
    next_id = ordered_lesson_ids[i + 1] if i < len(ordered_lesson_ids) - 1 else "glossary"
    nav_map[l_id] = {
        "label": all_lessons_by_id[l_id]["title"],
        "prev": prev_id,
        "next": next_id
    }
nav_map["glossary"] = {
    "label": "Glossário",
    "prev": ordered_lesson_ids[-1] if ordered_lesson_ids else "dashboard",
    "next": None
}

# Disciplines view
disciplines = {}
for l_id in ordered_lesson_ids:
    l = all_lessons_by_id[l_id]
    d = l["disciplina"]
    if d not in disciplines:
        disciplines[d] = {"prof": l["professor"], "badge": l["badge_cls"], "lessons": []}
    disciplines[d]["lessons"].append(l)

disc_cards_html = ['<div class="tracks-grid">']
for d, data in disciplines.items():
    pills = "".join([f'<a href="javascript:void(0)" onclick="showSection(\'{l[\'id\']}\')" class="lesson-pill-btn">{l[\'data\'].split("-")[2]}/{l[\'data\'].split("-")[1]} - {l[\'title\']}</a>' for l in data["lessons"]])
    disc_cards_html.append(f'''
        <div class="track-card">
            <span class="badge {data['badge']}">{d}</span>
            <div class="track-title" style="margin-top: 10px;">{d}</div>
            <div class="track-prof">Prof. {data['prof']}</div>
            <div class="track-lessons">{pills}</div>
        </div>
    ''')
disc_cards_html.append('</div>')
discipline_view = "".join(disc_cards_html)

# Timeline view
timeline_html = []
for w in weeks_data:
    cards_html = []
    for l in w["lessons"]:
        cards_html.append(f'''
            <div class="week-card-item" onclick="showSection('{l['id']}')">
                <div class="item-meta">
                    <span class="badge {l['badge_cls']}">{l['disciplina']}</span> &bull; {l['data']} &bull; Prof. {l['professor']}
                </div>
                <div class="item-title">{l['title']}</div>
            </div>
        ''')
    timeline_html.append(f'''
        <div class="timeline-section">
            <div class="week-header">{w['title']}</div>
            <div class="week-desc">{w['desc']}</div>
            <div class="week-cards-grid">
                {"".join(cards_html)}
            </div>
        </div>
    ''')
timeline_content = "".join(timeline_html)

# Lessons sections
lessons_html = []
for l_id in ordered_lesson_ids:
    l = all_lessons_by_id[l_id]
    lessons_html.append(f'''
        <section id="{l['id']}" class="spa-section">
            <div class="lesson-card">
                <div class="lesson-metadata">
                    <span class="badge {l['badge_cls']}">{l['disciplina']}</span>
                    <span>📅 {l['data']}</span>
                    <span>👨‍🏫 Prof. {l['professor']}</span>
                </div>
                <h1 style="font-size: 1.6rem; margin-bottom: 20px;">{l['title']}</h1>
                <div class="lesson-body">
                    {l['html']}
                </div>
            </div>
        </section>
    ''')
lessons_content = "".join(lessons_html)

# Glossary section
glossary_html = []
sorted_terms = sorted(global_glossary.keys())
for t_key in sorted_terms:
    item = global_glossary[t_key]
    sources_html = "".join([f'<a href="javascript:void(0)" onclick="showSection(\'{s[\'id\']}\')" class="source-tag">{s[\'name\']}</a>' for s in item["sources"]])
    t_id = f"term-{slugify(item['term'])}"
    glossary_html.append(f'''
        <div class="glossary-card" id="{t_id}">
            <div class="glossary-term">{item['term']}</div>
            <div class="glossary-def">{item['def']}</div>
            <div class="glossary-sources">{sources_html}</div>
        </div>
    ''')
glossary_content = "".join(glossary_html)

with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    template = f.read()

output = template.replace("{{MASTER_CSS}}", master_css)
output = output.replace("{{TOTAL_WEEKS}}", str(len(weeks_data)))
output = output.replace("{{TOTAL_LESSONS}}", str(len(ordered_lesson_ids)))
output = output.replace("{{GLOSSARY_COUNT}}", str(len(global_glossary)))
output = output.replace("{{DISCIPLINE_VIEW}}", discipline_view)
output = output.replace("{{TIMELINE_CONTENT}}", timeline_content)
output = output.replace("{{LESSONS_CONTENT}}", lessons_content)
output = output.replace("{{GLOSSARY_CONTENT}}", glossary_content)
output = output.replace("{{NAV_MAP}}", json.dumps(nav_map, indent=2))

OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(output)

print(f"🎉 Portal SSOT 2026.2 gerado com sucesso em: {OUTPUT_HTML}")
