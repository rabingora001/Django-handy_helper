from django.shortcuts import render, redirect, HttpResponse
from .models import User,Job
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, "exam/index.html")

def registration_process(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")

    else:
        hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create( first_name=request.POST['first_name'], 
                                        last_name=request.POST['last_name'], 
                                        email=request.POST['email'], 
                                        password=hash_password.decode())
        request.session["user_id"] = new_user.id
        request.session["f_name"] = new_user.first_name
        request.session["l_name"] = new_user.last_name
        return redirect("/dashboard")

def login_process(request):
    # if request.method=='post'

    errors =User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        logged_in_user = User.objects.get(email=request.POST["login_email"])
        request.session["user_id"] = logged_in_user.id
        request.session["f_name"] = logged_in_user.first_name
        request.session["l_name"] = logged_in_user.last_name
        return redirect('/dashboard')
    
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    context = {
        'logInInfo' : User.objects.get(id = request.session['user_id']),
        'job_list' : Job.objects.all().order_by('-created_at')
    }
    return render(request, 'exam/dashboard.html', context)

def addJob(request):
    # if 'user_id' not in request.session:
    #     return redirect('/')

    return render(request, 'exam/addJob.html')

def add_job(request):
    errors =Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addJob')
    else:
        created_by= User.objects.get(id = request.session['user_id'])
        Job.objects.create(title = request.POST['title_post'],
                            description=request.POST['description_post'],
                            location=request.POST['location_post'],
                            created_by=created_by)
    return redirect("/dashboard")

def user_job(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "job_dash" : Job.objects.get(id=id)
    } 
    return render(request, "exam/user_job.html", context)
    
def edit_job_page(request, id):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        "job_dash" : Job.objects.get(id=id)
    } 
    return render(request, 'exam/edit.html', context)

def edit_job(request, id):
    errors =Job.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit_job_page/'+id)
    else:
        job = Job.objects.get(id =id)
        job.title=request.POST['edit_one']
        job.description=request.POST['edit_two']
        job.location=request.POST['edit_three']
        job.save()
        return redirect('/dashboard')

def delete(request, id):
    job = Job.objects.get(id=id)
    if job.created_by.id == request.session["user_id"]:
        job.delete()
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')

def log_off(request):
    request.session.flush()
    return redirect('/')