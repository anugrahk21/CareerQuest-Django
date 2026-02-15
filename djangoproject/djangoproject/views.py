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

#@login_required(login_url='login') # User can't access view page if not logged in
def view(request):
    data=CareerApp.objects.all() # Fetch all entries from the database
    return render(request,'view.html',{'data':data})

def login_view(request):
    # If user is already logged in, show them the entry page (or force logout)
    # User can't login if already logged in
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        # 1. Check if user exists in the database and password is correct.
        user=authenticate(request,username=username,password=password) # 'None' if user doesn't exist or password is incorrect and 'User' object if user exists and password is correct
        if user is not None: 
            # 2. Create a session for this user.
            # This sets a 'sessionid' cookie in the browser.
            # If this user is a superuser (is_staff=True), this cookie ALSO grants access to /admin/.
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Invalid credentials")
    return render(request,'login.html')

def logout_view(request):
    # User can't logout if not logged in
    if not request.user.is_authenticated:
        return redirect('login')
    logout(request)
    return redirect('home')

@login_required(login_url='login')
# views.update(request=<HttpRequest>, id='201')
# This is automatic! Django knows to pass id='201' because:
# The URL pattern has <str:id> (the variable name must match)
def update(request, id):
    data = CareerApp.objects.get(id=id) # Get the existing data from the database using the id passed in the URL. We will show this data in the update form as default values. User can change them and click on "Update" button to save the changes.
    if request.method == 'POST': # We go inside this block when user changes the data and clicks on "Update" button.
        #Until then, we are in GET method and we show the update form with existing data.
        # data.id = request.POST.get('id') # ID should not be updated as it is the primary key
        data.company = request.POST.get('company')
        data.role = request.POST.get('role')
        data.type = request.POST.get('type')
        data.package = request.POST.get('package')
        data.status = request.POST.get('status')
        data.date = request.POST.get('date')
        data.notes = request.POST.get('notes')
        data.save()
        return redirect('view')
    # If we are in GET method, we show the update form with existing data.
    return render(request, 'update.html', {'data': data}) # We pass the existing data to the update.html page so that we can show it in the form fields as default values. User can change them and click on "Update" button to save the changes.

@login_required(login_url='login')
# views.delete(request=<HttpRequest>, id='201')
# This is automatic! Django knows to pass id='201' because:
# The URL pattern has <str:id> (the variable name must match)
def delete(request, id):
    data = CareerApp.objects.get(id=id)
    data.delete() # Delete the entry from the database
    return redirect('view')