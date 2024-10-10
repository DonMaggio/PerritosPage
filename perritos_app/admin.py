from django.contrib import admin
from .models import Perro, PerroFotos

# Register your models here.
#admin.site.register(Perro)

class PerroFotoInline(admin.TabularInline):
    model = PerroFotos
    extra = 1

@admin.register(Perro)
class PerroAdmin(admin.ModelAdmin):
    inlines = [PerroFotoInline]