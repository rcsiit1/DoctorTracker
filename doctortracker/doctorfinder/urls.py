"""doctortracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('registration/',views.RegistrationPage,name="registration"),
    path('login/',views.LoginPage,name="login"),
    path('registeruser/',views.RegisterUser, name="registeruser"),
    path('login_evealuate/',views.login_evaluation,name="login-evaluate"),
    path('forgotpassword/' ,views.forgotPage,name="forgot"),
    path('verify-otp-password/',views.forgotPassword,name="forgot-password"),
    path('logout/',views.logout,name="logout"),
    path('homepage/',views.Homepage,name="homepage"),
    path('reset-password/',views.ResetPassword,name="reset-password"),
    path('all-patient/',views.PatientList,name="patient-list"),
    path('edit-patient-profile/',views.EditPatientprofile,name="edit-patient-profile"),
    path('doctor-profile-picture/',views.DoctorProfilePicture,name="doctor-profile-picture"),
    path('',views.IndexPage,name="index"),
    path('add-patient',views.AddPatient,name="add-patient"),
    path('add-new-case',views.AddNewCase,name="add-new-case"),
    path('get-patient-details/',views.GetPatientDetails,name="get-patient-details"),
    path('create-new-case/',views.AddNewCaseToDatabase,name="create-new-case"),
    path('all-case/',views.allcase,name="allcase"),
    path('doctor-password/',views.doctor_password,name="doctor-password"),
    path('doctor-change-password/',views.doctor_change_password,name="doctor-change-password"),
    path('doctor-picture-profile/',views.doctor_pic_profile,name="doctor-profile"),
    path('change-doctor-pic/',views.change_profilepic,name="change-doctor-pic"),
    path('doc-profile/',views.doc_profile,name="doc-profile"),
    path('edit-doctor-profile/',views.edit_doctor_profile,name="edit-doctor-profile"),
    path('update-doctor-profile/',views.update_doctor_profile,name="update-doctor-profile"),
    path('delete-case/',views.deleteCase,name="delete-case"),
    path('get-schedules/',views.getAvailableSchedules,name="get-schedules"),
    
    
    #patient urls
    path('patient-homepage/',views.Patient_Homepage,name="Patient_Homepage"),
    path('update-patient-Health-profile/', views.update_Patient_Health_ProfilePage,name="update-patient-profile"),
    path('patient-profile-page/', views.patient_profile_page,name="edit-patient-profile-page"),
    path('update-patient-profile/', views.update_patient_profile,name="patient-profile-update"),
    path('view-patient-profile/', views.view_patient_profile,name="view-patient-profile"),
    path('change-patient-password/', views.changePatientPassword,name="change-patient-password"),
    path('update-patient-password/', views.updatePatientPassword,name="update-patient-password"),
    path('change-Patient-ProfilePic/', views.changePatientProfilePic,name="change-Patient-ProfilePic"),
    path('update-Patient-ProfilePic/', views.updatePatientProfilePic,name="update-Patient-ProfilePic"),
    path('aa', views.upload_file_page,name="upload_file_page"),
    path('upload/', views.upload_file,name="upload_file"),
    path('book-appointment/', views.bookAppointmentPage,name="book-appointment"),
    path('mark-availability/', views.markAvailability,name="mark-availability"),
    path('store-all-availabilities/',views.storeAllSchedules,name="store-all-availabilities"),
    path('delete-schedule/',views.deleteSchedule,name="delete-schedule"),
    path('delete-appointment/',views.deleteAppointment,name="delete-appointment"),
    path('book-appointment-patient/',views.bookAppointment,name="book-appointment-patient"),
    path('payment/',views.paymentPage,name="payment-page"),
    path('checkout/',views.createStripeSession,name="checkout"),
    path('success/',views.paymentSuccessPage,name="success"),
    path('fail/',views.paymentFailPage,name="fail"),
    path('purchase-fullfillment/',views.purchaseFullfillment,name="webhook-fullfillment")
    
    
]
 

