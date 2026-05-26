from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    display_name = forms.CharField(max_length=120, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'display_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
            user.profile.display_name = self.cleaned_data.get('display_name') or user.username
            user.profile.save(update_fields=['display_name'])
        return user
