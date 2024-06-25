from django.shortcuts import render ,redirect
from django.views import View
from django.contrib import messages
from App_Models.models import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.

class DashboardView(View):
    template_name ='shop/index.html'
    def get(self,request):
        return render(request, self.template_name)
        
class SignUpView(View):
    template_name= 'demo.html'
    template_name1= 'shop/index.html'
    def get(self, request):
        try:
            return  render(request , self.template_name)
        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred while loading the page.')
            return redirect('signup')  
    
    def post(self, request):
        print("i am in")
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        # Validate password and confirm_password match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        # Check if the email already exists
        if CustomBaseUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
            return redirect('signup')

        try:
            # Create the user
            user = CustomBaseUser(
                name=name,
                email=email,
                address=address,
                mobile=mobile
            )
            user.set_password(password)
            user.save()

            messages.success(request, 'Account created successfully! You can now log in.')
            return  render(request , self.template_name1)
            
            
        except Exception as e:
            print("----",e)
            messages.error(request, 'An error occurred while creating your account.')
            return redirect('signup')
        
        
        
# if not request.user.is_authenticated or (request.user.user_type != "ADM" and (request.user.user_type != "SUB" or not request.user.permissions.laboratory_management_permission)):
#                     messages.error(request, 'You are not authorized to access this page.')
#                     return redirect('Login' if not request.user.is_authenticated else 'Admin:dashboard_Admin')
class LoginView(View):
    template_name = 'demo.html'
    
    def get(self, request):
        try:
            return render(request, self.template_name)
        except Exception as e:
            print(e)
            messages.error(request, 'An error occurred while loading the page.')
            return redirect('login')
    
    def post(self, request):
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                print("hello login")
                messages.success(request, 'Login successful!')
                return redirect('dashboard')  # Redirect to your dashboard or another page
            else:
                messages.error(request, 'Invalid email or password.')
                return render(request, self.template_name)
        except Exception as e:
            print("----", e)
            messages.error(request, 'An error occurred while logging in.')
            return redirect('login')
        
class UserDetailView(View):
    template_name='user_detail.html'
    
    
    def get(self, request, identifier):
        try:
            if identifier.isdigit():                
                user = get_object_or_404(CustomBaseUser, pk=identifier)
                
            else:
                user = get_object_or_404(CustomBaseUser, slug_field=identifier)
            return render(request, self.template_name, {'user': user})
        except Exception as e:
            print("error:",e)
            messages.error(request, 'An error occurred while loading the user details.')
            return redirect('dashboard')
