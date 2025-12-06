from django import forms
from .models import Livro, Categoria


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = [
            'titulo',
            'autor',
            'categoria',
            'isbn',
            'descricao',
            'ano_publicacao',
            'quantidade_total',
            'quantidade_disponivel',
            'status'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título do livro'
            }),
            'autor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do autor'
            }),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 9788535929645'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrição do livro'
            }),
            'ano_publicacao': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number'
            }),
            'quantidade_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '1'
            }),
            'quantidade_disponivel': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '0'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da categoria'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da categoria'
            }),
        }
