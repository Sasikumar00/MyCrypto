from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def signupView(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    repassword = request.POST.get('re-password')
    if password!=repassword:
        messages.error(request,"Passwords don't match", extra_tags='wrong_passwords')
        return redirect('/user/signup')
    checkUser = User.objects.filter(username=username).exists()
    print(checkUser)
    if(checkUser):
        messages.error(request,'Username already registered', extra_tags='alert')
        return redirect('/user/signin')
    else:
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    
def signUp_page(request):
    return render(request,'signupPage.html')

def signInView(request):
    logUsername = request.POST["username"]
    logPassword = request.POST["password"]
    user = authenticate(request, username=logUsername, password=logPassword)
    if user is not None:
        login(request, user)
        messages.success(request, 'Logged in successfully', extra_tags="alert")
        return redirect('/')
    else:
        messages.error(request, 'Invalid credentials. Please try again.', extra_tags="invalid_credencials")
        return redirect('/user/signin')

def signIn_page(request):
    return render(request, 'signinPage.html')

def logoutView(request):
    logout(request)
    messages.error(request,'Logged out', extra_tags='alert')
    return redirect('/')