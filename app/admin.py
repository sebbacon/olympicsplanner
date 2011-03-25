from django.contrib import admin
import models

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'last_login')
    list_filter = ('is_active',)
    search_fields = ('first_name', 'last_name', 'email')

admin.site.register(models.CustomUser, UserAdmin)
