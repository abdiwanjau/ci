from django.test import TestCase
from django.urls import resolve,reverse

from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm as formy

class PasswordChangeForm(TestCase):
    def setUp(self):
        User.objects.create_user(username= 'marvin',email='marvin@marvin.com',password="marvin123")
        url = reverse("password_change")
        self.client.login(username = "marvin",password  = "marvin123")
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_resolves_view_func(self):
        view = resolve("/auth/password/change/")
        self.assertEquals(view.func.view_class,auth_views.PasswordChangeView)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, formy)

    def test_csrf(self):
        self.assertContains(self.response,"csrfmiddlewaretoken")
    
    def test_form_fields(self):
        self.assertContains(self.response,"<input",5)
        self.assertContains(self.response,'type="password"',3)
        self.assertContains(self.response, 'type="hidden"', 1)
        self.assertContains(self.response, 'type="submit"', 1)

class PasswordLoginRequired(TestCase):
    def setUp(self):
        url = reverse("password_change")
        self.response = self.client.get(url)

    def test_redirect(self):
        redirect_url = "{}?next={}".format(reverse("login"),reverse("password_change"))
        self.assertRedirects(self.response,redirect_url)
    
class SuccessfulPasswordChange(TestCase):
    def setUp(self):
        User.objects.create_user(username = "marvin",password="old_password",email="mer@gmail.com")
        self.client.login(username = "marvin",password = "old_password")
        data = {
            "old_password":"old_password",
            "new_password1":"new_password",
            "new_password2":"new_password"
        }
        url = reverse("password_change")
        self.response = self.client.post(url,data)

    def test_redirects(self):
        to_url = reverse("password_change_done")
        self.assertRedirects(self.response,to_url)


    def test_password_did_change(self):
        user = User.objects.first()
        self.assertTrue(user.check_password("new_password"))

class InvalidPasswordChange(TestCase):
    def setUp(self):
        User.objects.create_user(
                    username="marvin", password="old_password", email="mer@gmail.com")
        self.client.login(username = "marvin",password = "old_password")
        data = {
            "old_password":"old_password",
            "new_password1":"new_passwor",
            "new_password2":"new_password"
        }
        url = reverse("password_change")
        self.response = self.client.post(url,data)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)
    
    def test_errors(self):
        form = self.response.context.get("form")
        self.assertTrue(form.errors)
    
    def password_no_change(self):
        self.assertTrue(User.objects.first().check_password("old_password"))

class PasswordChangeDone(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="marvin", password="old_password", email="mer@gmail.com")
        self.client.login(username="marvin", password="old_password")
        url = reverse("password_change_done")
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertTrue(self.response.status_code == 200)

    def test_html(self):
        self.assertContains(
            self.response, "Password Change Successful. You can login")
    def test_link(self):
        self.assertContains(self.response,'href="{}"'.format(reverse("login")))
    

