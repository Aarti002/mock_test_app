from math import ceil

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from mock_test_app.EmailBackEnd import EmailBackEnd
from mock_test_app.models import CustomUser,CompetitionType,Staffs,FeedBack,Participants
from django.core.mail import send_mail
import uuid
from .helper import send_forget_password_mail, send_contact_message_mail

def home_page(request):
    feedback = FeedBack.objects.all()
    n = len(feedback)
    nSlides = n // 3 + ceil((n / 3) - (n // 3))
    allset = [[feedback, range(1, n), nSlides]]
    if request.method == 'POST':
        name=request.POST.get('full_name')
        email = request.POST.get('full_email')
        contact = request.POST.get('contact_no')
        mssg = request.POST.get('message')
        sub=request.POST.get('subject')
        data={
            'name':name,
            'email':email,
            'subject':sub,
            'message':mssg,
        }
        message = '''
        New Message: {}
        
        From: {}
        '''.format(data['message'],data['email'])
        send_mail(data['subject'],message,'',['aartikumarisingh120@gmail.com'])
    return render(request,'home_page.html',{"feedback":feedback ,"nSlides":nSlides,"range":range(1,nSlides),"allset":allset})


def staff_page(request):
    competition = CompetitionType.objects.all()
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user.id)
    return render(request,"Staff_templates/staff_home.html",{"competition":competition,"user":user})


def register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form':form})

def login_page(request):
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/index')
    else:
        form = AuthenticationForm()

    return render(request, 'login_page.html', {'form': form})

def dologin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST['email'],password=request.POST['password'])
        if user!=None:
            login(request, user)
            if user.user_type=='1':
                return HttpResponseRedirect('/index')
            elif user.user_type=='2':
                return HttpResponseRedirect('/participant_page')
            elif user.user_type=='3':
                return HttpResponseRedirect('/staff_page')
            else:
                messages.error(request,"Invalid Login Details")
                return HttpResponseRedirect("/login_page")

        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/login_page")
        
def forgot_password(request):
    return render(request,"forgot_password.html")


def reset_password(request):
    try:
        if request.method == 'POST':
            user_email = request.POST.get('email')
            
            if not CustomUser.objects.filter(email=user_email):
                messages.error(request, 'Not user found with this username.')
                return HttpResponseRedirect("/forgot_password")
            
            user_obj = CustomUser.objects.get(email = user_email)
            token = str(uuid.uuid4().hex)
            user_obj.forgot_password_token=token
            user_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return HttpResponseRedirect("/forgot_password")
    except Exception as e:
        print(e)
    messages.info(request, 'Something went wrong.')
    return HttpResponseRedirect("/forgot_password")

def change_password(request,token):
    context={}
    try:
        profile_obj = CustomUser.objects.filter(forgot_password_token = token)
        context = {'user_id' : profile_obj[0].id}
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is None:
                messages.error(request, 'No user id found.')
                return HttpResponseRedirect("/change_password/"+token)
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return HttpResponseRedirect("/change_password/"+token)
                         
            user_password_update=CustomUser.objects.get(id=user_id)
            user_password_update.set_password(new_password)
            user_password_update.save()
            messages.success(request,"Password Updated")
            return HttpResponseRedirect("/login_page")
    except Exception as e:
        print(e)
    return render(request , 'change_password.html' , context)


def contact_message(request):
    try:

        if request.method == 'POST':
            sender_name = request.POST.get('full_name')
            sender_email = request.POST.get('full_email')
            sender_subject = request.POST.get('subject')
            sender_message = request.POST.get('message')
            send_contact_message_mail(sender_email, sender_message, sender_name, sender_subject)
            
            messages.success(request,"Message Sent.")
            return HttpResponseRedirect("/")
        else:
            messages.error(request,"Failed to sent Message.")
            return HttpResponseRedirect("/")
    except Exception as e:
        print(e)
    return HttpResponseRedirect("/")


def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/")