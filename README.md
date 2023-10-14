
  
A mock test portal is an online platform designed to provide users with practice tests and assessments for various academic, professional, or certification exams. These portals offer a simulated testing environment that allows users to prepare for real exams by taking timed, structured tests. They also provide feedback, scoring, and performance analysis to help users identify strengths and weaknesses in their knowledge and skills. Mock test portals are valuable tools for exam preparation, self-assessment, and skill improvement. They assist individuals in building confidence, managing exam-related stress, and tracking their progress toward achieving their academic and career goals.  
  
**Present Features :**  

- Admin Page
	- Add, Delete and Update Questions and Answers
	- Send Feedback
	- Add, Delete and Update Candidate details
	- ![[Screenshot from 2023-10-15 00-29-03.png]]

- Candidate
	- Participate in any exam
	- Provide feedback  
  ![[Screenshot from 2023-10-15 00-27-54.png]]
  
  
  
**Table format :**  
  

- Admin

	- admin_id=models.AutoField(primary_key=True)
	- user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default="")
	- gender=models.CharField(max_length=255,default="")

- Candidate

	- candidate_id=models.AutoField(primary_key=True)
	- user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default="")
	- address=models.CharField(max_length=255,default="")
	- result=models.IntegerField(default=0)

- CompetitionType

	- competition_id=models.AutoField(primary_key=True)
	- admin_id=models.ForeignKey(Admin,on_delete=models.CASCADE,default="")
	- competition_name=models.CharField(max_length=255,default="")
	- about=models.TextField(default="")

- Question

	- question_id=models.AutoField(primary_key=True)
	- staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default="")
	- question=models.CharField(max_length=255,default="")
	- optionA=models.CharField(max_length=200,default="")
	- optionB = models.CharField(max_length=200, default="")
	- optionC = models.CharField(max_length=200, default="")
	- optionD = models.CharField(max_length=200, default="")
	- answer = models.CharField(max_length=200, default="")
	- competition_id=models.ForeignKey(CompetitionType, on_delete=models.CASCADE, default="")

- FeedBack

	- feedback_id = models.AutoField(primary_key=True)
	- participant_id = models.ForeignKey(Participants, on_delete=models.CASCADE)
	- feedback = models.TextField()
	- feedback_reply = models.TextField()

- NotificationStudent

	- notification_id = models.AutoField(primary_key=True)
	- participant_id = models.ForeignKey(Participants, on_delete=models.CASCADE)
	- message = models.TextField()

  
  
  
**ER -**  
![[Screenshot from 2023-10-06 21-06-25.png]]
