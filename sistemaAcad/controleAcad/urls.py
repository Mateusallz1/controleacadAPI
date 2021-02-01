from django.contrib import admin
from django.urls import path, include
from controleAcad import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth', include('rest_framework.urls')),
    path('api-root/', views.ApiRoot.as_view(), name=views.ApiRoot.name),
    path('turma/', views.TurmaLista.as_view(), name=views.TurmaLista.name),
    path('turma/<int:pk>/', views.TurmaDetalhe.as_view(), name=views.TurmaDetalhe.name),
    path('professor/', views.ProfessorLista.as_view(), name=views.ProfessorLista.name),
    path('professor/<int:pk>/', views.ProfessorDetalhe.as_view(), name=views.ProfessorDetalhe.name),
    path('aluno/', views.AlunoLista.as_view(), name=views.AlunoLista.name),
    path('aluno/<int:pk>/', views.AlunoDetalhe.as_view(), name=views.AlunoDetalhe.name),
    path('disciplina/', views.DisciplinaLista.as_view(), name=views.DisciplinaLista.name),
    path('disciplina/<int:pk>/', views.DisciplinaDetalhe.as_view(), name=views.DisciplinaDetalhe.name),
    path('nota/', views.NotaLista.as_view(), name=views.NotaLista.name),
    path('nota/<int:pk>/', views.NotaDetalhe.as_view(), name=views.NotaDetalhe.name),
    path('periodo-aluno/<int:pk>/disciplina/<int:disciplina_id>/', views.AlunoPeriodo.as_view(), name=views.AlunoPeriodo.name),
]
