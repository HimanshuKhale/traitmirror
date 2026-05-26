from django.contrib import admin

from .models import Answer, AssessmentSession, Question, TraitScore


@admin.register(AssessmentSession)
class AssessmentSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'started_at', 'completed_at')
    list_filter = ('completed_at',)
    search_fields = ('user__username',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('code', 'trait', 'display_order', 'reverse_scored', 'is_active')
    list_filter = ('trait', 'is_active', 'reverse_scored')
    search_fields = ('code', 'prompt')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('session', 'question', 'response', 'answered_at')
    list_filter = ('question__trait',)


@admin.register(TraitScore)
class TraitScoreAdmin(admin.ModelAdmin):
    list_display = ('session', 'trait', 'score', 'answer_count')
    list_filter = ('trait',)

# Register your models here.
