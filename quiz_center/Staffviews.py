import json

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from quiz_center.models import CustomUser,CompetitionType,Staffs,Participants,FeedBack,QuestionBank

def add_staff(request):
    staff=Staffs.objects.all()
    return render(request, "register_admin.html",{"staffs":staff})
"""
def delete_staff(request,staff_id):
    Staffs.objects.filter(id=staff_id).delete()
    staffs = Staffs.objects.all()
    return render(request, "hod_templates/manage_staff_template.html", {"staffs": staffs})
"""


def manage_participant(request):
    participant = Participants.objects.all()
    return render(request, "Staff_templates/paticipant_list.html", {"participants": participant})


def save_staff(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect("/add_staff")
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect("/add_staff")


def add_competition(request):
    staff = Staffs.objects.all()
    return render(request, "Staff_templates/register_test.html", {"staffs": staff})

def save_competition(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
       # email=request.POST.get("email")
        staff_id=request.POST.get("email")
        staff = CustomUser.objects.get(id=staff_id)
        competition_name=request.POST.get("exam_name")
        about=request.POST.get("about")
        try:
            competition=CompetitionType(staff_id=staff,competition_name=competition_name,about=about)
            competition.save()
            messages.success(request,"Mock test has been added!")
            return HttpResponseRedirect("/add_competition")
        except:
            messages.error(request,"Ooops, something went wrong!")
            return HttpResponseRedirect("/add_competition")

def view_feedback(request):
    feedback = FeedBack.objects.all()
    return render(request,"Staff_templates/view_feedback.html",{"feedback":feedback})

def edit_participant_reply(request,feed_id):
    feedback=FeedBack.objects.get(id=feed_id)
    return render(request,"Staff_templates/reply_participant.html",{"feedback":feedback})

def edit_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("/edit_participant_reply")
    else:
        feed_id = request.POST.get("feed_id")
        feedback_reply = request.POST.get("reply")

        try:
            user = FeedBack.objects.get(id=feed_id)
            user.feedback_reply = feedback_reply

            user.save()
            messages.success(request, "Successfully replied to Staff. ")
            return HttpResponseRedirect("/view_feedback")
        except:
            messages.error(request, "Failed to reply to Staff.")
            return HttpResponseRedirect("/edit_participant_reply/" + feed_id)

def add_question(request):
    staff=Staffs.objects.all()
    comp=CompetitionType.objects.all()
    neet="Neet"
    all_ques = QuestionBank.objects.filter(staff_id=2)
    print(all_ques)
    return render(request,"Staff_templates/add_questions.html",{"staff":staff,"competition":comp})

def save_question(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
       # email=request.POST.get("email")
        staff_id=request.POST.get("email")
        staff = CustomUser.objects.get(id=staff_id)
        competition_id = request.POST.get("exam_name")
        competition = CompetitionType.objects.get(id=competition_id)
        question=request.POST.get("question")
        optionA=request.POST.get("optiona")
        optionB = request.POST.get("optionb")
        optionC = request.POST.get("optionc")
        optionD = request.POST.get("optiond")
        answer = request.POST.get("answer")
        try:
            question_insert=QuestionBank(staff_id=staff,question=question,optionA=optionA,optionB=optionB,optionC=optionC,optionD=optionD,answer=answer,competition_id=competition)
            question_insert.save()
            messages.success(request,"Question has been added!")
            return HttpResponseRedirect("/add_question")
        except:
            messages.error(request,"Ooops, something went wrong!")
            return HttpResponseRedirect("/add_question")


def mock_test_list(request):
    tests=CompetitionType.objects.all()
    print(request.user.user_type)
    if request.user.user_type == "2":
        messages.info(request, "You are a participant you can appear in test if you want!")
    elif request.user.user_type == "3":
        messages.warning(request, 'Seems you are a Staff you can not visit test page.')
    else:
        messages.error(request, 'Seems you are Admin you can not visit test page.')
    return render(request, "Staff_templates/mock_test_list.html", {"tests": tests})

