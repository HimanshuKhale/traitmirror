import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from growth.recommendations import create_plan_from_session

from .models import Answer, AssessmentSession, Question
from .question_bank import ensure_question_bank
from .services import complete_session, get_or_create_open_session, next_question, record_answer


@login_required
@require_http_methods(['GET', 'POST'])
def assessment(request):
    ensure_question_bank()
    session = get_or_create_open_session(request.user)
    question = next_question(session)

    if request.method == 'POST':
        question = get_object_or_404(Question, pk=request.POST.get('question_id'), is_active=True)
        record_answer(session, question, request.POST.get('response'))
        next_item = next_question(session)
        if not next_item:
            complete_session(session)
            create_plan_from_session(request.user, session)
            return redirect('dashboard')
        return redirect('assessment')

    total_questions = Question.objects.filter(is_active=True).count()
    answered_count = Answer.objects.filter(session=session).count()
    return render(
        request,
        'assessments/assessment.html',
        {
            'session': session,
            'question': question,
            'total_questions': total_questions,
            'answered_count': answered_count,
            'choices': Answer.RESPONSE_CHOICES,
        },
    )


@login_required
@require_GET
def next_question_api(request):
    ensure_question_bank()
    session_id = request.GET.get('session_id')
    if session_id:
        session = get_object_or_404(AssessmentSession, pk=session_id, user=request.user)
    else:
        session = get_or_create_open_session(request.user)

    question = next_question(session)
    if not question:
        return JsonResponse({'session_id': session.id, 'complete': True})

    return JsonResponse(
        {
            'session_id': session.id,
            'complete': False,
            'question': {
                'code': question.code,
                'prompt': question.prompt,
                'trait': question.trait.code,
            },
            'choices': [{'value': value, 'label': label} for value, label in Answer.RESPONSE_CHOICES],
        }
    )


@login_required
@require_POST
def answer_api(request):
    ensure_question_bank()
    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
        session = get_object_or_404(AssessmentSession, pk=payload.get('session_id'), user=request.user)
        question = get_object_or_404(Question, code=payload.get('question_code'), is_active=True)
        record_answer(session, question, int(payload.get('response')))
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        return JsonResponse({'error': str(exc)}, status=400)

    return JsonResponse({'status': 'saved', 'session_id': session.id})


@login_required
@require_POST
def complete_api(request):
    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
        session = get_object_or_404(AssessmentSession, pk=payload.get('session_id'), user=request.user)
        scores = complete_session(session)
        create_plan_from_session(request.user, session)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        return JsonResponse({'error': str(exc)}, status=400)

    return JsonResponse(
        {
            'status': 'complete',
            'scores': [
                {'trait': score.trait.code, 'score': float(score.score), 'answer_count': score.answer_count}
                for score in scores
            ],
        }
    )

# Create your views here.
