from django.shortcuts import render, HttpResponseRedirect, reverse
from django.http import JsonResponse, HttpResponse
from .models import *
from random import randint
from .utils import *
from django.core import serializers
from datetime import datetime, timedelta, date
import stripe
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def LoginPage(request):
    return render(request, "doctorfinder/login.html")


def IndexPage(request):
    return render(request, 'doctorfinder/index.html')


def RegistrationPage(request):
    return render(request, 'doctorfinder/registration.html')


def forgotPage(request):
    return render(request, "doctorfinder/forgot-password.html")


def AddPatient(request):
    return render(request, 'doctorfinder/add_patient.html')


def Homepage(request):
    if 'email' in request.session and 'role' in request.session:
        if request.session['role'] == 'patient':

            all_doctors = Doctor.objects.all()
            return render(request, 'doctorfinder/base.html', {'all_doctors': all_doctors})
        else:
            all_patients = Patient.objects.all()
            all_doctors = Doctor.objects.all()
            return render(request, 'doctorfinder/base.html', {'all_patients': all_patients, 'all_doctors': all_doctors})
    else:
        return HttpResponseRedirect(reverse('login'))


def Patient_Homepage(request):
    if 'email' in request.session and 'role' in request.session:
        if request.session['role'] == 'patient':
            all_doctors = Doctor.objects.all()
            return render(request, 'doctorfinder/patient_base.html', {'all_doctors': all_doctors})
        else:
            all_patients = Patient.objects.all()
            all_doctors = Doctor.objects.all()
            return render(request, 'doctorfinder/patient_base.html', {'all_patients': all_patients, 'all_doctors': all_doctors})
    else:
        return HttpResponseRedirect(reverse('login'))


def AddNewCase(request):
    all_patients = Patient.objects.all()
    return render(request, 'doctorfinder/new_case.html', {'all_patients': all_patients})


def GetPatientDetails(request):
    patient_id = request.GET['id']
    print('patientid ----------->', patient_id)
    patient_details = Patient.objects.filter(id=patient_id)
    print(patient_details)
    res = serializers.serialize('json', patient_details)
    return JsonResponse(res, safe=False)


def AddNewCaseToDatabase(request):
    patient_id = request.POST['patientid']
    print('patient ------>', patient_id)
    doctor_id = request.session['id']
    print('sdnfndoigo----->', doctor_id)
    patient = Patient.objects.get(id=patient_id)
    print("PATIENT:______________________", patient)
    doctor = Doctor.objects.get(user_id=doctor_id)
    print(doctor)
    disease = request.POST['disease']
    symptoms = request.POST['symptoms']
    pres = request.FILES['pres']

    print("------------------------------------>", pres)

    c_id = Case.objects.create(
        patient_id=patient, doctor_id=doctor, disease=disease, symptoms=symptoms)
    Prescription.objects.create(
        case_id=c_id, patient_id=patient, doctor_id=doctor, attachment_file=pres)

    return HttpResponseRedirect(reverse('homepage'))


def upload_file_page(request):
    return render(request, 'doctorfinder/upload_file.html')


def upload_file(request):
    myfile = request.FILES['myfile']
    sampleupload.objects.create(a_file=myfile)
    return HttpResponseRedirect(reverse('homepage'))


def EditPatientprofile(request):
    patient_id = request.POST['patient-id']
    patient_info = Patient.objects.get(id=patient_id)

    doctorid = Doctor.objects.get(user_id=request.session['id'])
    allcase = Case.objects.filter(
        doctor_id=doctorid, patient_id=patient_id).select_related('patient_id', "doctor_id")

    return render(request, 'doctorfinder/edit_patient.html', {'patient_info': patient_info, 'allcase': allcase})


def DoctorProfilePicture(request):
    return render(request, 'doctorfinder/settings_base.html')


def doctor_password(request):
    return render(request, 'doctorfinder/change_password.html')


