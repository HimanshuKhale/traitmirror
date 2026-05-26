from django.contrib.auth.models import User
from django.test import TestCase

from growth.recommendations import create_plan_from_session
from traits.models import Trait
from traits.services import save_allocations

from .models import Question, TraitScore
from .question_bank import ensure_question_bank
from .services import build_gap_report, complete_session, get_or_create_open_session, record_answer


class PhaseOneFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reader', password='test-pass-123')
        ensure_question_bank()

    def test_question_bank_seeds_traits_and_questions(self):
        self.assertEqual(Trait.objects.count(), 5)
        self.assertEqual(Question.objects.count(), 15)

    def test_ideal_profile_requires_exactly_100_points(self):
        allocations = {trait.code: 10 for trait in Trait.objects.all()}

        with self.assertRaises(ValueError):
            save_allocations(self.user, allocations)

    def test_scoring_gap_report_and_growth_plan_use_reflection_language(self):
        allocations = {
            'clarity': 40,
            'courage': 25,
            'empathy': 15,
            'discipline': 10,
            'openness': 10,
        }
        save_allocations(self.user, allocations)
        session = get_or_create_open_session(self.user)

        for question in Question.objects.all():
            response = -1 if question.trait.code == 'clarity' else 1
            record_answer(session, question, response)

        scores = complete_session(session)
        self.assertEqual(len(scores), 5)
        self.assertEqual(TraitScore.objects.filter(session=session).count(), 5)

        gaps = build_gap_report(self.user, session=session)
        self.assertEqual(gaps[0]['trait'].code, 'clarity')
        self.assertGreater(gaps[0]['gap'], 0)

        plan = create_plan_from_session(self.user, session)
        rendered = f'{plan.summary} {plan.recommendations}'
        self.assertIn('Clarity', rendered)
        self.assertNotIn('diagnosis', rendered.lower())
        self.assertNotIn('lying', rendered.lower())

# Create your tests here.
