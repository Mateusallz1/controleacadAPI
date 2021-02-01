from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.parsers import JSONParser
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from controleAcad.models import Turma, Professor, Aluno, Disciplina, Nota
from controleAcad.serializers import TurmaSerializer, ProfessorSerializer, AlunoSerializer, DisciplinaSerializer, NotaSerializer, PeriodoAlunoSerializer, NotaPermitidaSerializer

# Create your views here.

class TurmaLista(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    name = 'turma-list'
    # permission_classes = (permissions.IsAuthenticated,)

class TurmaDetalhe(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    name = 'turma-detail'
    # permission_classes = (permissions.IsAuthenticated,)

class ProfessorLista(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    name = 'professor-list'
    # permission_classes = (permissions.IsAuthenticated,)

class ProfessorDetalhe(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    name = 'professor-detail'
    # permission_classes = (permissions.IsAuthenticated,)

class AlunoLista(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    name = 'aluno-list'
    # permission_classes = (permissions.IsAuthenticated,)

class AlunoDetalhe(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    name = 'aluno-detail'
    # permission_classes = (permissions.IsAuthenticated,)

class DisciplinaLista(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    name = 'disciplina-list'
    # permission_classes = (permissions.IsAuthenticated,)

class DisciplinaDetalhe(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    name = 'disciplina-detail'
    # permission_classes = (permissions.IsAuthenticated,)

class NotaLista(LoginRequiredMixin, generics.ListCreateAPIView):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
    name = 'nota-list'
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        aluno_request = Aluno.objects.filter(name=self.request.data['aluno']).values()
        queryset = Nota.objects.filter(aluno__id=aluno_request[0]['id']).values()
        lista_nota = queryset.values('pk','nota','bimestre','periodo','disciplina')
        for i in lista_nota:
            disciplina = Disciplina.objects.filter(pk=i['disciplina']).values()
            if self.request.data['bimestre'] == str(i['bimestre']) and self.request.data['periodo'] == str(i['periodo']) and self.request.data['disciplina'] == disciplina[0]['name']:
                return Response(status=status.HTTP_304_NOT_MODIFIED)
            else:
                disciplina1 = Disciplina.objects.get(name=self.request.data['disciplina'])
                aluno1 = Aluno.objects.get(name=self.request.data['aluno'])
                data = {'nota':float(self.request.data['nota']),'bimestre':int(self.request.data['bimestre']),'periodo':int(self.request.data['periodo']),'disciplina':disciplina1,'aluno':aluno1}
                nota = Nota(aluno=aluno1,bimestre=int(self.request.data['bimestre']),disciplina=disciplina1,nota=float(self.request.data['nota']),periodo=int(self.request.data['periodo']))
                nota.save()
                serializer = NotaSerializer(data)
                return Response(serializer.data, status=status.HTTP_200_OK)
        
class NotaDetalhe(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
    name = 'nota-detail'
    # permission_classes = (permissions.IsAuthenticated,)

class AlunoPeriodo(LoginRequiredMixin, generics.ListAPIView):
    name = 'periodo-aluno'
    # permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        aluno_request = Aluno.objects.get(pk=kwargs['pk'])
        disciplina = Nota.objects.filter(pk=kwargs['disciplina_id']).values('disciplina_id')
        media = aluno_request.media(disciplina[0]['disciplina_id'])
        situacao = aluno_request.situacao(media)
        data = {'pk':aluno_request.pk, 'nome':aluno_request.name, 'media':media, 'situacao':situacao}
        serializer = PeriodoAlunoSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ApiRoot(LoginRequiredMixin, generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'alunos': reverse(AlunoLista.name, request=request),
            'professores': reverse(ProfessorLista.name, request=request),
            'turmas': reverse(TurmaLista.name, request=request),
            'disciplinas': reverse(DisciplinaLista.name, request=request),
        })