def PatientList(request):
    all_patients = Patient.objects.all()
    res = serializers.serialize("json", all_patients)
    return JsonResponse(res, safe=False)


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

            user = User.objects.filter(email=email)
            if user:
                message = 'This email already exists'
                return render(request, 'doctorfinder/registration.html', {'message': message})
            else:
                if password == confirmpassword:
                    otp = randint(100000, 9999999)
                    newuser = User.objects.create(
                        email=email, password=password, role=role, otp=otp)
                    newdoctor = Doctor.objects.create(user_id=newuser, firstname=firstname, lastname=lastname,
                                                      gender=gender, speciality=speciality, city=city, mobile=mobile, birthdate=dateofbirth)
                    email_subject = "Doctor Finder : Account Vericication"
                    sendmail(email_subject, 'mail_template', email, {
                             'name': firstname, 'otp': otp, 'link': 'http://localhost:8000/enterprise/user_verify/'})
                    return render(request, 'doctorfinder/SuccessfulRegistration.html')
                else:
                    message = "Password and confirm password doesn't match"
                    return render(request, 'doctorfinder/registration.html', {'message': message})

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
            user = User.objects.filter(email=email)
            if user:
                message = 'This email already exists'
                return render(request, 'doctorfinder/registration.html', {'message': message})
            else:
                if password == confirmpassword:
                    otp = randint(100000, 9999999)
                    newuser = User.objects.create(
                        email=email, password=password, role=role, otp=otp)
                    newpatient = Patient.objects.create(
                        user_id=newuser, firstname=firstname, lastname=lastname, gender=gender, city=city, mobile=mobile, birthdate=dateofbirth)
                    email_subject = "Doctor Finder : Account Vericication"
                    sendmail(email_subject, 'mail_template', email, {
                             'name': firstname, 'otp': otp, 'link': 'http://localhost:8000/enterprise/user_verify/'})
                    return render(request, 'doctorfinder/SuccessfulRegistration.html')
                else:
                    message = "Password and confirm password doesn't match"
                    return render(request, 'doctorfinder/registration.html', {'message': message})
    except User.DoesNotExist:
        message = 'This email already exists'
        return render(request, 'doctorfinder/registration.html', {'message': message})


def login_evaluation(request):

    if request.POST['role'] == 'doctor':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email)
        print(user)
        if user[0]:
            if user[0].password == password and user[0].role == 'doctor':
                doctor = Doctor.objects.filter(user_id=user[0])
                request.session['email'] = user[0].email
                request.session['firstname'] = doctor[0].firstname
                request.session['role'] = user[0].role
                request.session['id'] = user[0].id

               # request.session['profile_pic']=doctor[0].profile_pic
                print("----------> Profile pic-->", doctor[0].profile_pic.url)

                return HttpResponseRedirect(reverse('homepage'))
            else:
                message = "Your password is incorrect or user doesn't exist"
                return render(request, "doctorfinder/login.html", {'message': message})
        else:
            message = "user doesn't exist"
            return render(request, "doctorfinder/login.html", {'message': message})

    if request.POST['role'] == 'patient':

        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email)
        print(user)
        if user[0]:
            if user[0].password == password and user[0].role == 'patient':
                patient = Patient.objects.filter(user_id=user[0])
                request.session['email'] = user[0].email
                request.session['firstname'] = patient[0].firstname
                request.session['role'] = user[0].role
                request.session['id'] = user[0].id
                return HttpResponseRedirect(reverse('Patient_Homepage'))
            else:
                message = "Your password is incorrect or user doesn't exist"
                return render(request, "doctorfinder/login.html", {'message': message})
        else:
            message = "user doesn't exist"
            return render(request, "doctorfinder/login.html", {'message': message})


