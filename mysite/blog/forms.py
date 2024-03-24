from django import forms

class EmailPostForm(forms.Form):
    """
    Form for sending posts via email.
    """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)