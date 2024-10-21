from django.shortcuts import render,redirect,get_object_or_404

from myApp.models import *
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def signupPage(request):
    
    if request.method=='POST':
        
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        Confirm_password=request.POST.get("Confirm_password")
        user_type=request.POST.get("user_type")
    
        
        if password==Confirm_password:
            
            
            user=customUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type,
            )
            if user_type=='seeker':
                seekerProfileModel.objects.create(user=user)
                
            elif user_type=='recruiter':
                recruiterProfileModel.objects.create(user=user)
            
            return redirect("signInPage")
            
    return render(request,"signupPage.html")


def signInPage(request):
    if request.method == 'POST':
        
        user_name=request.POST.get("username")
        pass_word=request.POST.get("password")

        try:
            user = authenticate(request, username=user_name, password=pass_word)

            if user is not None:
                login(request, user)
                return redirect('homePage') 
            else:
                return redirect('signInPage')

        except customUser.DoesNotExist:
            return redirect('signInPage')

    return render(request, 'signInPage.html')

@login_required
def homePage(request):
    
    
    return render(request,"homePage.html")


def logoutPage(request):
    
    logout(request)
    
    return redirect('signInPage')

@login_required
def profilePage(request):
    
    return render(request,"profilePage.html")

@login_required
def JobFeed(request):
    Job=JobModel.objects.all()
    
    context={
        'jobs':Job
    }
    
    return render(request,"JobFeed.html",context)

@login_required
def createdJob(request):
    
    current_user=request.user
    
    job=JobModel.objects.filter(user=current_user)
    
    context={
        "Jobs":job
    }
    return render(request,"createdJob.html",context)

@login_required
def deleteJob(request,job_id):
    
    JobModel.objects.get(id=job_id).delete()
    
    return redirect("createdJob")

@login_required


@login_required
def applyJob(request, job_id):
    job = JobModel.objects.get(id=job_id)

    if request.method == 'POST':
        skills_selected = request.POST.getlist('skills')
        resume = request.FILES.get('resume')

        application = JobApplicationModel(
            job=job,
            user=request.user,
            resume=resume,
        )
        application.save()

        for skill_id in skills_selected:
            skill = SkillModel.objects.get(id=skill_id)
            application.skills_required.add(skill)

        return redirect('JobFeed')  

    return render(request, 'applyJob.html', {'job': job})


def job_search(request):
    
    query=request.GET.get("query")
    
    if query:
        jobs=JobModel.objects.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query) |
            Q(user__username__icontains=query)
            )
    else:
        jobs=JobModel.objects.none()
        
    context={
        'jobs':jobs,
        'query':query
    }
    
    return render(request,"job_search.html",context)
    
    

@login_required
def editJob(request,job_id):
    
    job=JobModel.objects.get(id=job_id)
    all_skills = SkillModel.objects.all()

    
    if request.method == 'POST':
        j_id = request.POST.get('j_id')
        title = request.POST.get('title')
        openings = request.POST.get('openings')
        category = request.POST.get('category')
        description = request.POST.get('description')
        job_image = request.FILES.get('Job_Image')
        skills_required_ids = request.POST.getlist('skills_required')

        job = JobModel(
            id=j_id,
            user=request.user,
            title=title,
            openings=openings,
            category=category,
            description=description,
            Job_Image=job_image
        )
        job.save()

        for skill_id in skills_required_ids:
            skill = SkillModel.objects.get(id=skill_id)
            job.skills_required.add(skill)

        return redirect('createdJob')  
    
    context={
        "Jobs":job,
        'all_skills': all_skills
    }
    
    return render(request,"editJob.html",context)


@login_required
def viewJob(request,job_id):
    
    job=JobModel.objects.get(id=job_id)
    
    context={
        "Jobs":job
    }
    
    return render(request,"viewJob.html",context)


@login_required
def addJob(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        openings = request.POST.get('openings')
        category = request.POST.get('category')
        description = request.POST.get('description')
        job_image = request.FILES.get('Job_Image')
        skills_required_ids = request.POST.getlist('skills_required')

        job = JobModel(
            user=request.user,
            title=title,
            openings=openings,
            category=category,
            description=description,
            Job_Image=job_image
        )
        job.save()

        for skill_id in skills_required_ids:
            skill = SkillModel.objects.get(id=skill_id)
            job.skills_required.add(skill)

        return redirect('createdJob')  

    all_skills = SkillModel.objects.all() 
    return render(request, 'addJob.html', {'all_skills': all_skills})


