from django.contrib import admin

from .models import IdealTraitProfile, Trait


@admin.register(Trait)
class TraitAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')


@admin.register(IdealTraitProfile)
class IdealTraitProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'trait', 'points', 'updated_at')
    list_filter = ('trait',)
    search_fields = ('user__username', 'trait__name')

# Register your models here.