def forgotPassword(request):
    email = request.POST['email']
    try:
        user = User.objects.get(email=email)
        if user:
            if user.email == email:
                otp = randint(100000, 9999999)
                user.otp = otp
                user.save()
                email_subject = "This is your new OTP"
                # link = "https://localhost:8000/example?email="+email+"&otp="+otp+"&random="+random
                sendmail(email_subject, 'mail_template', email, {'otp': otp})
                return render(request, 'doctorfinder/forgot-password-verification.html', {'email': email})
            else:
                message = 'This email does not match'
                return render(request, "doctorfinder/forgot-password.html", {'message': message})
        else:
            message = 'This email is not available'
            return render(request, "doctorfinder/forgot-password.html", {'message': message})
    except:
        message = 'This email is not available'
        return render(request, "doctorfinder/forgot-password.html", {'message': message})


def logout(request):
    del request.session['email']
    del request.session['role']
    del request.session['firstname']
    return HttpResponseRedirect(reverse('login'))


def ResetPassword(request):

    otp = request.POST['otp']
    newPassword = request.POST['newpass']
    confirmPassword = request.POST['confirmpass']
    email = request.POST['email']
    try:
        user = User.objects.get(email=email)
        if confirmPassword == newPassword and str(user.otp) == otp:
            user.password = newPassword
            user.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            message = "Either password and confirm password doesn't match or you have entered a wrong otp"
            return render(request, "doctorfinder/forgot-password-verification.html", {'message': message})
    except:
        message = "Ivalid request"
        return render(request, "doctorfinder/forgot-password-verification.html", {'message': message})


def allcase(request):
    print("--->> ", request.session['id'])

    doctorid = Doctor.objects.get(user_id=request.session['id'])
    allcase = Case.objects.filter(
        doctor_id=doctorid).select_related('patient_id', "doctor_id")
    print(allcase)

    for i in allcase:
        print("--> p - name ", i.patient_id.firstname)
        print("--> d - name ", i.doctor_id.firstname)

    return render(request, "doctorfinder/all_cases.html", {'allcase': allcase})


"""def update_patient_by_doc(request):
   
    id = request.POST['pid']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    gender = request.POST['gender']
    mobile = request.POST['mobile']
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']
    Marital_Status=request.POST['Marital_Status']
    blood_group=request.POST['blood_group']
    Blood_Presure=request.POST['Blood_Presure']
    Sugar=request.POST['Sugar']
    haemoglobin=request.POST['haemoglobin']
    try:
        patient_user=Patient.objects.get(id=id)
        if patient_user:
            patient_user.firstname=firstname
            patient_user.lastname=lastname
            patient_user.gender=gender
            patient_user.number=mobile
            patient_user.address=address
            patient_user.city=city
            patient_user.state=state
            patient_user.Marital_Status=Marital_Status
            patient_user.blood_group=blood_group
            patient_user.Blood_Presure=Blood_Presure
            patient_user.Sugar=Sugar
            patient_user.haemoglobin=Sugar
            patient_user.save()
            return HttpResponseRedirect(reverse('Homepage'))   
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('Homepage'))
"""


def update_Patient_Health_ProfilePage(request):
    id = request.POST['id']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    gender = request.POST['gender']
    mobile = request.POST['mobile']
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']

    blood_group = request.POST['blood_group']
    blood_presure = request.POST['blood_presure']
    sugar = request.POST['sugar']
    Haemoglobin = request.POST['Haemoglobin']

    disease = request.POST['disease']
    symptoms = request.POST['symptoms']
    case_status = request.POST['status']

    try:
        patient_user = Patient.objects.get(id=id)
        if patient_user:
            patient_user.firstname = firstname
            patient_user.lastname = lastname
            patient_user.gender = gender
            patient_user.number = mobile
            patient_user.address = address
            patient_user.city = city
            patient_user.state = state

            patient_user.blood_group = blood_group
            patient_user.blood_presure = blood_presure
            patient_user.sugar = sugar
            patient_user.Haemoglobin = Haemoglobin
            patient_user.save()

            case_id = request.POST['id']
            case_details = Case.objects.get(id=case_id)

            if case_details:
                case_details.disease = disease
                case_details.symptoms = symptoms
                case_details.status = case_status
                case_details.save()

            return HttpResponseRedirect(reverse('homepage'))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('homepage'))


