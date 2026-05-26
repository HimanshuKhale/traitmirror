from django import forms


class IdealProfileForm(forms.Form):
    def __init__(self, *args, traits=None, allocations=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.traits = list(traits or [])
        allocations = allocations or {}
        for trait in self.traits:
            self.fields[trait.code] = forms.IntegerField(
                label=trait.name,
                min_value=0,
                max_value=100,
                initial=allocations.get(trait.code, 0),
                widget=forms.NumberInput(
                    attrs={
                        'class': 'points-input',
                        'data-trait-points': 'true',
                        'inputmode': 'numeric',
                    }
                ),
            )

    def clean(self):
        cleaned = super().clean()
        total = sum(cleaned.get(trait.code) or 0 for trait in self.traits)
        if total != 100:
            raise forms.ValidationError('Your ideal self map must add up to exactly 100 points.')
        return cleaned
