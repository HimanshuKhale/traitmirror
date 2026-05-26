from assessments.services import build_gap_report
from .models import GrowthPlan


def recommendation_for(row):
    trait = row['trait']
    if row['needs_attention']:
        focus = 'A useful next step is to practice this in a small, observable way.'
    else:
        focus = 'Keep this trait in view and notice where it already shows up.'
    return {
        'trait': trait.code,
        'trait_name': trait.name,
        'gap': row['gap'],
        'message': f'{trait.growth_prompt} {focus}',
    }


def build_recommendations(user, session=None, limit=3):
    rows = build_gap_report(user, session=session)
    focus_rows = [row for row in rows if row['ideal_points'] > 0][:limit]
    return [recommendation_for(row) for row in focus_rows]


def create_plan_from_session(user, session):
    recommendations = build_recommendations(user, session=session)
    if recommendations:
        names = ', '.join(item['trait_name'] for item in recommendations[:2])
        summary = f'Today focus gently on {names}.'
    else:
        summary = 'Build your ideal self map to receive focused growth prompts.'

    return GrowthPlan.objects.create(
        user=user,
        session=session,
        summary=summary,
        recommendations=recommendations,
    )


def get_or_create_daily_plan(user, session=None):
    if session:
        plan = GrowthPlan.objects.filter(user=user, session=session).first()
        if plan:
            return plan
        return create_plan_from_session(user, session)
    return GrowthPlan.objects.filter(user=user).first()
