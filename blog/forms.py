from django.forms import ModelForm
from .models import Comment
from allauth.account.forms import SignupForm
from django import forms


class CommentCreateForm(ModelForm):
    """Форма для создания комментария"""

    class Meta:
        model = Comment
        fields = ['text',]


class SiteUserSignupForm(SignupForm):
    first_name = forms.CharField(
        label="First name",
        widget=forms.TextInput(
            attrs={"placeholder": "First name", "autocomplete": "first_name"}
        ),
    )
    last_name = forms.CharField(
        label="Last name",
        widget=forms.TextInput(
            attrs={"placeholder": "Last name", "autocomplete": "last_name"}
        ),
    )

    def save(self, request):
        user = super(SiteUserSignupForm, self).save(request)
        return user