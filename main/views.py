from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})
    
def category(request, var_name):
    var_name = var_name.replace('-', ' ')
    try:
        category = Category.objects.get(name=var_name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.info(request, ("That category doesn't exist."))
        return redirect('home')

def product(request, pk):
    single_product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'single_product': single_product})

def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been successfully logged in!'))
            return redirect('home')

        else:
            messages.error(request, ('Error logging in!'))
            return redirect('login')
    
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ('You have been successfully logged out!'))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have been successfully registered!'))
            return redirect('update_info')
        else:
            messages.error(request, ('Error registering!'))
            return redirect('register')

    else:
        return render(request, 'register.html', {'form': form})
    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, ('You have successfully changed your profile!'))
            return redirect('login')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.info(request, ('You need to be logged in first.'))
        return redirect('update_user')
    
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, ('You have successfully changed your info!'))
            return redirect('home')
        return render(request, 'update_info.html', {'form': form})
    else:
        messages.info(request, ('You need to be logged in first.'))
        return redirect('update_user')
    

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                login(request, current_user)
                messages.success(request, ('You have successfully changed your password!'))
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, f'{error}')
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.info(request, ('You need to be logged in first.'))
        return redirect('update_user')

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.info(request, ('That product does not exist.'))
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})
