from django.db import models
from django.contrib.auth.models import User

# ============================
# MODELO: CATEGORIA
# ============================
class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        verbose_name_plural = "Categorias"


# ============================
# MODELO: LIVRO
# ============================
class Livro(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('emprestado', 'Emprestado'),
        ('indisponivel', 'Indisponível'),
    ]

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='livros'
    )
    isbn = models.CharField(max_length=13, unique=True)
    descricao = models.TextField(blank=True)
    ano_publicacao = models.IntegerField()
    quantidade_total = models.PositiveIntegerField(default=1)
    quantidade_disponivel = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='disponivel'
    )
    usuario_responsavel = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='livros_cadastrados'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

    class Meta:
        ordering = ['-criado_em']
        verbose_name_plural = "Livros"

    def pode_emprestar(self):
        return self.quantidade_disponivel > 0
