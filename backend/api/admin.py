from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address, Parent, SchoolClass, Student, SchoolZone, Administration, Holidays, Allergy, StudentAllergy

# Définition de la classe CustomUserAdmin
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'user_type', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {
         'fields': ('first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    filter_horizontal = ('groups', 'user_permissions')


# Enregistrement du modèle User avec CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

# Enregistrement des autres modèles
admin.site.register(Address)
admin.site.register(Parent)
admin.site.register(SchoolClass)
admin.site.register(Student)
admin.site.register(SchoolZone)
admin.site.register(Administration)
admin.site.register(Holidays)
admin.site.register(Allergy)
admin.site.register(StudentAllergy)
