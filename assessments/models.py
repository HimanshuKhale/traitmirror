from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class AssessmentSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-started_at',)

    @property
    def is_complete(self):
        return self.completed_at is not None

    def complete(self):
        self.completed_at = timezone.now()
        self.save(update_fields=['completed_at'])

    def __str__(self):
        return f'{self.user} assessment {self.pk}'


class Question(models.Model):
    code = models.SlugField(max_length=60, unique=True)
    trait = models.ForeignKey('traits.Trait', on_delete=models.CASCADE)
    prompt = models.TextField()
    reverse_scored = models.BooleanField(default=False)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('display_order', 'code')

    def __str__(self):
        return self.prompt


class Answer(models.Model):
    RESPONSE_CHOICES = [
        (-2, 'Strongly unlike me'),
        (-1, 'Somewhat unlike me'),
        (0, 'Mixed or unsure'),
        (1, 'Somewhat like me'),
        (2, 'Strongly like me'),
    ]

    session = models.ForeignKey(AssessmentSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.SmallIntegerField(
        choices=RESPONSE_CHOICES,
        validators=[MinValueValidator(-2), MaxValueValidator(2)],
    )
    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session', 'question'], name='unique_answer_per_session_question')
        ]
        ordering = ('question__display_order',)

    def __str__(self):
        return f'{self.session}: {self.question.code}={self.response}'


class TraitScore(models.Model):
    session = models.ForeignKey(AssessmentSession, on_delete=models.CASCADE, related_name='trait_scores')
    trait = models.ForeignKey('traits.Trait', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    answer_count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['session', 'trait'], name='unique_score_per_session_trait')
        ]
        ordering = ('trait__display_order', 'trait__name')

    def __str__(self):
        return f'{self.session} {self.trait}: {self.score}'

# Create your models here.
