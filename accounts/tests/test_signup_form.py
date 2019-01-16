from django.test import TestCase

from django.contrib.auth.forms import UserCreationForm

from ..forms import AddUserDetailsForm

class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form1 = UserCreationForm()
        form2 = AddUserDetailsForm()

        expected = ["email","username","password1","password2"]
        
        actual = list(form1.fields)
        actual.insert(0,"email")

        self.assertSequenceEqual(expected,actual)