from django.test import TestCase
from django.urls import resolve,reverse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from ..views import register
from ..forms import AddUserDetailsForm


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse("register")
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_signup_url_resolves_signup_view(self):
        views = resolve("/auth/register/")
        self.assertEquals(views.func,register)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")
    
    def test_contains_main_form(self):
        form = self.response.context.get('user_form')
        self.assertIsInstance(form,UserCreationForm)

    def test_contains_email_form(self):
        form = self.response.context.get("email_form")
        self.assertIsInstance(form, AddUserDetailsForm)
    
    def test_form_inputs(self):
        """
        This view must contain 6 inputs:csrf,email,username,password,password2,button
        """
        self.assertContains(self.response,"<input",6)
        self.assertContains(self.response,'type="text"',1)
        self.assertContains(self.response,'type="email"',1)
        self.assertContains(self.response,'type="password"',2)
        self.assertContains(self.response,'type="submit"',1)

    
class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse("register")
        data = {
            "username":"john",
            "email":"john@gmail.com",
            "password1":"marvin123",
            "password2":"marvin123"
        }
        self.response = self.client.post(url,data)
        self.redirect_url = reverse("home")

    def test_redirection(self):
        """
        Should redirect to login
        """
        self.assertRedirects(self.response,self.redirect_url)
    
    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        """
        Create a new request ot an arbitrary page
        The resulting response should now have a user to its context
        """
        response = self.client.get(self.redirect_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSignUpTest(TestCase):
    def setUp(self):
        url = reverse("register")
        self.response = self.client.post(url,{})

    def test_signup_status(self):
        """
        Invalid submission should return to the same page
        """
        self.assertEquals(self.response.status_code,200)

    def test_form_errors(self):
        form1 = self.response.context.get("user_form")
        form2 = self.response.context.get("email_form")
        self.assertTrue(form1.errors)
        self.assertTrue(form2.errors)
    
    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
    