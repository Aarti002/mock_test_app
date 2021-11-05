from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class CustomUser(AbstractUser):
    user_type_data=((1,"Admin"),(2,"Participants"),(3,"Staffs"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default="")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Staffs(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default="")
    gender=models.CharField(max_length=255,default="")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class CompetitionType(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE,default="")
    competition_name=models.CharField(max_length=255,default="")
    about=models.TextField(default="")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class QuestionBank(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default="")
    question=models.CharField(max_length=255,default="")
    optionA=models.CharField(max_length=200,default="")
    optionB = models.CharField(max_length=200, default="")
    optionC = models.CharField(max_length=200, default="")
    optionD = models.CharField(max_length=200, default="")
    answer = models.CharField(max_length=200, default="")
    competition_id=models.ForeignKey(CompetitionType, on_delete=models.CASCADE, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Participants(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default="")
    competition_id = models.ForeignKey(CompetitionType, on_delete=models.DO_NOTHING)
    person_image=models.ImageField(upload_to="Images/",default="")
    gender=models.CharField(max_length=255,default="")
    address=models.TextField()
    result=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBack(models.Model):
    id = models.AutoField(primary_key=True)
    participant_id = models.ForeignKey(Participants, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    participant_id = models.ForeignKey(Participants, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()



@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Participants.objects.create(admin=instance,competition_id=CompetitionType.objects.get(id=1),address="",gender="")
        if instance.user_type == 3:
            Staffs.objects.create(admin=instance)

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.participants.save()
    if instance.user_type == 3:
        instance.staffs.save()
