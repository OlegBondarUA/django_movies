from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
        labels = {'name': '', 'email': '', 'subject': '', 'message': ''}
        required = ('name', 'email', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Name'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Your Subject'}),
            'message': forms.TextInput(
                attrs={
                    'placeholder': 'Your Name',
                    'maxlength': '1000'
                }
            )
        }