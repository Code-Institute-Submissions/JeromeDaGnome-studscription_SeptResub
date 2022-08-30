from django import forms
from .models import Comment, Characters


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CharacterAddForm(forms.ModelForm):
    class Meta:
        model = Characters
        fields = ('name', 'bio', 'tag_lines', "image")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tag_lines': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CharacterEditForm(forms.ModelForm):
    class Meta:
        model = Characters
        fields = ('name', 'bio', 'tag_lines')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tag_lines': forms.Textarea(attrs={'class': 'form-control'}),
        }
