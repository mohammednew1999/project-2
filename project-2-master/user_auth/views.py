from django.core.files.storage import FileSystemStorage
from django.shortcuts import render ,redirect , get_object_or_404 ,HttpResponseRedirect
from django.contrib.auth import login , authenticate ,logout ,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from website.views import DataConnection



def login_user(request):
    if request.user.is_authenticated:
        messages.info(request, 'u are aready loged in')
        return redirect('index')
    else :
        if request.method == "GET":
            messages.info(request, 'Please press the Login button')
            return redirect('index')

        elif request.method == "POST":
            user_username = request.POST['username']
            user_password = request.POST['password']
            user = authenticate(request, username=user_username, password=user_password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, "your username or password is incorrect , please try again")
                return redirect("index")

@login_required(login_url='login_user')
def logout_user(request) :
    if request.method == "POST" :
        logout(request)
        return redirect('index')

def sign_up_user(request) :
    if request.user.is_authenticated:
        messages.info(request,'You are already Registered')
        return redirect('index')
    else :
        if request.method == "GET" :
            messages.info(request, 'Please press the Sign Up button')
            return redirect('index')

        elif request.method == "POST" :
            # user_first_name = request.POST['first_name']
            # user_last_name = request.POST['last_name']
            user_account = request.POST['username']
            user_email = request.POST['email']
            user_password1 = request.POST['password1']
            user_password2 = request.POST['password2']
            user_type = request.POST['type']

            user_account_sql = "'"+user_account+"',"
            user_account_sql2 = "'"+user_account+"'"
            user_email_sql = "'"+user_email+"',"
            user_password1_sql = "'"+user_password1+"',"
            user_type_sql = "'"+user_type+"'"

            message = ''
            if user_account == '':
                message += 'please full the input of the Username<br>'
            if user_email == '':
                message += 'please full the input of the Email<br>'

            if (user_account == '') or (user_email == ''):
                context = {
                    # 'user_first_name': user_first_name,
                    # 'user_last_name': user_last_name,
                    'user_username': user_account,
                    'user_email': user_email,
                    'user_password1': user_password1,
                    'user_type': user_type,
                }
                messages.info(request, message)
                return render(request,'website/index.html',context)

            account_is_taken_array=DataConnection(
                "select",
                "select exists(select * from allusers where account="+"'"+str(user_account)+"');"
            )
            account_is_taken = account_is_taken_array[0][0]

            email_is_taken_array = DataConnection(
                "select",
                "select exists(select * from allusers where email="+"'"+str(user_email)+"');"
            )
            email_is_taken = email_is_taken_array[0][0]
            passwords_didnt_match = user_password1 != user_password2

            if account_is_taken:
                message += 'Username is taken, try another one<br>'
            if email_is_taken:
                message += 'Email is taken, try another one<br>'
            if passwords_didnt_match:
                message += 'Passwords didnt match<br>'

            if account_is_taken or email_is_taken or passwords_didnt_match:
                messages.info(request, message)
                context = {

                    'user_username': user_account,
                    'user_email': user_email,
                    'user_password1': user_password1,
                    'account_is_taken': account_is_taken,
                    'email_is_taken': email_is_taken,
                }
                return render(request,'website/index.html',context)


            else :
                user = User.objects.create_user(
                    username=user_account,
                    password=user_password1
                )
                user.save()
                DataConnection(
                    "update",
                    # "insert into allusers(account,email,password,usertype) values ('accountss1ss','emailsss@gmail.com','kkkk','client'); "
                    "insert into allusers(account,email,password,user_type) values ("+user_account_sql+user_email_sql+user_password1_sql+user_type_sql+"); "
                )
                if user_type == "company":
                    DataConnection(
                        "update",
                        "insert into company(account) values ("+user_account_sql2+");"
                    )
                elif user_type == "client":
                    DataConnection(
                        "update",
                        "insert into client(account) values (" + user_account_sql2 + ");"
                    )
                login(request, user)
                return redirect('edit_account_information')




@login_required(login_url='login_user')
def change_password(request) :
    user_account = "'"+request.user.username+"'"
    if request.method == "GET":
        messages.info(request, 'Change password button in the page down')
        return redirect('user_account', request.user.username)
    if request.method == "POST" :
        user_old_password = request.POST['old_password']
        user_new_password = request.POST['new_password']
        user_new_password2 = request.POST['new_password2']
        password_user = DataConnection(
            'select',
            "select password from allusers where account = "+user_account+";"
                                       )

        if password_user[0][0] != user_old_password:
            messages.info(request, 'the password(current) You entered is incorrect')
        elif user_new_password != user_new_password2 :
            messages.info(request, 'the new password did not matching')
        elif password_user[0][0] == user_new_password :
            messages.info(request, 'the new password can not be the old password')
        else :
            new_password = "'"+user_new_password+"'"
            request.user.set_password(user_new_password)
            request.user.save()
            DataConnection(
                'update',
                "update allusers set \"password\" = "+new_password+"  where account =" +user_account+";"
            )
            # update_session_auth_hash(request, user)
            messages.info(request, "Your password was changed sucssfully , please login again")
            logout(request)
            return redirect('index')
        return redirect('edit_account_information')


