
from django import forms


class SearchPartForm(forms.Form):
    query = forms.CharField(max_length=200)


class ChooseModelForm(forms.Form):
    pass 