from decimal import Decimal

from django.db import transaction
from django.db.models import Prefetch
from django.utils import timezone

from traits.models import IdealTraitProfile, Trait

from .models import Answer, AssessmentSession, Question, TraitScore


def latest_completed_session(user):
    return (
        AssessmentSession.objects.filter(user=user, completed_at__isnull=False)
        .order_by('-completed_at')
        .first()
    )


def get_or_create_open_session(user):
    session = AssessmentSession.objects.filter(user=user, completed_at__isnull=True).order_by('-started_at').first()
    return session or AssessmentSession.objects.create(user=user)


def next_question(session):
    answered_ids = Answer.objects.filter(session=session).values_list('question_id', flat=True)
    return Question.objects.filter(is_active=True).exclude(id__in=answered_ids).order_by('display_order').first()


def record_answer(session, question, response):
    if session.is_complete:
        raise ValueError('This reflection round is already complete.')
    response = int(response)
    if response not in {-2, -1, 0, 1, 2}:
        raise ValueError('Assessment responses must use one of the provided choices.')
    return Answer.objects.update_or_create(
        session=session,
        question=question,
        defaults={'response': response},
    )[0]


def normalized_answer_value(answer):
    value = -answer.response if answer.question.reverse_scored else answer.response
    return Decimal(value + 2) / Decimal(4) * Decimal(100)


@transaction.atomic
def complete_session(session):
    answers = list(session.answers.select_related('question__trait'))
    if not answers:
        raise ValueError('Answer at least one question before completing the assessment.')

    TraitScore.objects.filter(session=session).delete()
    by_trait = {}
    for answer in answers:
        by_trait.setdefault(answer.question.trait, []).append(normalized_answer_value(answer))

    scores = []
    for trait, values in by_trait.items():
        score = sum(values) / Decimal(len(values))
        scores.append(
            TraitScore.objects.create(
                session=session,
                trait=trait,
                score=score.quantize(Decimal('0.01')),
                answer_count=len(values),
            )
        )

    if not session.completed_at:
        session.completed_at = timezone.now()
        session.save(update_fields=['completed_at'])

    return scores


def build_gap_report(user, session=None):
    traits = list(Trait.objects.active().order_by('display_order', 'name'))
    ideal = {
        item.trait_id: item.points
        for item in IdealTraitProfile.objects.filter(user=user).select_related('trait')
    }
    scores = {}
    if session:
        session = AssessmentSession.objects.prefetch_related(
            Prefetch('trait_scores', queryset=TraitScore.objects.select_related('trait'))
        ).get(pk=session.pk)
        scores = {item.trait_id: float(item.score) for item in session.trait_scores.all()}

    total_current = sum(scores.values()) or 0
    rows = []
    for trait in traits:
        score = scores.get(trait.id)
        current_share = (score / total_current * 100) if score is not None and total_current else 0
        ideal_points = ideal.get(trait.id, 0)
        gap = ideal_points - current_share
        rows.append(
            {
                'trait': trait,
                'ideal_points': ideal_points,
                'current_score': round(score, 1) if score is not None else None,
                'current_share': round(current_share, 1),
                'gap': round(gap, 1),
                'needs_attention': gap >= 5,
            }
        )
    return sorted(rows, key=lambda row: row['gap'], reverse=True)
