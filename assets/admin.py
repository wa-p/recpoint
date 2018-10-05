from django.contrib import admin
from django.contrib.auth import admin as auth_admin
# Register your models here.
from .models import *


admin.site.register(Vehicle)
admin.site.register(Maintenance)

"""
	CREAR FILTROS DE BUSQUEDA
"""