def doctor_change_password(request):
    id = request.session['id']
    user = User.objects.get(id=id)

    old_password = user.password

    current = request.POST['current']
    new_password = request.POST['new_password']
    confirm = request.POST['confirm']

    if old_password == current and new_password == confirm:
        user.password = confirm
        user.save()
        message = "Your Password have been changed successfully!"
        return render(request, "doctorfinder/password_changed.html")
    else:
        error_msg = "Incorrect Password , Try Again  !!"
        return render(request, "doctorfinder/change_password.html", {'error_msg': error_msg})


def doctor_pic_profile(request):
    id = request.session['id']
    doc_id = Doctor.objects.get(user_id=id)

    if doc_id:
        pro_pic = doc_id.profile_pic
        return render(request, "doctorfinder/change_profile_pic.html", {'pro_pic': pro_pic})


def change_profilepic(request):
    doctor = Doctor.objects.get(user_id=request.session['id'])
    doctor.profile_pic = request.FILES['profile']
    doctor.save()
    # request.session['profile_pic']=doctor.profile_pic
    # print("############################--->",doctor.profile_pic)

    return HttpResponseRedirect(reverse('homepage'))


def doc_profile(request):
    id = request.session['id']
    doctor = Doctor.objects.get(user_id=id)

    user = User.objects.get(id=id)
    email = user.email

    if doctor and email:
        return render(request, "doctorfinder/doctor_profile.html", {'doctor': doctor, 'email': email})
    else:
        return HttpResponseRedirect(reverse('homepage'))


def edit_doctor_profile(request):
    id = request.session['id']
    doctor = Doctor.objects.get(user_id=id)
    user = User.objects.get(id=id)
    # email=user.email

    if doctor:
        return render(request, "doctorfinder/edit_doctor_profile.html", {'doctor': doctor})
    else:
        return HttpResponseRedirect(reverse('homepage'))


def update_doctor_profile(request):

    doctor = Doctor.objects.get(user_id=request.session['id'])

    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    mobile = request.POST['mobile']
    qualification = request.POST['qualification']
    specialization = request.POST['specialization']
    gender = request.POST['gender']
    city = request.POST['city']
    state = request.POST['state']
    location = request.POST['location']
    hospitals = request.POST['hospitals']
    address = request.POST['address']
    aboutme = request.POST['aboutme']

    if doctor:
        doctor.firstname = firstname
        doctor.lastname = lastname
        doctor.mobile = mobile
        doctor.qualification = qualification
        doctor.specialization = specialization
        doctor.gender = gender
        doctor.city = city
        doctor.state = state
        doctor.location = location
        doctor.address = address
        doctor.clinic = hospitals
        doctor.about_doc = aboutme
        doctor.save()
        return render(request, "doctorfinder/doctor_profile.html", {'doctor': doctor})
    else:
        print("Errrror ")


def patient_profile_page(request):
    patient = Patient.objects.get(user_id=request.session['id'])
    return render(request, "doctorfinder/patient_settings_base.html", {'patient': patient})


def update_patient_profile(request):
    patient = Patient.objects.get(user_id=request.session['id'])

    patient.firstname = request.POST['firstname']
    patient.lastname = request.POST['lastname']
    patient.mobile = request.POST['mobile']
    patient.address = request.POST['address']
    patient.gender = request.POST['gender']
    patient.city = request.POST['city']
    patient.state = request.POST['state']
    patient.save()
    return HttpResponseRedirect(reverse('Patient_Homepage'))


def view_patient_profile(request):
    id = request.session['id']
    patient_info = Patient.objects.get(user_id=id)

    # doctorid=Doctor.objects.get(user_id=request.session['id'])

    allcase = Case.objects.filter(
        patient_id=patient_info).select_related('patient_id', "doctor_id")

    """for i in allcase:
        print("--> p - name ",i.patient_id.firstname)
        print("--> d - name ",i.doctor_id.firstname)
        print("status --> ",i.status)"""

    return render(request, "doctorfinder/patient_profile.html", {'patient_info': patient_info, 'allcase': allcase})


