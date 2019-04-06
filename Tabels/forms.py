from django import forms
from django.db import models
from Tabels.models import Post

class LevelForm(forms.Form):
    level = forms.DecimalField(label='Write level')
    def clean(self):
        super(LevelForm, self).clean()
        level = self.cleaned_data['level']
        if level <= 0:
            self._errors['level'] = self.error_class(['Must be positive integer'])
        return self.cleaned_data
