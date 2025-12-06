import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca.settings')
django.setup()

from django.contrib.auth.models import User
from livros.models import Categoria, Livro

# Criar usuário admin se não existir
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@biblioteca.local', 'admin')
    print("Usuário admin criado com sucesso!")

# Criar categorias
categorias_nomes = [
    'Ficção Científica',
    'Romance',
    'Mistério',
    'Tecnologia',
    'Autoajuda',
    'História'
]

for nome in categorias_nomes:
    categoria, created = Categoria.objects.get_or_create(
        nome=nome,
        defaults={'descricao': f'Categoria de {nome}'}
    )
    if created:
        print(f"Categoria '{nome}' criada!")

# Criar alguns livros de exemplo
livros_dados = [
    {
        'titulo': 'Fundação',
        'autor': 'Isaac Asimov',
        'categoria': 'Ficção Científica',
        'isbn': '9788535914778',
        'ano_publicacao': 1951,
        'quantidade_total': 5,
        'descricao': 'A história de como uma organização tenta salvar a humanidade de um futuro sombrio.'
    },
    {
        'titulo': 'Senhor dos Anéis',
        'autor': 'J.R.R. Tolkien',
        'categoria': 'Ficção Científica',
        'isbn': '9788532530787',
        'ano_publicacao': 1954,
        'quantidade_total': 3,
        'descricao': 'Uma jornada épica através de um mundo fantástico.'
    },
    {
        'titulo': 'O Código Da Vinci',
        'autor': 'Dan Brown',
        'categoria': 'Mistério',
        'isbn': '9788532506015',
        'ano_publicacao': 2003,
        'quantidade_total': 4,
        'descricao': 'Um thriller que mistura arte, história e religião.'
    },
]

usuario_admin = User.objects.get(username='admin')

for livro_info in livros_dados:
    categoria = Categoria.objects.get(nome=livro_info.pop('categoria'))
    livro, created = Livro.objects.get_or_create(
        isbn=livro_info['isbn'],
        defaults={
            **livro_info,
            'categoria': categoria,
            'usuario_responsavel': usuario_admin,
            'quantidade_disponivel': livro_info['quantidade_total']
        }
    )
    if created:
        print(f"Livro '{livro.titulo}' criado!")

print("\nDados de exemplo criados com sucesso!")
