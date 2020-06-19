
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.shortcuts import render ,get_object_or_404 ,redirect ,HttpResponse
from .models import *
from user_auth.models import *

#**********************************************************************
import psycopg2



def DataConnection(command,query):
    try:
        connection = psycopg2.connect(user="group_m6",#group_m6
                                      password="F4jtszcr",#F4jtszcr
                                      host="134.122.66.119",#134.122.66.119
                                      port="5432",
                                      database="group_m6")#group_m6
        cursor = connection.cursor()
        outputData = ''
        if command == "select":
            cursor.execute(query)
            outputData = cursor.fetchall()

        elif (command == "update")  :
            cursor.execute(query)
            connection.commit()
            outputData = cursor.rowcount


    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
        return  outputData
#**********************************************************************




def index(request):
    all_jobs = DataConnection("select","select job_id,job_title,job_description,req_skill,allusers.logo,post_time from job left join company using(account) left join allusers using(account) where job_type='general' and status='available';")


    context = {
        'jobs': all_jobs,
        'from_job' : True,
    }
    if request.user.is_authenticated:
        user_account = "'"+request.user.username+"'"
        type_user = DataConnection(
            'select',
            "select user_type from allusers where account=" + user_account + " ;"
        )
        context.update({'type_user': type_user[0][0]})

    return render(request, 'website/index.html', context)




@login_required(login_url='login_user')
def my_applayed_jobs(request):
    user_account = "'"+request.user.username+"'"

    my_applayed_jobs = DataConnection(
        'select',
        "select std_account,job_id,logo,job.job_title,job.job_description,job.req_skill,company_massage,company_reply from application  join job using (job_id) join allusers on (job.account=allusers.account) where std_account =  "+user_account+";"
    )
    context = {
        'my_applayed_jobs' : my_applayed_jobs,
        'from_apply' : True,
    }
    return render(request,'website/index.html',context)


uniqe_views = []



@login_required(login_url='login_user')
def job_details(request,job_id):
    user_account="'"+request.user.username+"'"
    job_id_="'"+job_id+"'"
    job = DataConnection("select","select * from job where job_id ="+"'"+str(job_id)+"';")
    same_company = DataConnection("select","select account,campany_name,address,salary_range_from,salary_range_to,num_of_employees,logo from job full join company using (account)  join allusers using (account) where job_id ="+"'"+str(job_id)+"';")


    jobs_of_same_company = DataConnection("select","select job_id,job_title from job where account = "+"'"+str(same_company[0][0])+"';")
    is_appled = DataConnection(
        'select',
        "select exists(select * from application where std_account="+ user_account+" and job_id="+job_id_+" );"
    )
    type_user = DataConnection(
        'select',
        "select user_type from allusers where account="+ user_account+" ;"
    )

    if type_user[0][0] == "client":
        old_views = DataConnection("select", "select num_of_views from job where job_id =" + job_id_ + ";")
        old_views = old_views[0][0] + 1
        DataConnection(
            "update",
            "update job set num_of_views = " + str(old_views) + " where job_id = " + job_id_ + ";"
        )
        not_uniqe = DataConnection(
            'select',
            "select exists(select * from job_unique_view where job_id = "+job_id_+" and std_account = "+user_account+")"
        )
        uniqe = not (not_uniqe[0][0])
        if uniqe :
            DataConnection(
                'update',
                "insert into job_unique_view values ("+user_account+","+job_id_+");"
            )


    context = {
        'job' : job,
        'jobs_of_same_company': jobs_of_same_company,
        'same_company': same_company,
        'is_appled': is_appled[0][0],
        'type_user': type_user[0][0],


    }
    return render(request,'website/job_details.html',context)



@login_required(login_url='login_user')
def user_account_(request,user_username):
    user_account ="'"+user_username+"'"
    user_exist  = DataConnection(
        'select',
        "select exists(select * from allusers where account ="+user_account+");"
    )
    if user_exist[0][0]:
        user_ = ""

        user_type = DataConnection(
            'select',
            "select allusers.user_type from allusers where account =" + user_account + ";"
        )
        context = {

            'user_type': user_type[0][0],

            'guest': request.user.username != user_username
        }
        if user_type[0][0] == "company":
            user_ = DataConnection(
                'select',
                "select * from allusers join company using (account) where account=" + user_account + ";"
            )

        elif user_type[0][0] == "client":
            user_ = DataConnection(
                'select',
                "select * from allusers join client using (account) where account=" + user_account + ";"
            )
            practical_experiences = DataConnection(
                'select',
                "select * from practical_experiences where account = " + user_account + ";"
            )
            context.update({
                'practical_experiences': practical_experiences,
            })
        context.update({

            'user_': user_[0],
        })
        return render(request, 'website/user_account.html', context)
    else :
        return HttpResponse('page not found 404')