def deleteCase(request):
    case_id = request.POST['caseid']
    delete_row = Case.objects.get(id=case_id)
    delete_row.delete()
    return HttpResponseRedirect(reverse('homepage'))


def changePatientPassword(request):
    return render(request, "doctorfinder/change_patient_password.html")


def updatePatientPassword(request):
    id = request.session['id']
    user = User.objects.get(id=id)

    old_password = user.password

    current = request.POST['current']
    new_password = request.POST['new_password']
    confirm = request.POST['confirm']

    if old_password == current and new_password == confirm:
        user.password = confirm
        user.save()
        message = "Your Password have been changed successfully!"
        return render(request, "doctorfinder/password_changed.html")
    else:
        error_msg = "Incorrect Password , Try Again  !!"
        return render(request, "doctorfinder/change_patient_password.html", {'error_msg': error_msg})


def changePatientProfilePic(request):
    return render(request, "doctorfinder/change_patient_profile_pic.html")


def updatePatientProfilePic(request):
    patient = Patient.objects.get(user_id=request.session['id'])
    patient.profile_pic = request.FILES['profile']
    patient.save()
    return HttpResponseRedirect(reverse('Patient_Homepage'))

    """doctor=Doctor.objects.get(user_id=request.session['id'])
    doctor.profile_pic=request.FILES['profile']
    doctor.save()"""


def bookAppointmentPage(request):
    print('this is role --->', request.session['role'])
    all_doctors = Doctor.objects.all()
    return render(request, "doctorfinder/book_appointment.html", {'all_doctors': all_doctors})


def markAvailability(request):
    if request.session['role'] == 'doctor':
        doctor_id = Doctor.objects.get(user_id=request.session['id'])
        all_availabilities = availability.objects.filter(
            doctor_id=doctor_id.id)
        return render(request, "doctorfinder/mark_availability.html", {'all_availabilities': all_availabilities})
    else:
        return HttpResponseRedirect(reverse('homepage'))


def storeAllSchedules(request):
    if request.session['role'] == 'doctor':
        start_date = datetime.strptime(
            request.POST['start_date'], "%Y-%m-%d").date()
        end_date = datetime.strptime(
            request.POST['end_date'], "%Y-%m-%d").date()
        start_time = request.POST['start_time']
        print('this is date', start_date)
        end_time = request.POST['end_time']
        doctor_id = Doctor.objects.get(user_id=request.session['id'])
        current_time = date.today()
        print(type(current_time))
        print(type(start_date))
        # if start_date > current_time and end_time > current_time:
        difference_in_days = end_date - start_date
        for i in range(0, int(difference_in_days.days)+1):
            modified_date = start_date + timedelta(days=i)
            for j in range(int(start_time), int(end_time) + 1):
                availability.objects.create(
                    doctor_id=doctor_id, avail_date=modified_date, start_time=str(j)+':00')
                availability.objects.create(
                    doctor_id=doctor_id, avail_date=modified_date, start_time=str(j)+':30')
        all_availabilities = availability.objects.filter(doctor_id=doctor_id)
        return HttpResponseRedirect(reverse('mark-availability'))
        # else:
        #     all_availabilities = availability.objects.filter(doctor_id = doctor_id)
        #     return render(request, "doctorfinder/mark_availability.html", {'all_availabilities': all_availabilities,'error':'Start and end time should be greater than current date'})
    else:
        return HttpResponseRedirect(reverse('homepage'))


def deleteSchedule(request):
    schedule_id = request.POST['id']
    availability.objects.get(id=schedule_id).delete()
    return HttpResponseRedirect(reverse('mark-availability'))


def deleteAppointment(request):
    try:
        schedule_id = request.POST['id']
        availability_id = availability.objects.get(id=schedule_id)
        # Appointment.objects.filter(id = 1).select_related('patient_id','doctor_id')
        Appointment.objects.get(availability_id=availability_id).delete()
        availability_id.status = False
        availability_id.save()
        return HttpResponseRedirect(reverse('mark-availability'))
    except:
        return HttpResponseRedirect(reverse('mark-availability'))


