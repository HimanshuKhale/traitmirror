from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TraitQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class Trait(models.Model):
    code = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=80)
    description = models.TextField()
    growth_prompt = models.CharField(max_length=255)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    objects = TraitQuerySet.as_manager()

    class Meta:
        ordering = ('display_order', 'name')

    def __str__(self):
        return self.name


class IdealTraitProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'trait'], name='unique_user_ideal_trait')
        ]
        ordering = ('trait__display_order', 'trait__name')

    def __str__(self):
        return f'{self.user} ideal {self.trait}: {self.points}'

# Create your models here.
