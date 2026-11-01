from django.contrib import admin
from .models import Professor, Disciplina, Semana, Aula, GlossarioTermo, GlossarioAula


class GlossarioAulaInline(admin.TabularInline):
    model = GlossarioAula
    extra = 1


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("nome", "papel", "total_aulas")
    search_fields = ("nome", "papel")

    def total_aulas(self, obj):
        return obj.aulas.count()
    total_aulas.short_description = "Aulas Ministradas"


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ("sigla", "nome", "ordem", "cor", "total_aulas")
    list_editable = ("ordem",)
    search_fields = ("nome", "sigla")

    def total_aulas(self, obj):
        return obj.aulas.count()
    total_aulas.short_description = "Aulas Registradas"


@admin.register(Semana)
class SemanaAdmin(admin.ModelAdmin):
    list_display = ("numero", "codigo", "titulo", "total_aulas")
    search_fields = ("titulo", "descricao", "codigo")
    ordering = ("numero",)

    def total_aulas(self, obj):
        return obj.aulas.count()
    total_aulas.short_description = "Qtd. Aulas"


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "semana", "disciplina", "professor", "data_aula", "rotulo")
    list_filter = ("semana", "disciplina", "professor")
    search_fields = ("titulo", "conteudo_markdown", "rotulo")
    autocomplete_fields = ("disciplina", "professor", "semana")
    inlines = [GlossarioAulaInline]


@admin.register(GlossarioTermo)
class GlossarioTermoAdmin(admin.ModelAdmin):
    list_display = ("termo", "slug", "wiki_url", "total_aulas")
    search_fields = ("termo", "definicao", "slug")
    prepopulated_fields = {"slug": ("termo",)}

    def total_aulas(self, obj):
        return obj.aulas.count()
    total_aulas.short_description = "Aulas Vinculadas"