@login_required(login_url='login_user')
def apply_to_job(request,job_id2):
    user_account ="'"+request.user.username+"'"
    job_id_ = "'"+job_id2+"'"
    DataConnection(
        'update',
        "insert into application(std_account,job_id) values("+user_account+","+job_id_+");"
    )

    messages.info(request,'you applayed to this job sucssfully')
    return redirect('job_details',job_id2)



@login_required(login_url='login_user')
def delete_my_apply(request,job_id):
    user_account = "'" + request.user.username + "'"
    job_id_ = "'" + job_id + "'"

    DataConnection(
        'update',
        "delete from application where job_id="+job_id_+"and std_account="+user_account+";"
    )

    messages.info(request, 'delete apply done sucssfully')
    return redirect('job_details', job_id)



@login_required(login_url='login_user')
def all_students(request):
    all_student = DataConnection("select","select account,name,email,logo,address,skills from allusers join client using (account);")

    context={
        'all_students':all_student,
        'from_std' : True,
    }
    return render(request, 'website/index.html', context)




@login_required(login_url='login_user')
def all_companys(request):
    all_companys = DataConnection(
        'select',
        "select account,campany_name,address,email,logo,about_campany from company join allusers using (account);"
    )
    context={
        'all_companys':all_companys,
        'from_com' : True,
    }
    return render(request, 'website/index.html', context)



@login_required(login_url='login_user')
def add_job(request):
    user_account = "'"+request.user.username+"'"
    if request.method == "GET":
        return HttpResponse('Error 404')
    elif request.method == "POST" :

        title_ = "'"+request.POST['title']+"'"
        description_ = "'"+request.POST['description']+"'"
        skills_required_ = "'"+request.POST['skills_required']+"'"

        price_from_ ="'"+ str(request.POST['from'])+"'"
        price_to_ ="'"+ str(request.POST['to'])+"'"

        counter = DataConnection(
            'select',
            "select job_id from job where account ="+ user_account+"order by job_id desc limit 1 ;"
        )
        there_is_job = DataConnection(
            'select',
            "select exists(select * from job where account = "+user_account+")"
        )
        if not there_is_job[0][0] :
            counter = 1
        else:

            counter = counter[0][0]
            index_ = counter.index('_')
            counter = counter[index_+1:]
            counter = int(counter)+1

        job_ID ="'"+str((request.user.username)+"_"+str(counter))+"'"

        status = "'"+ "available"+"'"
        type = "'"+ "general"+"'"
        num_of_views = "'"+ str(0)+"'"
        DataConnection(
            'update',
            "insert into job(job_id,account,job_title,job_description,post_time,num_of_views,status,job_type,price_from,price_to,req_skill) values(" + job_ID + "," + user_account +"," + title_ +"," + description_ +",now()," + num_of_views + "," +status +"," + type +"," + price_from_ +"," + price_to_ +"," + skills_required_ +");"
        )
        messages.info(request,"The new Job has been add sucssfully<br>")
        return redirect('user_account',request.user.username)

@login_required(login_url='login_user')
def offer(request):
    user_account = "'"+request.user.username+"'"
    offers  = DataConnection(
        'select',
        "select job_id,std_account,job_title from offer join job using (job_id)  where std_account = "+user_account+";"
    )
    context = {
        'offers': offers,
        'from_offers' : True,
    }
    return render(request, 'website/index.html', context)

@login_required(login_url='login_user')
def my_jobs(request):
    user_account = "'"+request.user.username+"'"

    my_jobs = DataConnection(
        'select',
        "select job_id,account,job_title from job where account="+user_account+" ;"
    )
    context = {
        'my_jobs' : my_jobs,
        'from_myjob' : True,
    }
    return render(request,'website/index.html',context)
@login_required(login_url='login_user')
def delete_job(request,job_id):
    user_account = "'" + request.user.username + "'"
    job_id_ = "'" + job_id + "'"
    DataConnection(
        'update',
        "delete from application where job_id=" + job_id_ +";"
    )
    DataConnection(
        'update',
        "delete from offer where job_id=" + job_id_ + ";"
    )
    DataConnection(
        'update',
        "delete from job_unique_view where job_id=" + job_id_ + ";"
    )
    DataConnection(
        'update',
        "delete from job where job_id="+job_id_+"and account="+user_account+";"
    )

    messages.info(request, 'delete job done sucssfully')
    return redirect('user_account', request.user.username)
