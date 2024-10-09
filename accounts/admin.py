from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    ordering = ('last_login','username',)
    list_display = ("username", "email","last_login", "is_superuser", "credit",)


    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('credit',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)