@login_required(login_url='login_user')
def edit_account_information(request):
    user_account = "'"+request.user.username+"'"

    if request.method == "GET" :
        user_ = ""
        practical_experiences = ""
        user_type = DataConnection(
            'select',
            "select allusers.user_type from allusers where account ="+user_account+";"
        )

        if user_type[0][0] == "company" :
            user_ = DataConnection(
                'select',
                "select * from allusers join company using (account) where account="+user_account+";"
            )

        elif user_type[0][0] == "client" :
            user_ = DataConnection(
                'select',
                "select * from allusers join client using (account) where account="+user_account+";"
            )
            practical_experiences = DataConnection(
                'select',
                "select * from practical_experiences where account = "+user_account+";"
            )
        context = {
            'user_' : user_[0],
            'user_type' : user_type[0][0],
            'practical_experiences' :practical_experiences,


        }
        return render(request,'user_auth/edit_account_info.html',context)
    elif request.method == "POST" :
        if "company_settings" in request.POST :
            user_account = "'"+request.user.username+"'"
            message = ""
            name_ ="'"+request.POST['name']+"'"
            company_name_ = "'"+request.POST['company_name']+"'"
            company_address_ = "'"+request.POST['company_address']+"'"
            salary_range_from = "'"+request.POST['salary_range_from']+"'"
            salary_range_to = "'"+request.POST['salary_range_to']+"'"
            number_of_employees_ = "'"+request.POST['number_of_employees']+"'"
            about_company_ = "'"+request.POST['about_company']+"'"
            DataConnection(
                'update',
                "update company set campany_name ="+company_name_+" ,address=" + company_address_ + "  ,salary_range_from = " + salary_range_from + " ,salary_range_to = " + salary_range_to + " ,num_of_employees=" + number_of_employees_ + " ,about_campany=" + about_company_ + "  where account = " + user_account + " ;"
            )

            DataConnection(
                'update',
                "update allusers set name = " + name_ + " where account =" + user_account + ";"
            )

            if 'company_logo' in request.FILES:
                company_logo_ = request.FILES['company_logo']
                fs = FileSystemStorage()
                filename = fs.save('companys_logo/' + str(request.user.username) + '/' + str(request.user.username) + "_" + str(company_logo_.name), company_logo_)
                uploaded_file_url = fs.url(filename)
                text = str(uploaded_file_url)
                text2 =  "'"+text+"'"
                DataConnection(
                    'update',
                    "update allusers set logo = "+text2+" where account = "+user_account+" ;"
                )

            if 'video' in request.FILES:
                company_video_ = request.FILES['video']
                fs = FileSystemStorage()
                filename = fs.save('companys_video/' + str(request.user.username) + '/' + str(request.user.username) + "_" + str(company_video_.name), company_video_)
                uploaded_file_url = fs.url(filename)
                text = str(uploaded_file_url)

                text2 = "'" + text + "'"
                DataConnection(
                    'update',
                    "update company set about_campany_video = " + text2 + " where account = " + user_account + " ;"
                )

            message += "The changes has been saved sucssfully <br>"

            messages.info(request,message)
            return redirect('edit_account_information')


        else :
            user_account = "'"+request.user.username+"'"
            message = ""

            name_ = "'"+request.POST['name']+"'"
            address_ = "'"+request.POST['address']+"'"
            birthday_ = "'"+request.POST['birthday']+"'"
            specialist_ = "'"+request.POST['specialist']+"'"
            skills_ = "'"+request.POST['skills']+"'"
            qualifications_ = "'"+request.POST['qualifications']+"'"
            education_ = "'"+request.POST['education']+"'"

            DataConnection(
                'update',
                "update client set birthday =cast("+birthday_+" as date)  ,address="+address_+"  ,qualifications = "+qualifications_+" ,skills = "+skills_+" ,education="+education_+" ,specialist="+specialist_+"  where account = "+user_account+" ;"
            )

            DataConnection(
               'update',
                "update allusers set name = "+name_+" where account ="+user_account+";"
            )



            if 'profile_image' in request.FILES:
                profile_image_ = request.FILES['profile_image']
                fs = FileSystemStorage()
                filename = fs.save('std_personal_images/' + str(request.user.username) + '/' + str(request.user.username) + "_" + str(profile_image_.name), profile_image_)
                uploaded_file_url = fs.url(filename)
                text = str(uploaded_file_url)
                text2 =  "'"+text+"'"
                DataConnection(
                    'update',
                    "update allusers set logo = "+text2+" where account = "+user_account+" ;"
                )


            if 'cv' in request.FILES:
                cv_ = request.FILES['cv']
                fs = FileSystemStorage()
                filename = fs.save('std_cv/' + str(request.user.username) + '/' + str(request.user.username) + "_" + str(cv_.name), cv_)
                uploaded_file_url = fs.url(filename)
                text = str(uploaded_file_url)
                text2 = "'" + text + "'"
                DataConnection(
                    'update',
                    "update client set cv = "+text2+" where account = "+user_account+" ;"
                )

            message += "The changes has been saved sucssfully <br>"

            messages.info(request, message)
            return redirect('edit_account_information')

#error views
def error_404(request,exception) :
    context = {

    }
    return render(request,'user_auth/errors/error_404.html',context)