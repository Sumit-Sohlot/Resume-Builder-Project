from django.urls import path
from . import views

urlpatterns = [
    # Main resume page (requires login)
    path("", views.index, name="index"),
    
    # Authentication URLs
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.user_logout, name='logout'),
    
    # Resume management
    path("resume-list/", views.resume_list, name='resume-list'),
    path("<int:id>/download/", views.download, name="download"),
]
