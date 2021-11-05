import json
import pyautogui as pag
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from quiz_center.models import CustomUser,CompetitionType,Staffs,Participants,FeedBack,QuestionBank

def add_participant(request):
    competition=CompetitionType.objects.all()
    return render(request, "register_participant.html",{"competition":competition})

def participant_page(request):
    competition=CompetitionType.objects.all()
    feedback = FeedBack.objects.all()
    return render(request, "Participant_templates/participant_home.html",{"competition":competition,"feedback":feedback})

def view_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    participant=Participants.objects.get(admin=user.id)
    competition=CompetitionType.objects.all()
    return render(request,"Participant_templates/user_profile.html",{"user":user,"participant":participant,"competition":competition})

def add_feedback(request):
    student_obj = Participants.objects.get(admin=request.user.id)
    feedback_data = FeedBack.objects.all()
    return render(request,"Participant_templates/user_feedback.html",{"feedback":feedback_data})

def feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("/student_feedback")
    else:
        feedback_message=request.POST.get("feedback")
        student_obj = Participants.objects.get(admin=request.user.id)
        try:
            feedback_report=FeedBack(participant_id=student_obj,feedback=feedback_message,feedback_reply="")
            feedback_report.save()
            messages.success(request, "Your feedback has been recorded")
            return HttpResponseRedirect("/add_feedback")
        except:
            messages.error(request, "Something went wrong, try again!")
            return HttpResponseRedirect("/add_feedback")


"""def delete_student(request,student_id):
    Students.objects.filter(id=student_id).delete()
    students = Students.objects.all()
    return render(request, "hod_templates/manage_student_template.html", {"students": students})
"""
def save_participant(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        comp = request.POST.get("competition")
        gender = request.POST.get("gender")
        #profile_pic = request.POST.FILES

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,last_name=last_name, first_name=first_name,user_type=2)
            user.participants.address = address
            competition_obj=CompetitionType.objects.get(id=comp)
            user.participants.competition_id=competition_obj
            user.participants.gender = gender
            user.save()

            messages.success(request, "Woah, you are registered now!")
            return HttpResponseRedirect("/add_participant")
        except:
            messages.error(request,"Oops! something went wrong")
            return HttpResponseRedirect("/add_participant")



@csrf_exempt
def get_staff(request):
    staff_id=request.POST.get("chk_email")
    staff_user=request.POST.get("chk_username")

    staff=Staffs.objects.get(id=staff_id)
    list_data=[]

    for s in staff:
        data_small={"id":s.admin.id,"name":s.admin.first_name+" "+s.admin.last_name}
        list_data.append(data_small)
    print(list_data)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


"""
def delete_staff(request,staff_id):
    Staffs.objects.filter(id=staff_id).delete()
    staffs = Staffs.objects.all()
    return render(request, "hod_templates/manage_staff_template.html", {"staffs": staffs})
"""

def selected_question(request,exam_id):
    all_ques=QuestionBank.objects.filter(competition_id=exam_id)
    competition=CompetitionType.objects.get(id=exam_id)
    #print(all_ques)
    return render(request,"Test_papers/exam.html",{"question_set":all_ques,"competition":competition})

def save_participant_changes(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user = CustomUser.objects.get(id=request.user.id)
            user.first_name=first_name
            user.last_name=last_name
            if password!=None and password!="":
                user.password=password
            user.save()
            staff=Staffs.objects.get(admin=user.id)
            staff.address=address
            staff.save()
            messages.success(request, "Successfully Edited Participant Details!")
            return HttpResponseRedirect(reverse("view_profile"))
        except:
            messages.error(request, "Failed to Edit Participant Details!")
            return HttpResponseRedirect(reverse("view_profile"))

def available_mock_test(request):
    tests=CompetitionType.objects.all()
    print(request.user.user_type)
    if request.user.user_type == "2":
        messages.info(request, "You are a participant you can appear in test if you want!")
    elif request.user.user_type == "3":
        messages.warning(request, 'Seems you are a Staff you can not visit test page.')
    else:
        messages.error(request, 'Seems you are Admin you can not visit test page.')
    return render(request, "Participant_templates/mock_test.html", {"tests": tests})