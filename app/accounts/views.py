from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import User, Profile
import uuid

# Create your views here.
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # validating user credentials
        existingAccount = authenticate(request, email=email, password=password)
        if existingAccount and existingAccount.role == 'Customer':
            auth_login(request, existingAccount)
            return redirect('customers:dashboard')
        
        elif existingAccount and existingAccount.role == 'Owner':
            auth_login(request, existingAccount)
            return redirect(reverse("agents:agents_dashboard")+f"?id={existingAccount.id}")

        elif  existingAccount and existingAccount.role == "admin":
            auth_login(request, existingAccount)
            return redirect("Admin:admin_dashboard")

        else:
            messages.info(request,"Account does'nt exist. create new account")
            return redirect("accounts:login")

    return render(request, 'accounts/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone-number')
        account_type = request.POST.get('user_role')

        # creating a new user account
        # Validating the email domain name
        Accepted_domain = {'gmail.com', 'yahoo.com'}
        domain = email.split("@")[-1].strip().lower()

        try:
            if domain in Accepted_domain:
                verified_email = email
            else:
                messages.error(request, f"{domain} is not allowed")
                return redirect('register')
        except IndexError:
            messages.error(request, "Email invalid")
            return redirect('register')

        if User.objects.filter(phone_number=phone_number):
            messages.warning(request, "Account already exists. Please login to continue.")
            return redirect("accounts:login")

        
        else:
          New_UserAccount = User.objects.create_user(
                name = username,
                email = verified_email,
                password = password,
                phone_number = phone_number,
                gender = gender,
                role = account_type
            )

      
          if account_type == "Owner":
            Profile(userId = New_UserAccount).save()
            messages.success(request, "Account successfully created. login account now")
            return redirect("accounts:login")

        messages.success(request, "Account successfully created. login account now")
        return redirect("accounts:login")
        
    return render(request, 'accounts/register.html')

def logout(request):
    auth_logout(request)
    messages.success(request, "logout account successfully")
    return redirect('accounts:login')
