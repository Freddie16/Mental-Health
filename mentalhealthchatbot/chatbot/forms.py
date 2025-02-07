from django import forms
from .models import Biodata

class BiodataForm(forms.ModelForm):
    class Meta:
        model = Biodata
        fields = ['age', 'relationship_status', 'problem_description']