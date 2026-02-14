from django.shortcuts import render,redirect
from app.models import CareerApp
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

@login_required(login_url='login') # User can't access entry page if not logged in
# If not logged in, redirect to login page->login_url='login'
# Any one on internet can add entries even if not logged in if we remove @login_required(login_url='login')
def entry(request):
    if request.method=='POST':
        id=request.POST.get('id')
        company=request.POST.get('company')
        role=request.POST.get('role')
        type=request.POST.get('type')
        package=request.POST.get('package')
        status=request.POST.get('status')
        date=request.POST.get('date') # YYYY-MM-DD
        notes=request.POST.get('notes')

        data=CareerApp(id=id,company=company,role=role,type=type,package=package,status=status,date=date,notes=notes)
        data.save()
        return redirect('entry')

    return render(request,'entry.html')

def home(request):
    return render(request,'index.html')

@login_required(login_url='login') # User can't access view page if not logged in
def view(request):
    data=CareerApp.objects.all()
    return render(request,'view.html',{'data':data})

def login_view(request):
    # If user is already logged in, show them the entry page (or force logout)
    # User can't login if already logged in
    if request.user.is_authenticated:
        return redirect('entry')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        # 1. Check if user exists in the database and password is correct.
        user=authenticate(request,username=username,password=password)
        if user is not None:
            # 2. Create a session for this user.
            # This sets a 'sessionid' cookie in the browser.
            # If this user is a superuser (is_staff=True), this cookie ALSO grants access to /admin/.
            login(request,user)
            return redirect('entry')
        else:
            return HttpResponse("Invalid credentials")
    return render(request,'login.html')

def logout_view(request):
    # User can't logout if not logged in
    if not request.user.is_authenticated:
        return redirect('login')
    logout(request)
    return redirect('home')