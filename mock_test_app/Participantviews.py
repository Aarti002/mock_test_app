import json
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from mock_test_app.models import CustomUser,CompetitionType,Staffs,Participants,FeedBack,QuestionBank

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
            messages.success(request, "Your feedback has been recorded.")
            return HttpResponseRedirect("/add_feedback")
        except:
            messages.error(request, "Something went wrong, try again.")
            return HttpResponseRedirect("/add_feedback")


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
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,last_name=last_name, first_name=first_name,user_type=2)
            user.participants.address = address
            competition_obj=CompetitionType.objects.get(id=comp)
            user.participants.competition_id=competition_obj
            user.participants.gender = gender
            user.save()
            messages.success(request, "Details Saved, Thank you!")
            return HttpResponseRedirect("/add_participant")
        except:
            messages.error(request,"Something went wrong, try again.")
            return HttpResponseRedirect("/add_participant")


@csrf_exempt
def get_staff(request):
    staff_id=request.POST.get("chk_email")
    staff=Staffs.objects.get(id=staff_id)
    list_data=[]
    for s in staff:
        data_small={"id":s.admin.id,"name":s.admin.first_name+" "+s.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


def selected_question(request,exam_id):
    all_ques=QuestionBank.objects.filter(competition_id=exam_id)
    competition=CompetitionType.objects.get(id=exam_id)
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
            messages.success(request, "Changes Saved.")
            return HttpResponseRedirect(reverse("view_profile"))
        except:
            messages.error(request, "Failed to Save Details.")
            return HttpResponseRedirect(reverse("view_profile"))


def available_mock_test(request):
    all_competition=CompetitionType.objects.all()
    if request.user.user_type == "2":
        messages.info(request, "You are a participant you can appear in test if you want!")
    elif request.user.user_type == "3":
        messages.warning(request, 'Seems you are a Staff you can not visit test page.')
    else:
        messages.error(request, 'Seems you are Admin you can not visit test page.')
    return render(request, "Participant_templates/mock_test.html", {"available_competition": all_competition})


def instruction_page(request,exam_id):
    try:
        context={}
        competition_type=CompetitionType.objects.get(id=exam_id)
        all_questions=QuestionBank.objects.filter(competition_id=exam_id)
        total_question_count=all_questions.count()
        total_allowed_time=2*total_question_count
        context["competition_type"]=competition_type
        context["total_allowed_time"]=total_allowed_time
        context["all_questions"]=all_questions
        context["total_question_count"]=total_question_count
        return render(request, "Participant_templates/instruction_page.html", context)
    except Exception as e:
        messages.error(request, "Something went wrong. Try Again.")
        return HttpResponseRedirect("/participant_page")


def question_paper(request,competition_id):
    try:
        context={}
        questions=QuestionBank.objects.filter(competition_id=competition_id)
        context["questions"]=questions
        context["total_time"]=questions.count()*2*60
        return render(request, "Participant_templates/question_paper.html", context)
        
    except Exception as e:
        messages.error(request, "Something went wrong. Try Again.")
        return HttpResponseRedirect("/participant_page")


def collect_response(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("available_mock_test"))
    else:
        score=0
        participant=Participants.objects.get(admin_id=request.user.id)
        for key, value in request.POST.items():
            if key.startswith('option'):
                question_id = key.replace('option', '')
                correct_answer = QuestionBank.objects.get(id=question_id).answer
                if value==correct_answer:
                    score+=1
       
        participant.result=score
        participant.save()
        return HttpResponseRedirect("available_mock_test")
