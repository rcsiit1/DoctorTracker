from django.shortcuts import render
from .models import *
from random import randint
from .utils import *


# Create your views here.

def LoginPage(request):
    return render(request,"doctorfinder/login.html")

def RegistrationPage(request):
    return render(request,'doctorfinder/registration.html')

def RegisterUser(request):
    try:
        if request.POST['role'] == 'doctor':
            role = request.POST['role']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            password = request.POST['password']
            confirmpassword = request.POST['confirmpassword']
            gender = request.POST['gender']
            email = request.POST['email']
            speciality = request.POST['speciality']
            dateofbirth = request.POST['birthdate']
            city = request.POST['city']
            mobile = str(request.POST['phone'])

            user = User.objects.filter(email = email)
            if user:
                message = 'This email already exists'
                return render(request,'doctorfinder/registration.html',{'message':message})
            else:
                if password == confirmpassword:
                    otp = randint(100000, 9999999)
                    newuser = User.objects.create(email = email, password= password,role = role, otp = otp)  
                    newdoctor = Doctor.objects.create(user_id = newuser,firstname = firstname, lastname = lastname, gender = gender, speciality = speciality, city = city, mobile = mobile, birthdate = dateofbirth)
                    email_subject = "Doctor Finder : Account Vericication"
                    sendmail(email_subject,'mail_template',email,{'name':firstname,'otp':otp,'link':'http://localhost:8000/enterprise/user_verify/'})
                    return render(request,'doctorfinder/SuccessfulRegistration.html')
                else:
                    message = "Password and confirm password doesn't match"
                    return render(request,'doctorfinder/registration.html',{'message':message})

        else:
            role = request.POST['role']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            password = request.POST['password']
            confirmpassword = request.POST['confirm']
            gender = request.POST['gender']
            email = request.POST['email']
            dateofbirth = request.POST['birthdate']
            city = request.POST['city']
            mobile = str(request.POST['phone'])
            user = User.objects.filter(email = email)
            if user:
                message = 'This email already exists'
                return render(request,'doctorfinder/registration.html',{'message':message})
            else:
                if password == confirmpassword:
                    otp = randint(100000, 9999999)
                    newuser = User.objects.create(email = email, password= password,role = role, otp = otp)  
                    newpatient = Patient.objects.create(user_id = newuser,firstname = firstname, lastname = lastname, gender = gender, city = city, mobile = mobile, birthdate = dateofbirth)
                    email_subject = "Doctor Finder : Account Vericication"
                    sendmail(email_subject,'mail_template',email,{'name':firstname,'otp':otp,'link':'http://localhost:8000/enterprise/user_verify/'})
                    return render(request,'doctorfinder/SuccessfulRegistration.html')
                else:
                    message = "Password and confirm password doesn't match"
                    return render(request,'doctorfinder/registration.html',{'message':message})
    except User.DoesNotExist:
        message = 'This email already exists'
        return render(request,'doctorfinder/registration.html',{'message':message})

def login_evaluation(request):
    if request.POST['role'] == 'doctor':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email = email)
        print(user)
        if user:
            if user.password == password:
                doctor = Doctor.objects.get(user_id = user)
                request.session['email'] = user.email
                request.session['firstname'] = doctor.firstname
                return render(request,"doctorfinder/homepage-doctor.html")
            else:
                message = "Your password is incorrect or user doesn't exist"
                return render(request,"doctorfinder/login.html",{'message':message})
        else:
            message = "user doesn't exist"
            return render(request,"doctorfinder/login.html",{'message':message})
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email = email)
        print(user)
        if user:
            if user.password == password:
                patient = Patient.objects.get(user_id = user)
                request.session['email'] = user.email
                request.session['firstname'] = patient.firstname
                return render(request,"doctorfinder/homepage-doctor.html")
            else:
                message = "Your password is incorrect or user doesn't exist"
                return render(request,"doctorfinder/login.html",{'message':message})
        else:
            message = "user doesn't exist"
            return render(request,"doctorfinder/login.html",{'message':message})

