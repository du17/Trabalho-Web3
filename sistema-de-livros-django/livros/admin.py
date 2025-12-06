from django.contrib import admin
from .models import Livro, Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criada_em')
    search_fields = ('nome',)


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'autor',
        'categoria',
        'status',
        'quantidade_disponivel',
        'criado_em'
    )
    list_filter = ('status', 'categoria', 'criado_em')
    search_fields = ('titulo', 'autor', 'isbn')
    readonly_fields = ('criado_em', 'atualizado_em')
