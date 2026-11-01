from django.db import models


class Professor(models.Model):
    nome = models.CharField(max_length=150, unique=True, verbose_name="Nome do Docente")
    papel = models.CharField(max_length=100, default="Docente Titular", verbose_name="Papel / Cargo")

    class Meta:
        db_table = "professores"
        verbose_name = "Professor"
        verbose_name_plural = "Professores"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Disciplina(models.Model):
    nome = models.CharField(max_length=150, unique=True, verbose_name="Nome da Disciplina")
    sigla = models.CharField(max_length=20, verbose_name="Sigla")
    cor = models.CharField(max_length=20, default="#94a3b8", verbose_name="Cor Primária")
    bg_color = models.CharField(max_length=50, default="rgba(148, 163, 184, 0.12)", verbose_name="Cor de Fundo")
    border_color = models.CharField(max_length=50, default="rgba(148, 163, 184, 0.4)", verbose_name="Cor da Borda")
    ordem = models.IntegerField(default=99, verbose_name="Ordem de Exibição")

    class Meta:
        db_table = "disciplinas"
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ["ordem", "nome"]

    def __str__(self):
        return f"{self.sigla} - {self.nome}"


class Semana(models.Model):
    numero = models.IntegerField(unique=True, verbose_name="Número da Semana")
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código (ex: W01)")
    titulo = models.CharField(max_length=255, verbose_name="Título da Semana")
    descricao = models.TextField(blank=True, verbose_name="Descrição / Resumo da Semana")

    class Meta:
        db_table = "semanas"
        verbose_name = "Semana Letiva"
        verbose_name_plural = "Semanas Letivas"
        ordering = ["numero"]

    def __str__(self):
        return f"Semana {self.numero:02d}: {self.titulo[:40]}"


class Aula(models.Model):
    semana = models.ForeignKey(Semana, on_delete=models.CASCADE, related_name="aulas", verbose_name="Semana")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name="aulas", verbose_name="Disciplina")
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="aulas", verbose_name="Docente")
    slug_arquivo = models.CharField(max_length=100, verbose_name="Slug / Arquivo Base")
    titulo = models.CharField(max_length=255, verbose_name="Título da Aula")
    data_aula = models.CharField(max_length=20, blank=True, verbose_name="Data (YYYY-MM-DD)")
    rotulo = models.CharField(max_length=50, blank=True, verbose_name="Rótulo / Pílula (ex: Aula 01)")
    conteudo_markdown = models.TextField(verbose_name="Conteúdo Markdown Completo")

    class Meta:
        db_table = "aulas"
        verbose_name = "Aula / Registro"
        verbose_name_plural = "Aulas / Registros"
        ordering = ["semana__numero", "data_aula", "id"]

    def __str__(self):
        return f"[{self.semana.codigo}] {self.disciplina.sigla} - {self.titulo[:45]}"


class GlossarioTermo(models.Model):
    termo = models.CharField(max_length=150, unique=True, verbose_name="Termo Técnico")
    slug = models.CharField(max_length=150, unique=True, verbose_name="Slug")
    definicao = models.TextField(verbose_name="Definição Didática")
    wiki_url = models.URLField(blank=True, null=True, verbose_name="Link de Referência / Wikipedia")
    aulas = models.ManyToManyField(Aula, through="GlossarioAula", related_name="termos_glossario", blank=True)

    class Meta:
        db_table = "glossario_termos"
        verbose_name = "Termo de Glossário"
        verbose_name_plural = "Termos de Glossário"
        ordering = ["termo"]

    def __str__(self):
        return self.termo


class GlossarioAula(models.Model):
    termo = models.ForeignKey(GlossarioTermo, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)

    class Meta:
        db_table = "glossario_aulas"
        unique_together = ("termo", "aula")
