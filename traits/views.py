import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from assessments.question_bank import ensure_question_bank

from .forms import IdealProfileForm
from .models import Trait
from .services import get_allocations, save_allocations


@login_required
@require_http_methods(['GET', 'POST'])
def ideal_profile(request):
    ensure_question_bank()
    traits = Trait.objects.active()
    allocations = get_allocations(request.user)
    form = IdealProfileForm(
        request.POST or None,
        traits=traits,
        allocations=allocations,
    )

    if request.method == 'POST' and form.is_valid():
        save_allocations(request.user, {trait.code: form.cleaned_data[trait.code] for trait in traits})
        return redirect('dashboard')

    return render(request, 'traits/ideal_profile.html', {'form': form, 'traits': traits})


@login_required
@require_http_methods(['GET', 'POST'])
def ideal_profile_api(request):
    ensure_question_bank()
    traits = list(Trait.objects.active())

    if request.method == 'GET':
        allocations = get_allocations(request.user)
        return JsonResponse(
            {
                'traits': [
                    {
                        'code': trait.code,
                        'name': trait.name,
                        'description': trait.description,
                        'points': allocations.get(trait.code, 0),
                    }
                    for trait in traits
                ],
                'total_points': sum(allocations.get(trait.code, 0) for trait in traits),
            }
        )

    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
        raw_allocations = payload.get('allocations', payload)
        allocations = {code: int(points) for code, points in raw_allocations.items()}
        save_allocations(request.user, allocations)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        return JsonResponse({'error': str(exc)}, status=400)

    return JsonResponse({'status': 'saved'})

# Create your views here.
