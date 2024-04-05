from django.shortcuts import redirect, render
from django.contrib.auth import login
from authentication.forms import SignUpForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(SuccessMessageMixin, LoginView):
    success_message = "connexion réussie"
    redirect_authenticated_user = True
    template_name = "authentication/index.html"


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    success_message = "déconnexion réussie"


# Create your views here.
def index(request):
    return render(request, "authentication/index.html")


def signupPage(request):
    context = {"form": SignUpForm}
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            messages.success(request, f"Compte crée pour {user.username}")
            return redirect("home")
        else:

            message = str(form.errors).split("<li>")[2].split(".")[0]

            context.update({"errors": message})
            return render(request, "authentication/signup.html", context)
    return render(request, "authentication/signup.html", context)
