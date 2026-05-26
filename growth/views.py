import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from assessments.services import latest_completed_session
from traits.models import Trait

from .models import PracticeEvent
from .recommendations import get_or_create_daily_plan


@login_required
@require_GET
def daily_plan(request):
    session = latest_completed_session(request.user)
    plan = get_or_create_daily_plan(request.user, session=session) if session else None
    return render(request, 'growth/daily_plan.html', {'growth_plan': plan})


@login_required
@require_POST
def practice_event(request):
    trait = get_object_or_404(Trait, code=request.POST.get('trait'))
    PracticeEvent.objects.create(user=request.user, trait=trait, note=request.POST.get('note', ''))
    return redirect('daily_plan')


@login_required
@require_GET
def daily_plan_api(request):
    session = latest_completed_session(request.user)
    plan = get_or_create_daily_plan(request.user, session=session) if session else None
    if not plan:
        return JsonResponse({'summary': 'Complete an assessment to receive a daily growth plan.', 'recommendations': []})
    return JsonResponse({'summary': plan.summary, 'recommendations': plan.recommendations})


@login_required
@require_POST
def practice_event_api(request):
    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
        trait = get_object_or_404(Trait, code=payload.get('trait'))
        event = PracticeEvent.objects.create(
            user=request.user,
            trait=trait,
            note=payload.get('note', ''),
            completed=bool(payload.get('completed', True)),
        )
    except json.JSONDecodeError as exc:
        return JsonResponse({'error': str(exc)}, status=400)

    return JsonResponse({'status': 'saved', 'id': event.id})

# Create your views here.
