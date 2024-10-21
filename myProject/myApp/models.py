from django.db import models
from django.contrib.auth.models import AbstractUser

class customUser(AbstractUser):
    
    USER=[
        ('recruiter','Recruiter'),
        ('seeker','Seeker'),
    ]
    user_type=models.CharField(choices=USER,max_length=100,null=True)
    Profile_Pic=models.ImageField(upload_to='Media/Profile_Pic',null=True)
    
    def __str__(self):  
        
        return f"{self.username}-{self.user_type}"
    
class SkillModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class seekerProfileModel(models.Model):
    
    
    user=models.OneToOneField(customUser,on_delete=models.CASCADE,related_name='seekerProfile')
    skills = models.ManyToManyField(SkillModel,null=True)
    resume = models.FileField(upload_to='Media/Resume',null=True)
   
    
    def __str__(self):
        return f"{self.user.username}-{self.user.user_type}"
    
    
class recruiterProfileModel(models.Model):
    
   
    user = models.OneToOneField(customUser, on_delete=models.CASCADE,related_name='recruiterProfile')
    company_name = models.CharField(max_length=100,null=True)
    company_info = models.TextField(null=True)
   
    def __str__(self):
        return f"{self.user.username} {self.user.user_type} {self.company_name}"
    
    
class JobModel(models.Model):
    user = models.ForeignKey(customUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    openings = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    Job_Image=models.ImageField(upload_to='Media/Job_Image',null=True)
    skills_required = models.ManyToManyField(SkillModel, related_name='jobs_model', blank=True)
    
    def __str__(self):
        return f"{self.user.username} {self.title}"

class JobApplicationModel(models.Model):
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE)
    user = models.ForeignKey(customUser, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
    skills_required = models.ManyToManyField(SkillModel, related_name='job_applications', blank=True)
    resume = models.FileField(upload_to='Media/Resumes', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.title} - Applied on {self.applied_on}"
