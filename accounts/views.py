from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignupForm, UserEditForm, ProfileEditForm
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Profile
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def user_login(request):
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(request, 
                                      username=data["username"],
                                      password=data["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Muvaffaqiyatli login amalga oshirildi")
                else:
                    return HttpResponse("Sizning profilingiz faol holatda emas ")
            else:
                return HttpResponse("Login va parolda xatolik bor")
    else:
        form=LoginForm()
        context={
            "form":form
            }
        return render(request, "account/login.html", context)
    
    
@login_required    
def dashboard(request):
    if request.user.is_authenticated: 
        user=request.user
        profile=Profile.objects.get(user=user)
        context={
            "user":user,
            "profile":profile
            }
        return render(request, "pages/user_profile.html", context)
    else:
        return redirect("login")


def signupView(request):
    if request.method=="POST":
        user_form=SignupForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data["password"]
                )
            new_user.save()
            Profile.objects.create(user=new_user)
        context={
            "new_user":new_user
            }
        return render(request, "account/signup_done.html", context)
    else:
        user_form=SignupForm()
        context={
            "user_form":user_form
            }
        return render(request, "account/signup.html", context)
    
    
class SignUpView(CreateView):
    form_class=UserCreationForm
    success_url=reverse_lazy("signup_done")
    template_name="account/signup.html"
    
    
@login_required 
def edit_user(request):
    if request.method=='POST':
        user_form=UserEditForm(instance=request.user, data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile,
                                     data=request.POST, 
                                     files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return redirect("user_profile")
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
        context={
            "user_form":user_form,
            "profile_form":profile_form
            }
    return render(request, "account/profile_edit.html", context)


class EditUserView(LoginRequiredMixin ,View):
    def get(self, request):
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
        context={
            "user_form":user_form,
            "profile_form":profile_form
            }
        return render(request, "account/profile_edit.html", context)
    
    def post(self, request):
        user_form=UserEditForm(instance=request.user, data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile,
                                     data=request.POST, 
                                     files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return redirect("user_profile")
        
    
    
    
    
    
    
    
    
    