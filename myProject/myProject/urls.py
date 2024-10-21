from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from myProject.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',signupPage,name="signupPage"),
    path("signInPage/", signInPage, name="signInPage"),
    path("homePage/", homePage, name="homePage"),
    path("logoutPage/", logoutPage, name="logoutPage"),
    path("ProfilePage/", profilePage, name="profilePage"),
    path("JobFeed/", JobFeed, name="JobFeed"),
    path("createdJob/", createdJob, name="createdJob"),
    path("editJob/<str:job_id>", editJob, name="editJob"),
    path("deleteJob/<str:job_id>", deleteJob, name="deleteJob"),
    path("viewJob/<str:job_id>", viewJob, name="viewJob"),
    path("addJob/", addJob, name="addJob"),
    
    path("JobFeed/", JobFeed, name="JobFeed"),
    path("job_search/", job_search, name="job_search"),
    path("applyJob/<str:job_id>", applyJob, name="applyJob"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
