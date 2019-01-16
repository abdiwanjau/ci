from django.shortcuts import render,redirect

from django.contrib.auth.forms import UserCreationForm

from .forms import AddUserDetailsForm

# Create your views here.
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
            return redirect("login")
    else:
        user_form = UserCreationForm()
        email_form = AddUserDetailsForm()

    context = {
        "user_form":user_form,
        "email_form":email_form
    }
    
    return render(request,"registration/register.html",context)