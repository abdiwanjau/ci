from django.test import TestCase
from django.urls import resolve,reverse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User,AnonymousUser

class LoginTest(TestCase):
    def setUp(self):
        url = reverse("login")
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertTrue(self.response.status_code,200)

    def test_func(self):
        view = resolve("/auth/login/")
        self.assertEquals(view.func.view_class,auth_views.LoginView)
    
    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form,AuthenticationForm)
    
    def test_csrf(self):
        self.assertContains(self.response,"csrfmiddlewaretoken")

    def test_form_fields(self):
        self.assertContains(self.response,"<input",4)
        self.assertContains(self.response,'type="text"',1)
        self.assertContains(self.response, 'type="password"', 1)
        self.assertContains(self.response, 'type="submit"', 1)
        self.assertContains(self.response, 'type="hidden"', 1)
    
class SuccessfulLogin(TestCase):
    def setUp(self):
        User.objects.create_user(username = "marvin_chomba",
                                email = "marvin@gmail.com",
                                password="marvin123"
        )
        data = {
            "username":"marvin_chomba",
            "password":"marvin123"
        }
        url = reverse("login")
        self.response = self.client.post(url,data)

        self.home = reverse("home")

    def test_redirect(self):
        self.assertRedirects(self.response,self.home)
    
    def test_user_auth(self):
        home_response = self.client.get(self.home)
        user = home_response.context.get("user")
        self.assertTrue(user.is_authenticated)


class InvalidLogin(TestCase):
    def setUp(self):
        url = reverse("login")
        self.response = self.client.post(url,{})

    def test_no_redirect(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_errors(self):
        form = self.response.context.get("form")
        self.assertTrue(form.errors)
    
    def test_user_not_authenticated(self):
        user = self.response.context.get("user")
        self.assertIsInstance(user,AnonymousUser)
