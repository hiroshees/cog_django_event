from django import forms
from django.forms import ModelForm

from .models import Category
from .models import Event
from .models import Chat


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name' : forms.TextInput(attrs={'autofocus' : True}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','number','category', 'user']
        widgets = {
            'name' : forms.TextInput(attrs={'autofocus' : True}),
        }


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['body',]
        widgets = {
            'body' : forms.Textarea(attrs={'autofocus' : True}),
        }

