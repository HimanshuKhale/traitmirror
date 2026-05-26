from django.db import transaction

from .models import IdealTraitProfile, Trait


def get_allocations(user):
    return {
        profile.trait.code: profile.points
        for profile in IdealTraitProfile.objects.filter(user=user).select_related('trait')
    }


def save_allocations(user, allocations):
    traits = list(Trait.objects.active())
    valid_codes = {trait.code for trait in traits}
    unknown = sorted(set(allocations) - valid_codes)
    if unknown:
        raise ValueError(f'Unknown trait code: {", ".join(unknown)}')

    normalized = {}
    for trait in traits:
        points = int(allocations.get(trait.code, 0))
        if points < 0 or points > 100:
            raise ValueError('Each ideal trait allocation must be between 0 and 100 points.')
        normalized[trait.code] = points

    total = sum(normalized.values())
    if total != 100:
        raise ValueError('Ideal trait points must add up to exactly 100.')

    with transaction.atomic():
        for trait in traits:
            IdealTraitProfile.objects.update_or_create(
                user=user,
                trait=trait,
                defaults={'points': normalized[trait.code]},
            )
