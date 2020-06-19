from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name="index"),
    path('account/<str:user_username>/',user_account_,name="user_account"),

    path('job/<str:job_id>',job_details,name="job_details"),

    path('applyed_jobs/',my_applayed_jobs,name="my_applayed_jobs"),

    path('companys/',all_companys,name="all_companys"),

    path('students/',all_students,name="all_students"),

    path('apply/<str:job_id2>',apply_to_job,name="apply_to_job"),

    path('delete_apply/<str:job_id>',delete_my_apply,name="delete_my_apply"),


    path('add_job/',add_job,name="add_job"),

    path('offers/',offer,name="offer"),

    path('my_jobs/',my_jobs,name="my_jobs"),

    path('delete_job/<str:job_id>',delete_job,name="delete_job"),

    path('add_job/<str:job_id>',delete_job,name="delete_job"),
    path('accept/<str:job_id>/<str:std_id>',accept,name="accept"),
    path('ref/',refesh,name="refesh"),
    path('reject/<str:job_id>/<str:std_id>',reject,name="reject"),
    path('settings_job/<str:job_id>',settings_job,name="settings_job"),
    path('add_project',add_practical,name="add_practical"),

    path('delete_project/',delete_project,name="delete_project"),

]
