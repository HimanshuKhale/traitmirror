from django.core.management.base import BaseCommand

from assessments.question_bank import ensure_question_bank


class Command(BaseCommand):
    help = 'Seed the Phase 1 static TraitMirror trait and question bank.'

    def handle(self, *args, **options):
        ensure_question_bank()
        self.stdout.write(self.style.SUCCESS('Seeded TraitMirror traits and questions.'))
