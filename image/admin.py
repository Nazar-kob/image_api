from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from image.models import Image, Tier, User

admin.site.register(Image)
admin.site.register(Tier)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("tier",)

    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("tier",)}),)
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional info", {"fields": ("tier",)}),)
    )
