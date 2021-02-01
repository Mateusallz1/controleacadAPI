from django.db import models

# Create your models here.
NUMBER_CHOICES = (
        (0, '0.0'),
        (0.5, '0.5'),
        (1, '1.0'),
        (1.5, '1.5'),
        (2, '2.0'),
        (2.5, '2.5'),
        (3, '3.0'),
        (3.5, '3.5'),
        (4, '4.0'),
        (4.5, '4.5'),
        (5, '5.0'),
        (5.5, '5.5'),
        (6, '6.0'),
        (6.5, '6.5'),
        (7, '7.0'),
        (7.5, '7.5'),
        (8, '8.0'),
        (8.5, '8.5'),
        (9, '9.0'),
        (9.5, '9.5'),
        (10, '10.0'),
    )

BIMESTRE_CHOICES = (
    (1, '1º BIMESTRE'),
    (2, '2º BIMESTRE'),
)

PERIODO_CHOICES = (
    (1, '1º PERÍODO'),
    (2, '2º PERÍODO'),
    (3, '3º PERÍODO'),
    (4, '4º PERÍODO'),
    (5, '5º PERÍODO'),
    (6, '6º PERÍODO'),
)

class Turma(models.Model):
    turno = models.CharField(max_length=15, null=False)
    sala = models.CharField(max_length=2, null=False, unique=True)
    
    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return str(self.pk)

class Professor(models.Model):
    name = models.CharField(max_length=100, null=False)
    titulacao = models.CharField(max_length=35, null=False)
    numero_licenca = models.IntegerField(null=False, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(self.name)

class Aluno(models.Model):
    name = models.CharField(max_length=100, null=False)
    idade = models.IntegerField(null=False)
    matricula = models.IntegerField(null=False, unique=True)
    email = models.EmailField(null=False, unique=True)

    def media(self, disci):
        nota1 = Nota.objects.filter(aluno=self, bimestre=1, disciplina=disci).values('nota')
        print(nota1)
        nota2 = Nota.objects.filter(aluno=self, bimestre=2, disciplina=disci).values('nota')
        print(nota2)
        a = float(nota1[0]['nota'])
        b = float(nota2[0]['nota'])
        media = (a+ b)/2
        return media

    def situacao(self, media):
        if media >= 7:
            return 'Aprovado'
        else:
            return 'Reprovado'

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(self.name)

class Disciplina(models.Model):
    name = models.CharField(max_length=75, null=False)
    turma = models.ForeignKey(Turma, related_name='turmas', on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, related_name='professor', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return str(self.name)
    
class Nota(models.Model):
    nota = models.DecimalField(null=False, choices=NUMBER_CHOICES, max_digits=3, decimal_places=1)
    bimestre = models.IntegerField(null=False, choices=BIMESTRE_CHOICES)
    periodo = models.IntegerField(default=1, null=False, choices=PERIODO_CHOICES)
    disciplina = models.ForeignKey(Disciplina, related_name='disciplina', on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, related_name='aluno', on_delete=models.CASCADE)

    class Meta:
        ordering = ('aluno',)

    def __str__(self):
        return str(self.aluno)