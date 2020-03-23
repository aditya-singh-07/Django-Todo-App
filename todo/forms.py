from django.forms import ModelForm
from .models import Todo
from django import forms

class Todoform(forms.ModelForm):
    todotitle = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Todo title'
        }
    ))
    category = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Category'
        }
    ))
    notes = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Notes',

        }
    ))

    class Meta:
        model = Todo
        fields = ['todotitle', 'category', 'notes', 'important']

