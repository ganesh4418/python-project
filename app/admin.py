from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RequestDemo, ContactUs, HelpandSupport

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(RequestDemo)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = ('Full_name', 'Company', 'Business_email', 'Contact_number')


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('Full_name', 'Company', 'Business_email', 'Contact_number')


@admin.register(HelpandSupport)
class HelpandSupportAdmin(admin.ModelAdmin):
    list_display = ('Full_name', 'Company', 'Business_email', 'Contact_number')