from django.shortcuts import render ,redirect
from django.http import HttpResponse

from .models import *
from .forms import CreateUserForm
from django.contrib import messages

from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import admin_only, unauthenticated_user , allowed_users
# Create your views here.


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def indexPage(request):
    context={}
    return render(request,'index.html',context)

@admin_only
def adminPage(request):
    context={}
    return render(request,'admin.html',context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request,'Username OR Password is incorrect')
    context={}
    return render(request,'login.html',context)

@unauthenticated_user
def registerPage(request):

    form=CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(request)
        if form.is_valid():
            user = form.save()
            
            username=form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request,'Account was created for '+username)
            return redirect('login')
    
    context={'form':form}
    return render(request,'register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')
