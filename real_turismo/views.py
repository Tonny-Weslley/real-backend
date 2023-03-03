from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from django.contrib.auth import authenticate

from rest_framework.parsers import JSONParser 
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.

from .models import Funcionario,Veiculo, Posto, Abastecimento, User
from .serializer import FuncionarioSerializer,VeiculoSerializer, PostoSerializer, AbastecimentoSerializer, CadastroSerializer, LoginSerializer, UserSerializer

#metodo para pegar usuario apartir do token
def get_user_from_token(request):
    try:
        auth = TokenAuthentication()
        user, token = auth.authenticate(request)
        return user
    except AuthenticationFailed:
        return None

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

    #abastecimentos de um funcionario
    @action(detail=False, methods=['get'], serializer_class=AbastecimentoSerializer, url_path='(?P<pk>[^/.]+)/ultimos_abastecimentos')
    def abastecimentos(self, request, pk=None):
        funcionario = User.objects.get(id=pk)
        print(funcionario)
        if funcionario is None:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            abastecimentos = Abastecimento.objects.filter(motorista=funcionario).order_by('-data')[:4]
            serializer = AbastecimentoSerializer(abastecimentos, many=True)
            return Response(serializer.data)

   #endpoint para validação de abastecimento
    @action(detail=False, methods=['get'], serializer_class=AbastecimentoSerializer, url_path='(?P<pk>[^/.]+)/validar_abastecimento')
    def validar_abastecimento(self, request, pk=None):
        abastecimento = get_object_or_404(Abastecimento, pk=pk)
        abastecimento.EValidado = True
        user = get_user_from_token(request)
        abastecimento.validador = user
        abastecimento.save()
        serializer = AbastecimentoSerializer(abastecimento)
        return Response(serializer.data)

class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

    #endpoint para pegar o ultimo abastecimento de um veiculo
    @action(detail=False, methods=['get'], serializer_class=AbastecimentoSerializer, url_path='(?P<pk>[^/.]+)/ultimo_abastecimento')
    def ultimo_abastecimento(self, request, pk=None):
        veiculo = get_object_or_404(Veiculo, pk=pk)
        abastecimento = Abastecimento.objects.filter(veiculo=veiculo).order_by('-data')[:4]
        serializer = AbastecimentoSerializer(abastecimento)
        return Response(serializer.data)



class PostoViewSet(viewsets.ModelViewSet):
    queryset = Posto.objects.all()
    serializer_class = PostoSerializer

    #endpoint para pegar os abastecimentos de um posto
    @action(detail=False, methods=['get'], serializer_class=AbastecimentoSerializer, url_path='(?P<pk>[^/.]+)/ultimo_abastecimento')
    def abastecimentos(self, request, pk=None):
        posto = get_object_or_404(Posto, pk=pk)
        abastecimentos = Abastecimento.objects.filter(posto=posto).order_by('-data')[:4]
        serializer = AbastecimentoSerializer(abastecimentos, many=True)
        return Response(serializer.data)

class AbastecimentoViewSet(viewsets.ModelViewSet):
    queryset = Abastecimento.objects.all()
    serializer_class = AbastecimentoSerializer


    def post (self, request):
        serializer = AbastecimentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Abastecimento.objects.all()
        veiculo = self.request.query_params.get('veiculo', None)
        if veiculo is not None:
            queryset = queryset.filter(veiculo=veiculo)
        return queryset
    
    #endpoint para pegar os abastecimentos que um usuario funcionario fez
    @action(detail=False, methods=['get'], serializer_class=FuncionarioSerializer)
    def abastecimentos_funcionarios(self, request, pk=None):
        funcionario = get_user_from_token(request)
        print(funcionario)
        if funcionario is None:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            abastecimentos = Abastecimento.objects.filter(motorista=funcionario)
            serializer = AbastecimentoSerializer(abastecimentos, many=True)
            return Response(serializer.data) 

 
   

#view para cadastro de usuarios funcionarios

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    authentication_classes = (TokenAuthentication,)
    
    @action(detail=False, methods=['post'],serializer_class=CadastroSerializer, url_path='cadastro')
    def cadastro(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        confirmed_password = request.data.get('confirmed_password')
        funcao = request.data.get('funcao')
        username = request.data.get('matricula') #matricula

        user = User.objects.filter(username=username).first()
        funcionario = Funcionario.objects.filter(matricula=username).first()

        #verifica se o usuario já existe
        if  (user or funcionario):
            return Response({'error': 'Usuário já existe'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            #verifica se as passwords são iguais
            if password != confirmed_password:
                return Response({'error': 'passwords não conferem'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                #cria o usuario
                user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
                user.save()
                #cria o funcionario
                funcionario = Funcionario.objects.create(user=user, funcao=funcao, matricula=username)
                funcionario.save()
                return Response({'success': 'Usuário criado com sucesso'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='login',serializer_class=LoginSerializer)
    def login(self, request):
        username = request.data.get('matricula')
        password = request.data.get('password')

        user = User.objects.filter(username=username)
        if (user):
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token:': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Usuário ou senha incorretos'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Usuário não existe'}, status=status.HTTP_400_BAD_REQUEST)