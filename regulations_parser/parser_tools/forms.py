from django import forms
from parser_tools.models import Regulation, Incorporation, \
    StandardsOrganization

class ScrapeForm(forms.Form):
    url = forms.URLField(max_length=200, initial='')
    title = forms.CharField(max_length=200)

class RegulationForm(forms.ModelForm):
    class Meta:
        model = Regulation

class IncorporationForm(forms.ModelForm):
    class Meta:
        model = Incorporation
        exclude = ('page', 'context_start_position', 'context_end_position',)

class StandardsOrganizationForm(forms.ModelForm):
    class Meta:
        model = StandardsOrganization
