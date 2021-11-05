from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from quiz_center.models import CustomUser,CompetitionType


def add_admin(request):
    return render(request, "register_admin.html")

"""def delete_student(request,student_id):
    Students.objects.filter(id=student_id).delete()
    students = Students.objects.all()
    return render(request, "hod_templates/manage_student_template.html", {"students": students})
"""
def save_admin(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,last_name=last_name, first_name=first_name,user_type=2)


            user.admin.gender = gender
            user.save()
            messages.success(request, "Woah, you are registered now!")
            return HttpResponseRedirect("/add_participant")
        except:
            messages.error(request,"Oops! something went wrong")
            return HttpResponseRedirect("/add_participant")

