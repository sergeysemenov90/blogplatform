from django.forms import ModelForm
from .models import Comment


class CommentCreateForm(ModelForm):
    """Форма для создания комментария"""

    class Meta:
        model = Comment
        fields = ['text',]