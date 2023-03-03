from django.contrib import admin
from .models import Funcionario,Veiculo, Posto, Abastecimento

# Register your models here.
admin.site.register(Funcionario)
admin.site.register(Veiculo)
admin.site.register(Posto)
admin.site.register(Abastecimento)