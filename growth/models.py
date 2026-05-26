from django.conf import settings
from django.db import models


class GrowthPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(
        'assessments.AssessmentSession',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    summary = models.CharField(max_length=255)
    recommendations = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.summary


class PracticeEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trait = models.ForeignKey('traits.Trait', on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    completed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user} practice for {self.trait}'

# Create your models here.
