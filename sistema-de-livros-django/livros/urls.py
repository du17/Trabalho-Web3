from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    
    # Livros
    path('livros/', views.LivroListView.as_view(), name='livro_list'),
    path('livro/<int:pk>/', views.LivroDetailView.as_view(), name='livro_detail'),
    path('livro/novo/', views.LivroCreateView.as_view(), name='livro_create'),
    path('livro/<int:pk>/editar/', views.LivroUpdateView.as_view(), name='livro_update'),
    path('livro/<int:pk>/excluir/', views.LivroDeleteView.as_view(), name='livro_delete'),
    
    # Categorias
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categoria/novo/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categoria/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categoria/<int:pk>/excluir/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),
]
