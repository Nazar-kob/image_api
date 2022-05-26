from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app_image.models import Tier, User, ThumbnailSize

admin.site.register(ThumbnailSize)


@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    filter_horizontal = ('thumbnail_sizes',)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "tier")

    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("tier",)}),)
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional info", {"fields": ("tier",)}),)
    )
