from django.test import TestCase
from django.core import mail
from django.urls import reverse,resolve

from django.contrib.auth.models import User

class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="john",
            email="john@doe.com",
            password = "marvin123"
        )
        data = {
            "email":"john@doe.com"
        }
        self.response = self.client.post(reverse("password_reset"),data)
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEquals("Password reset on testserver",self.email.subject)

    def test_mail_body(self):
        context = self.response.context
        token = context.get("token")
        uid = context.get("uid")
        password_reset_token_url = reverse("password_reset_confirm",args = [uid,token])
        self.assertIn(password_reset_token_url,self.email.body)
    
    def test_email_to(self):
        self.assertEquals(['john@doe.com',], self.email.to)
