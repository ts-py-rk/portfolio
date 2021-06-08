from django.contrib import admin
from . models import Operation
from . models import Active

# Register your models here.
admin.site.register(Operation)
admin.site.register(Active)
# admin.site.register(Active2)