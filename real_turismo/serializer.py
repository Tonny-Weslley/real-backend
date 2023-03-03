from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import Abastecimento, Funcionario, Posto, Veiculo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ('id','user', 'funcao', 'matricula')

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = ('id', 'codigo', 'placa', 'modelo', 'fabricante', 'tipo')

class PostoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posto
        fields = ('id', 'nome', 'cnpj')

class AbastecimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abastecimento
        fields = ('id', 'data', 'hodometro', 'valor_combustivel','km_rodado' ,'tipo_combustivel','EValidado','validador' ,'posto', 'motorista', 'veiculo')


#serializer para cadastro de usuarios funcionarios
class CadastroSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=100)
    funcao = serializers.IntegerField()
    matricula = serializers.CharField(max_length=100) #matricula
    password = serializers.CharField(max_length=40,)
    confirmed_password = serializers.CharField(max_length=40)
    class Meta:
        model = Funcionario
        fields = fields = ('id', 'first_name','last_name', 'funcao', 'matricula', 'password','confirmed_password')

class LoginSerializer(serializers.Serializer):
    matricula = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=40)

