from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm

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
        messages.success(request, ("That category doesn't exist."))
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
            messages.success(request, ('Error logging in!'))
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
            return redirect('home')
        else:
            messages.success(request, ('Error registering!'))
            return redirect('register')

    else:
        return render(request, 'register.html', {'form': form})