def getAvailableSchedules(request):
    doctor_id = request.GET['id']
    print('patientid ----------->', doctor_id)
    doctor_details = Doctor.objects.get(id=doctor_id)
    print(doctor_details)
    availability_list = availability.objects.filter(
        doctor_id=doctor_details, status=False)
    res = serializers.serialize('json', availability_list)
    return JsonResponse(res, safe=False)


def bookAppointment(request):
    if 'email' in request.session and 'role' in request.session:
        doctor_id = request.POST['doctor_id']
        schedule_id = request.POST['schedule_id']
        patient_id = Patient.objects.get(user_id=request.session['id'])
        doctor = Doctor.objects.get(id=doctor_id)
        schedule = availability.objects.get(id=schedule_id)
        schedule.status = True
        schedule.save()
        new_appointment = Appointment.objects.create(doctor_id=doctor, patient_id=patient_id,
                                availability_id=schedule, appointment_status=True)
        customer_details = Payments.objects.filter(
            email=request.session['email'])
        if customer_details:
            print('inside if statement')
            session = startStripeSession(customer_details[0].customer_id,new_appointment.pk)
            #print('this is session', session)
            return render(request, "doctorfinder/checkout.html", {'CHECKOUT_SESSION_ID': session.id})
        else:
            print('inside else')
            customer = stripe.Customer.create(email=request.session['email'])
            Payments.objects.create(
                email=request.session['email'], customer_id=customer.id, user_id=User.objects.get(id=request.session['id']))
            session = startStripeSession(customer.id,new_appointment.pk)
            #print('this is session', session)
            return render(request, "doctorfinder/checkout.html", {'CHECKOUT_SESSION_ID': session.id})
    else:
        return HttpResponseRedirect(reverse('login'))


def paymentPage(request):
    return render(request, "doctorfinder/payment.html")


def paymentSuccessPage(request):
    return render(request, "doctorfinder/success.html")


def paymentFailPage(request):
    return render(request, "doctorfinder/unsuccessfulls.html")

def confirmPaymentStatus(appointment_id):
    try:
        appointment_details = Appointment.objects.get(id = appointment_id)
        appointment_details.payment_status = True
        appointment_details.save()
        return True
    except:
        return False

# def createStripeSession(request):
#     if 'email' in request.session and 'role' in request.session:
#         customer_details = Payments.objects.filter(
#             email=request.session['email'])
#         if customer_details:
#             print('inside if statement')
#             session = startStripeSession(customer_details[0].customer_id)
#             #print('this is session', session)
#             return render(request, "doctorfinder/checkout.html", {'CHECKOUT_SESSION_ID': session.id})
#         else:
#             print('inside else')
#             customer = stripe.Customer.create(email=request.session['email'])
#             Payments.objects.create(
#                 email=request.session['email'], customer_id=customer.id, user_id=User.objects.get(id=request.session['id']))
#             session = startStripeSession(customer.id)
#             #print('this is session', session)
#             return render(request, "doctorfinder/checkout.html", {'CHECKOUT_SESSION_ID': session.id})

#     else:
#         return HttpResponseRedirect(reverse('login'))


# You can find your endpoint's secret in your webhook settings



@csrf_exempt
def purchaseFullfillment(request):
    print('webhook called --------------------------------------___>')
    endpoint_secret = 'whsec_GRxruQGY346JH3EnZxV7WUsNMJtmgEv9'
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        print('this is the session object from webhook',session)
        confirmPaymentStatus(session.display_items[0].custom.description)

    return HttpResponse(status=200)

def listAllScheduledAppointments(request):
    patient_details = Patient.objects.get( user_id = request.session['id'])
    all_appointments = Appointment.objects.filter(patient_id = patient_details)
    return render(request,"doctorfinder/list_appointments.html",{'all_appointments':all_appointments})