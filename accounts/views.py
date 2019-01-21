from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

from .forms import AddUserDetailsForm

# Create your views here.
def home(request):
    return render(request,"home.html")

def register(request):
    """
    This is the view I will use to register the users
    """
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        email_form = AddUserDetailsForm(request.POST)
        if user_form.is_valid() and email_form.is_valid():
            new_user = user_form.save(commit = False)
            cd = email_form.cleaned_data
            new_user.email = cd["email"]
            new_user.save()
            auth_login(request,new_user)
            return redirect('home')
    else:
        user_form = UserCreationForm()
        email_form = AddUserDetailsForm()

    context = {
        "user_form":user_form,
        "email_form":email_form
    }
    print hey
    return render(request,"registration/register.html",context)