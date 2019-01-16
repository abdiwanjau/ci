from django import forms

from django.contrib.auth.models import User


class AddUserDetailsForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        if User.objects.filter(email = self.cleaned_data["email"]):
            raise forms.ValidationError("There is a user with that email")
        else:
            return self.cleaned_data["email"]