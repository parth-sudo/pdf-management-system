from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import PDF, Comment
from ckeditor.fields import RichTextField

class CustomUserForm(UserCreationForm):
 class Meta:
  model = User
  fields = ['username', 'email', 'password1', 'password2']

class PDFForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ['title', 'file']

class SharePDFForm(forms.Form):
    users_shared_with = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )


class CommentForm(forms.ModelForm):
    class Meta:
       model = Comment
       fields = ['description']
