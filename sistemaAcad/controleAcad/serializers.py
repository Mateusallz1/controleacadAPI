from django.contrib.auth.models import User

from rest_framework import serializers
from controleAcad.models import Turma, Professor, Aluno, Disciplina, Nota

class TurmaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Turma
        fields = ('pk','turno','sala')

class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ('pk','name','titulacao','numero_licenca')

class AlunoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Aluno
        fields = ('name','pk','idade','matricula','email')

class DisciplinaSerializer(serializers.HyperlinkedModelSerializer):
    turma = serializers.SlugRelatedField(queryset=Turma.objects.all(), slug_field='sala')
    professor = serializers.SlugRelatedField(queryset=Professor.objects.all(), slug_field='name')

    class Meta:
        model = Disciplina
        fields = ('name','pk','turma','professor')

class NotaSerializer(serializers.HyperlinkedModelSerializer):
    disciplina = serializers.SlugRelatedField(queryset=Disciplina.objects.all(), slug_field='name')
    aluno = serializers.SlugRelatedField(queryset=Aluno.objects.all(), slug_field='name')
    
    class Meta:
        model = Nota
        fields = ('nota','bimestre','periodo','disciplina','aluno')

class PeriodoAlunoSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    nome = serializers.CharField()
    media = serializers.IntegerField()
    situacao = serializers.CharField()

class NotaPermitidaSerializer(serializers.Serializer):
    nota = serializers.DecimalField(max_digits=3, decimal_places=1)
    bimestre = serializers.IntegerField()
    periodo = serializers.IntegerField()
    disciplina = serializers.CharField()
    aluno = serializers.CharField()
