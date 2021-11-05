from math import ceil

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from quiz_center.EmailBackEnd import EmailBackEnd
from quiz_center.models import CustomUser,CompetitionType,Staffs,FeedBack,Participants
from django.core.mail import send_mail


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

def index(request):
    competition=CompetitionType.objects.all()
    feedback=FeedBack.objects.all()
    n=len(feedback)
    n1=len(competition)
    n1Slides=n1//3+ceil((n1/3)-(n1//3))
    allset1=[[competition,range(1,n1),n1Slides]]
    nSlides=n//3+ceil((n/3)-(n//3))
    allset=[[feedback,range(1,n),nSlides]]
    return render(request,"index.html",{"competition":competition,"feedback":feedback ,"nSlides":nSlides,"n1Slides":n1Slides,"range1":range(1,n1Slides),"range":range(1,nSlides),"allset":allset,"allset1":allset1})

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
            return HttpResponseRedirect("/")

def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/")