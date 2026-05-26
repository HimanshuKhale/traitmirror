from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from assessments.question_bank import ensure_question_bank
from assessments.services import build_gap_report, latest_completed_session
from growth.recommendations import get_or_create_daily_plan
from traits.models import Trait


@login_required
def dashboard(request):
    ensure_question_bank()
    traits = Trait.objects.active().order_by('display_order', 'name')
    session = latest_completed_session(request.user)
    gap_rows = build_gap_report(request.user, session=session)
    plan = get_or_create_daily_plan(request.user, session=session) if session else None

    return render(
        request,
        'dashboard/index.html',
        {
            'traits': traits,
            'latest_session': session,
            'gap_rows': gap_rows,
            'growth_plan': plan,
            'has_ideal_profile': any(row['ideal_points'] for row in gap_rows),
            'has_scores': bool(session),
        },
    )
