"""quiz_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from mock_test_app import views

from mock_test_app import Adminviews

from mock_test_app import Participantviews,Staffviews

from quiz_app import settings

urlpatterns = [
    #Admin urls
    path('admin/', admin.site.urls),
    path('login_page', views.login_page,name="login_page"),
    path('staff_page', views.staff_page,name="staff_page"),
    path('dologin', views.dologin,name="dologin"),
    path('logout_page', views.logout_page,name="logout_page"),
    path('forgot_password', views.forgot_password,name="forgot_password"),
    path('reset_password', views.reset_password,name="reset_password"),
    path('change_password/<str:token>/', views.change_password,name="change_password"),
    path('contact_message', views.contact_message,name="contact_message"),

    #Staff urls
    path('view_feedback', Staffviews.view_feedback,name="view_feedback"),
    path('edit_participant_reply/<str:feed_id>', Staffviews.edit_participant_reply, name="edit_participant_reply"),
    path('edit_feedback_save', Staffviews.edit_feedback_save, name="edit_feedback_save"),
    path('add_staff', Staffviews.add_staff,name="add_staff"),
    path('save_staff', Staffviews.save_staff,name="save_staff"),
    path('add_competition', Staffviews.add_competition, name="add_competition"),
    path('save_competition', Staffviews.save_competition, name="save_competition"),
    path('add_question', Staffviews.add_question, name="add_question"),
    path('save_question', Staffviews.save_question, name="save_question"),
    path('mock_test_list', Staffviews.mock_test_list, name="mock_test_list"),
    path('manage_participant', Staffviews.manage_participant, name="manage_participant"),
    path('edit_competition_details/<str:type_id>', Staffviews.edit_competition_details, name="edit_competition_details"),
    path('edit_competition_detail_save', Staffviews.edit_competition_detail_save, name="edit_competition_detail_save"),

    #Participants urls
    path('add_participant', Participantviews.add_participant,name="add_participant"),
    path('add_feedback', Participantviews.add_feedback,name="add_feedback"),
    path('feedback_save', Participantviews.feedback_save, name="feedback_save"),
    path('view_profile', Participantviews.view_profile,name="view_profile"),
    path('participant_page', Participantviews.participant_page,name="participant_page"),
    path('save_participant', Participantviews.save_participant,name="save_participant"),
    path('get_staff', Participantviews.get_staff, name="get_staff"),
    path('selected_question/<str:exam_id>', Participantviews.selected_question, name="selected_question"),
    path('save_participant_changes', Participantviews.save_participant_changes, name="save_participant_changes"),
    path('available_mock_test', Participantviews.available_mock_test, name="available_mock_test"),
    path('instruction_page/<str:exam_id>', Participantviews.instruction_page,name="instruction_page"),
    path('question_paper/<str:competition_id>', Participantviews.question_paper,name="question_paper"),
    path('collect_response', Participantviews.collect_response,name="collect_response"),
    

    #HOME page
    path('', views.home_page,name="home_page"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