@login_required(login_url='login_user')
def add_practical(request):
    user_account = "'" + request.user.username + "'"
    if request.method == "POST":
        title_ = "'" + request.POST['title'] + "'"
        description_ = "'" + request.POST['description'] + "'"

        if 'image' in request.FILES:
            image_ = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(
                'project_images/' + str(request.user.username) + '/' + str(request.user.username) + "_" + str(image_.name), image_)
            uploaded_file_url = fs.url(filename)
            text = str(uploaded_file_url)

            text2 = "'" + text + "'"
            DataConnection(
                'update',
                "insert into practical_experiences values ("+user_account+","+title_+","+description_+","+text2+");"
            )
        else :
            DataConnection(
                'update',
                "insert into practical_experiences values (" + user_account + "," + title_ + "," + description_ + ",'/media/project_default_image.jpg');"
            )
        messages.info(request,'Project Added sucssfully')
        return redirect('edit_account_information')


@login_required(login_url='login_user')
def accept(request,job_id,std_id):
    job_id_ = "'"+job_id+"'"
    std_id_ = "'"+std_id+"'"
    if request.method == "POST" :
        message = "'"+request.POST['message']+"'"
        DataConnection(
            'update',
            "update application set company_massage = "+message+" , company_reply = 'accept' where application.job_id = "+job_id_+" and application.std_account = "+std_id_+";"
        )
        messages.info(request,"Student accepted to job sucssfully")
        return redirect('job_details',job_id)
@login_required(login_url='login_user')
def reject(request,job_id,std_id):
    job_id_ = "'"+job_id+"'"
    std_id_ = "'"+std_id+"'"
    if request.method == "POST" :
        message = "'"+request.POST['message']+"'"
        DataConnection(
            'update',
            "update application set company_massage = "+message+" , company_reply = 'refuse' where application.job_id = "+job_id_+" and application.std_account = "+std_id_+";"
        )
        messages.info(request,"Student rejected sucssfully")
        return redirect('job_details',job_id)
@login_required(login_url='login_user')
def settings_job(request,job_id):

    req = DataConnection(
        'select',
        "select account from job where job_id = "+"'"+job_id+"'"+";"
    )
    if request.user.username == req[0][0]:
        job_id_ = "'"+job_id+"'"
        all_students_apply_to_this_job = DataConnection(
            "select",
            "select allusers.account,name,job.account,job.job_id from client join allusers using (account) join application on (client.account=application.std_account) join job using (job_id) where application.job_id = " + job_id_ + " and application.company_reply = 'no_reply' ;"
        )
        all_students_got_answers = DataConnection(
            "select",
            "select allusers.account,name,job.job_id,application.company_massage,application.company_reply from client join allusers using (account) join application on (client.account=application.std_account) join job using (job_id) where application.job_id =  " + job_id_ + "  and application.company_reply != 'no_reply'  ;"
        )
        views = DataConnection("select", "select num_of_views from job where job_id =" + job_id_ + ";")
        uniqe_views = DataConnection(
            'select',
            "select count(*) from job_unique_view where job_id = "+job_id_+";"
        )

        context = {
            'all_students_apply_to_this_job':all_students_apply_to_this_job,
            'all_students_got_answers':all_students_got_answers,
            'views':views,
            'uniqe_views':uniqe_views[0][0],
        }
        return render(request, 'website/job_settings.html', context)
    else :
        return HttpResponse("ERORR 404")
@login_required(login_url='login_user')
def delete_project(request):
    if request.method == "POST":
        std = request.POST['std']
        title = request.POST['title']
        desc = request.POST['desc']
        image = request.POST['image']


        std_ = "'" + std + "'"
        title_ = "'" + title + "'"
        desc_ = "'" + desc + "'"
        image_ = "'" + image + "'"
        DataConnection(
            "update",
            "delete from practical_experiences where account ="+std_+" and title = "+title_+"  and about = "+desc_+"  and image = "+image_+" ;"
        )
        messages.info(request, "Project Deleted sucssfully")
        return redirect('edit_account_information')



def my_function(postgresql,sqllite,postgress):
  for user in postgresql:
      if user[0] in sqllite:
        continue
      else:
          User.objects.create_user(
              username=user[0],
              password=user[1]
          )
  for user in sqllite:
      if user in postgress:
        continue
      else:
        user_ = User.objects.get(username=user)
        user_.delete()








def refesh(request):
    postgresql1 = DataConnection(
        'select',
        "select account,\"password\" from allusers;"
    )

    c = []
    d = []
    for i in postgresql1:
        c.append(i[0])
        c.append(i[1])
        d.append(c)
        c = []
    sqllite1 = User.objects.all()
    a = []

    for i in sqllite1:
        a.append(i.username)
    postgress1d = []
    for i in range(0, len(d)):
        postgress1d.append(postgresql1[i][0])
    my_function(d,a,postgress1d)
    return redirect('index')

