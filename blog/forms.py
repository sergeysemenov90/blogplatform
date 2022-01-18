from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import ModelForm
from .models import Comment, Post
from allauth.account.forms import SignupForm
from django import forms


class CommentCreateForm(ModelForm):
    """Форма для создания комментария"""

    class Meta:
        model = Comment
        fields = ['text',]


class SiteUserSignupForm(SignupForm):
    """Форма регистрации пользователя"""
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(
            attrs={"placeholder": "", "autocomplete": "first_name"}
        ), required=False
    )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(
            attrs={"placeholder": "", "autocomplete": "last_name"}
        ), required=False
    )

    description = forms.CharField(
        label="Коротко о себе",
        widget=forms.TextInput(
            attrs={"placeholder": "", "autocomplete": "description"}
        ), required=False
    )

    def save(self, request):
        user = super(SiteUserSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.description = self.cleaned_data['description']
        user.save()
        return user


class PostCreateForm(ModelForm):
    """Форма создания записи, добавление виджета CKEditor"""
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['title', 'content', 'blog', 'tags', 'image', 'source']
