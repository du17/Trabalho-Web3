from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Livro, Categoria
from .forms import LivroForm, CategoriaForm


# ============================
# LIVROS - VIEWS
# ============================

class LivroListView(LoginRequiredMixin, ListView):
    model = Livro
    template_name = 'livros/livro_list.html'
    context_object_name = 'livros'
    paginate_by = 10

    def get_queryset(self):
        queryset = Livro.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) |
                Q(autor__icontains=query) |
                Q(isbn__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_livros'] = Livro.objects.count()
        context['livros_disponiveis'] = Livro.objects.filter(
            status='disponivel'
        ).count()
        return context


class LivroDetailView(LoginRequiredMixin, DetailView):
    model = Livro
    template_name = 'livros/livro_detail.html'
    context_object_name = 'livro'


class LivroCreateView(LoginRequiredMixin, CreateView):
    model = Livro
    form_class = LivroForm
    template_name = 'livros/livro_form.html'
    success_url = reverse_lazy('livro_list')

    def form_valid(self, form):
        form.instance.usuario_responsavel = self.request.user
        return super().form_valid(form)


class LivroUpdateView(LoginRequiredMixin, UpdateView):
    model = Livro
    form_class = LivroForm
    template_name = 'livros/livro_form.html'
    success_url = reverse_lazy('livro_list')


class LivroDeleteView(LoginRequiredMixin, DeleteView):
    model = Livro
    template_name = 'livros/livro_confirm_delete.html'
    success_url = reverse_lazy('livro_list')


# ============================
# CATEGORIAS - VIEWS
# ============================

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'livros/categoria_list.html'
    context_object_name = 'categorias'


class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'livros/categoria_form.html'
    success_url = reverse_lazy('categoria_list')


class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'livros/categoria_form.html'
    success_url = reverse_lazy('categoria_list')


class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'livros/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria_list')


# ============================
# AUTENTICAÇÃO - VIEWS
# ============================

def login_view(request):
    from django.contrib.auth import authenticate, login
    
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect("livro_list")
        else:
            return render(
                request,
                'livros/login.html',
                {'error': 'Usuário ou senha inválidos'}
            )
    
    return render(request, 'livros/login.html')


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    context = {
        'total_livros': Livro.objects.count(),
        'livros_disponiveis': Livro.objects.filter(status='disponivel').count(),
        'total_categorias': Categoria.objects.count(),
        'ultimos_livros': Livro.objects.all()[:5],
    }
    return render(request, 'livros/dashboard.html', context)
