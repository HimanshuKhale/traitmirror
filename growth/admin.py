from django.contrib import admin

from .models import GrowthPlan, PracticeEvent


@admin.register(GrowthPlan)
class GrowthPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'summary', 'session', 'created_at')
    search_fields = ('user__username', 'summary')


@admin.register(PracticeEvent)
class PracticeEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'trait', 'completed', 'created_at')
    list_filter = ('trait', 'completed')
    search_fields = ('user__username', 'note')

# Register your models here.
