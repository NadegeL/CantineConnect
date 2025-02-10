from django.contrib import admin
from .models import Student, Allergy, Parent


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'grade', 'get_allergies', 'get_parent')
    list_filter = ('grade', 'allergies', 'parent')
    search_fields = ['parent__user__first_name',
                     'parent__user__last_name', 'grade']

    def get_full_name(self, obj):
        return f"{obj.parent.user.first_name} {obj.parent.user.last_name}"
    get_full_name.short_description = 'Nom complet'

    def get_allergies(self, obj):
        return ", ".join([allergy.name for allergy in obj.allergies.all()])
    get_allergies.short_description = 'Allergies'

    def get_parent(self, obj):
        return obj.parent
    get_parent.short_description = 'Parent'


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ('name', 'severity')
    list_filter = ('severity',)
    search_fields = ['name']


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'phone_number', 'city')
    list_filter = ('city', 'is_admin')
    search_fields = ['user__first_name', 'user__last_name', 'email']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = "Nom complet"


"""
L'administration peut voir facilement la liste des étudiants avec leurs allergies
Elle peut filtrer les étudiants par allergie, classe ou parent
Elle peut rechercher un étudiant par son nom
Elle peut voir rapidement quel parent est associé à quel étudiant
"""
