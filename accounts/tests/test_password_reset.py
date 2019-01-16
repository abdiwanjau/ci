from django.test import TestCase
from django.urls import reverse,resolve
from django.core import mail

from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse("password_reset")
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_view_function(self):
        view = resolve("/auth/password/reset/")
        self.assertEquals(view.func.view_class,auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response,"csrfmiddlewaretoken")
    
    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form,PasswordResetForm)

    def test_form_inputs(self):
        """
        Contains three inputs:csrf,email and submit
        """
        self.assertContains(self.response,"<input",3)
        self.assertContains(self.response,'type="hidden"',1)
        self.assertContains(self.response,'type="email"',1)
        self.assertContains(self.response,'type="submit"',1)

class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        data = {
            "email":"haha@gmail.com"
        }
        User.objects.create_user(username='hey',email="haha@gmail.com",password="marvin123")
        url = reverse("password_reset")
        self.response = self.client.post(url,data)

    def test_redirection(self):
        url = reverse("password_reset_done")
        self.assertRedirects(self.response,url)

    def test_send_password_reset_email(self):
        self.assertEqual(1,len(mail.outbox))
    

class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse("password_reset")
        self.response = self.client.post(url,{"email":"heythere@gmail.com"})

    def test_redirection(self):
        url = reverse("password_reset_done")
        self.assertRedirects(self.response,url)

    def test_no_email_sent(self):
        self.assertEqual(0,len(mail.outbox))

class PasswordResetDone(TestCase):
    def setUp(self):
        url = reverse("password_reset_done")
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertTrue(self.response.status_code == 200)

    def test_view_func(self):
        view = resolve("/auth/password/reset/done/")
        self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)

    def test_contains_redirect_link(self):
        self.assertContains(self.response,"Check your email")

class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username = "john",email = "john@gmail.com",password = "marvin123")

        """
        create a valid password reset token
        """

        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        self.token = default_token_generator.make_token(user)

        url = reverse("password_reset_confirm",args = [self.uid,self.token])

        self.response = self.client.get(url,follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_view_func(self):
        view = resolve("/auth/reset/{}/{}/".format(self.uid,self.token))
        self.assertEquals(view.func.view_class,auth_views.PasswordResetConfirmView)

    def test_csrf(self):
        self.assertContains(self.response,"csrfmiddlewaretoken")

    
    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form,SetPasswordForm)
    
    def test_form_inputs(self):
        self.assertContains(self.response,"<input",4)
        self.assertContains(self.response,'type="hidden"',1)
        self.assertContains(self.response,'type="password"',2)
        self.assertContains(self.response,'type="submit"',1)
    

class InvalidPassReset(TestCase):
    def setUp(self):
        user = User.objects.create(
            username = "john",
            email = "john@gmail.com",
            password = "marvin123"
        )

        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        self.token = default_token_generator.make_token(user)

        user.set_password("marvin1234")
        user.save()

        url = reverse("password_reset_confirm",args = [self.uid,self.token])

        self.response = self.client.get(url)
    
    def test_status(self):
        self.assertEqual(self.response.status_code,200)

    def test_html(self):
        self.assertContains(self.response,'Invalid link')

    