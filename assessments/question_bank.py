from traits.models import Trait

from .models import Question


TRAITS = [
    {
        'code': 'clarity',
        'name': 'Clarity',
        'description': 'Noticing what matters, naming it plainly, and choosing with intention.',
        'growth_prompt': 'Name one decision you can make more clearly today.',
    },
    {
        'code': 'courage',
        'name': 'Courage',
        'description': 'Taking honest action when something important feels uncomfortable.',
        'growth_prompt': 'Take one small honest step you have been postponing.',
    },
    {
        'code': 'empathy',
        'name': 'Empathy',
        'description': "Making room for another person's perspective while staying grounded in your own.",
        'growth_prompt': 'Ask one sincere question before offering your view.',
    },
    {
        'code': 'discipline',
        'name': 'Discipline',
        'description': 'Following through on chosen commitments in small, repeatable ways.',
        'growth_prompt': 'Choose one commitment and make it easier to complete today.',
    },
    {
        'code': 'openness',
        'name': 'Openness',
        'description': 'Being willing to update your view when new information appears.',
        'growth_prompt': 'Write down one belief you are willing to examine gently.',
    },
]

QUESTIONS = [
    ('clarity_1', 'clarity', 'When plans change, I can usually name what matters most before reacting.', False),
    ('clarity_2', 'clarity', 'I often postpone choices because I have not sorted my priorities yet.', True),
    ('clarity_3', 'clarity', 'I can explain my reasons for a meaningful decision without overcomplicating them.', False),
    ('courage_1', 'courage', 'I can say a respectful no when yes would go against my values.', False),
    ('courage_2', 'courage', 'I avoid useful conversations when they might feel awkward.', True),
    ('courage_3', 'courage', 'I take small action even when I am not fully confident yet.', False),
    ('empathy_1', 'empathy', 'In disagreement, I try to understand what the other person is protecting or hoping for.', False),
    ('empathy_2', 'empathy', 'I sometimes prepare my reply before I have really heard the other person.', True),
    ('empathy_3', 'empathy', 'I can acknowledge someone else experience without abandoning my own view.', False),
    ('discipline_1', 'discipline', 'I keep small promises to myself even when the day gets noisy.', False),
    ('discipline_2', 'discipline', 'My follow-through depends heavily on whether I feel motivated in the moment.', True),
    ('discipline_3', 'discipline', 'I recover from missed routines without turning the whole day into a loss.', False),
    ('openness_1', 'openness', 'I can update my opinion without feeling like I have failed.', False),
    ('openness_2', 'openness', 'I tend to defend my first interpretation when new details appear.', True),
    ('openness_3', 'openness', 'I can be curious about feedback before deciding what to do with it.', False),
]


def ensure_question_bank():
    trait_by_code = {}
    for index, trait_data in enumerate(TRAITS, start=1):
        trait, _created = Trait.objects.update_or_create(
            code=trait_data['code'],
            defaults={
                'name': trait_data['name'],
                'description': trait_data['description'],
                'growth_prompt': trait_data['growth_prompt'],
                'display_order': index,
                'is_active': True,
            },
        )
        trait_by_code[trait.code] = trait

    for index, (code, trait_code, prompt, reverse_scored) in enumerate(QUESTIONS, start=1):
        Question.objects.update_or_create(
            code=code,
            defaults={
                'trait': trait_by_code[trait_code],
                'prompt': prompt,
                'reverse_scored': reverse_scored,
                'display_order': index,
                'is_active': True,
            },
        )
