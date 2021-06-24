from django.contrib import admin
from .forms import UserChangeForm , UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name','last_name','is_shopadmin', 'is_admin','email_confirmed')
    list_filter = ('is_admin','is_shopadmin')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations', {'fields': ('first_name','last_name','phone','ostan','address','email_confirmed')}),

        ('Permissions', {'fields': ('is_admin','is_active','is_shopadmin')}),
    )

    add_fieldsets = (
		(None, {
			'fields':('first_name','last_name', 'email', 'password1', 'password2')
		}),
	)

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()




admin.site.register(User, UserAdmin)
admin.site.unregister(Group)