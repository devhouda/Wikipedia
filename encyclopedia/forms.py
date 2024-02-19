from django import forms

class CreateNewEntry(forms.Form):
    title = forms.CharField(max_length=50)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":10}))

class EditEntry(forms.Form):
    content = content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":10}))