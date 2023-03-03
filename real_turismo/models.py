from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Funcionario(models.Model):
    #username == matricula
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=100)
    
    #0 -> administrador, 1 -> motorista
    funcao = models.CharField(max_length=20)


    def __str__(self):
        return self.user.first_name
    
    def get (self):
        return self.user
    

class Veiculo(models.Model):
    codigo = models.IntegerField()
    placa = models.CharField(max_length=7)
    modelo = models.CharField(max_length=20)
    fabricante = models.CharField(max_length=20)
    #0 -> carro, 1 -> van,  2 -> onibus
    tipo = models.IntegerField()

    def __str__(self):
        return self.codigo
    

class Posto (models.Model):
    nome = models.CharField(max_length=20)
    cnpj = models.CharField(max_length=14)



    def __str__(self):
        return self.nome
class Abastecimento(models.Model):
    data = models.DateField(default=timezone.now)
    hodometro = models.FloatField()
    km_rodado = models.FloatField()
    valor_combustivel = models.DecimalField(max_digits=6, decimal_places=2)
    tipo_combustivel = models.CharField(max_length=20)

    EValidado = models.BooleanField(default=False)

    validador = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='validador')
    
    posto = models.ForeignKey(Posto, on_delete=models.CASCADE)
    motorista = models.ForeignKey(User, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)

    def __str__(self):
        return self.data