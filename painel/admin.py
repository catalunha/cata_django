from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

from painel.models import User,Variavel

admin.site.site_header = "CAT@"
admin.site.site_title = "CAT@"
#admin.site.register(admin.models.LogEntry)

ADDITIONAL_USER_FIELDS = (
    ("Informações personalizadas", {'fields': ('cargo','professor')}),
)

class CustomUserAdmin(UserAdmin):
    model = User
    add_fieldsets = UserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS

    #list_display = ('id', 'username', 'last_name', 'cargo')
    list_display = ('id', 'username', 'last_name', 'last_name', 'email','cargo','is_active')
admin.site.register(User, CustomUserAdmin)
#admin.site.register(User)



class VariavelAdmin(admin.ModelAdmin):
    list_display=('usuario','nome','valor','texto','arquivo',)
    fields=('usuario','nome','valor','texto','arquivo',)
admin.site.register(Variavel,VariavelAdmin)
