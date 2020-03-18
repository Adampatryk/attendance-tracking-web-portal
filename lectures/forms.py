from django import forms
from . import models

class DateTimeInput(forms.DateTimeInput):
    input_type = 'date'

class CreateLecture(forms.ModelForm):
    datetime = forms.DateTimeField(widget=DateTimeInput)
    class Meta:
        model = models.Lecture
        fields = ['classId', 'title', 'datetime']