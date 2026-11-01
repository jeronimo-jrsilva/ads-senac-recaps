---
tipo: portal
titulo: "Programação Orientada a Objetos - Aula 07"
disciplina: "Programação Orientada a Objetos"
semestre: "2026.2"
data: 2026-10-20
professor: "Tibério"
---

A sétima aula de **Programação Orientada a Objetos (POO)** com o Professor Tibério explorou a fronteira entre os modelos orientados a objetos e os sistemas de armazenamento persistente, estabelecendo as bases do que no mercado se consolida como Mapeamento Objeto-Relacional (ORM).

---

## 1. O Descompasso de Impedância Objeto-Relacional
O Professor Tibério explicou que em memória o software opera sobre grafos de objetos encapsulados, tipos complexos e herança:
- Um banco de dados relacional tradicional opera sobre **tabelas bidimensionais** (linhas e colunas atômicas).
- Por isso, não é possível simplesmente "salvar um objeto inteiro" em uma célula do banco sem desmembrá-lo.
- O desenvolvedor precisa **desmontar o objeto**: extrair seus atributos primitivos, convertê-los em tipos relacionais (`VARCHAR`, `INT`, `DECIMAL`) e estruturar as chaves estrangeiras necessárias para refletir as composições.

---

## 2. Padrões de Projeto para Acesso a Dados (DAO)
Foi apresentada a arquitetura limpa de separação de responsabilidades:
- **Entidades (Model):** Classes puras representando conceitos de domínio (`Aluno`, `Curso`, `Matricula`).
- **Camada de Acesso a Dados (DAO - Data Access Object):** Responsável exclusiva por traduzir chamadas orientadas a objetos em instruções SQL estruturadas (`INSERT`, `SELECT`, `UPDATE`).

```java
// Exemplo de padrão conceitual de desmontagem de entidade para persistência
public class AlunoDAO {
    public void salvar(Aluno aluno) {
        String sql = "INSERT INTO Aluno (nome, email, matricula) VALUES (?, ?, ?)";
        // Os atributos do objeto são extraídos e vinculados aos parâmetros SQL
        try (PreparedStatement stmt = conexao.prepareStatement(sql)) {
            stmt.setString(1, aluno.getNome());
            stmt.setString(2, aluno.getEmail());
            stmt.setString(3, aluno.getMatricula());
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao persistir aluno", e);
        }
    }
}
```
