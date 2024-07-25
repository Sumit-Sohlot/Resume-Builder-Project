from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import resume_form, RegistrationForm, ResumeList
from .models import profile
from django.http import HttpResponse
from django.template import loader
import pdfkit


@login_required
def index(request):

    if request.method == "POST":
        name  = request.POST.get('name')
        email = request.POST.get('email')
        about = request.POST.get('about')
        college = request.POST.get('college')
        degree = request.POST.get('degree')
        project1 = request.POST.get('project1')

        pr1 = profile(
            name = name,
            email = email,
            about = about,
            college = college,
            degree = degree,
            project1 = project1,
        )

        pr1.save()
        return HttpResponse("Generation succesful")
    context = {
        "form" : resume_form()
    }
    return render(request, "resume.html", context)

@login_required
def view_resume(request, id):

    pr_details = profile.objects.get(id=id)
    context = {
        "id" : id,
        "name" : pr_details.name,
        "email" : pr_details.email,
        "about" : pr_details.about,
        "college" : pr_details.college,
        "degree" : pr_details.degree,
        "project1" : pr_details.project1,
    }

    return render(request, "resume_details.html", context)

@login_required
def download(request, id):

    pr_details = profile.objects.get(id=id)
    context = {
        "id": id,
        "name": pr_details.name,
        "email": pr_details.email,
        "about": pr_details.about,
        "college": pr_details.college,
        "degree": pr_details.degree,
        "project1": pr_details.project1,
    }
    template = loader.get_template('resume_details.html')
    html = template.render(context)
    options = {
        'page-size' : 'Letter',
        'encoding' : "UTF-8",
    }
    pdf = pdfkit.from_string(html,False,options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    #filename = 'resume.pdf'
    return response


    return HttpResponse("Download succesful")

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

        return HttpResponse("Invalid Data")

    form = RegistrationForm()
    return render(request,"register.html",{"form" : form})



def userlogin(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username, password=password)

        if user is not None:
            form = login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')
        else:
            return HttpResponse("Invalid credentails")


    form = AuthenticationForm()
    return render(request, 'login.html', {'form' : form})

@login_required
def userlogout(request):
    logout(request)

    messages.success(request,'Logout Successful!!')
    return redirect("login")

@login_required
def resume_list(request):
    if request.method == "POST":
        print(request.__dict__)
        id = request.POST.get('resume_id')
        return view_resume(request, id=id)
    return render(request, 'resume_list.html', {"form": ResumeList()})

