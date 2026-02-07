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

from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validation checks
        if not username or not email or not password1 or not password2:
            messages.error(request, "All fields are required")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if len(password1) < 6:
            messages.error(request, "Password must be at least 6 characters long")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()

            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")
        except Exception as e:
            messages.error(request, "Error creating account. Please try again.")
            return redirect("register")

    return render(request, "register.html")


def login_view(request):
    # NOTE: Temporarily removed the authenticated check to test
    # Uncomment these lines after testing:
    # if request.user.is_authenticated:
    #     return redirect("index")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validation
        if not username or not password:
            messages.error(request, "Please enter both username and password")
            return render(request, "login.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            # Redirect to next page if exists, otherwise to resume page
            next_page = request.GET.get('next', 'index')
            return redirect(next_page)
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "login.html")

    return render(request, "login.html")


@login_required
def user_logout(request):
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
