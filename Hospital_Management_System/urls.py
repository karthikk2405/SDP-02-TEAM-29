"""Hospital_Management_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from hopital.views import *
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home,name="home"),
    path('login_user',Login_User,name="login_user"),
    path('contact',Contact,name="contact"),
    path('about',About,name="about"),
    path('login_admin',Login_Admin,name="login_admin"),
    path('signup',Signup,name="signup"),
    path('add_res',Signup_Res,name="add_res"),
    path('admin_home',Admin_Home,name="admin_home"),
    path('res_home',Res_Home,name="res_home"),
    path('profile',profile,name="profile"),
    path('edit_profile',Edit_profile,name="edit_profile"),
    path('edit_doctor_profile',Edit_doctor_profile,name="edit_doctor_profile"),
    path('doctor_profile',Doctor_profile,name="doctor_profile"),
    path('all_doctor',All_Doctor,name="all_doctor"),
    path('add_appointment(<int:pid>)',Add_Appointment,name="add_appointment"),
    path('doctor_detail(<int:pid>)',Doctor_detail,name="doctor_detail"),
    path('add_prescription(<int:pid>)',Add_Prescription,name="add_prescription"),
    path('view_appointment',View_Appointment,name="view_appointment"),
    path('doctor_view_appointment',Doctor_View_Appointment,name="doctor_view_appointment"),
    path('view_prescription',View_Prescription,name="view_prescription"),
    path('Pat_Change_Password',Pat_Change_Password,name="Pat_Change_Password"),
    path('Res_Change_Password',Res_Change_Password,name="Res_Change_Password"),
    path('Hr_Change_Password',Hr_Change_Password,name="Hr_Change_Password"),
    path('Doc_Change_Password',Doc_Change_Password,name="Doc_Change_Password"),
    path('logout',Logout,name="logout"),
    path('pat_history',Pat_History,name="pat_history"),
    path('view_patient',View_Patient,name="view_patient"),
    path('view_rs_patient',View_rs_Patient,name="view_rs_patient"),
    path('add_patient',add_patient,name="add_patient"),
    path('edit_patient(<int:pid>)',Edit_patient,name="edit_patient"),
    path('detail_patient(<int:pid>)',Patient_Detail,name="detail_patient"),
    path('view_doctor',View_Doctor,name="view_doctor"),
    path('view_receptionist',View_Res,name="view_receptionist"),
    path('new_appointment',New_Appointment,name="new_appointment"),
    path('done_appointment',Done_Appointment,name="done_appointment"),
    path('patient_invoice',Patient_Invoice,name="patient_invoice"),
    path('all_appointment',All_Appointment,name="all_appointment"),
    path('create_appointment',Create_Appointment,name="create_appointment"),
    path('doctor_accounting',Doctor_Accouting,name="doctor_accounting"),
    path('patient_accounting',Patient_Accouting,name="patient_accounting"),
    path('add_attendance',Add_Attendance,name="add_attendance"),
    path('view_attendance(<int:pid>)',View_Attendance,name="view_attendance"),
    path('get_invoice/<int:book_id>', get2, name="get_invoice"),
    path('get_invoice1/<int:book_id>', get3, name="get_invoice1"),
    path('next_payment(<int:pid>)',Next_Payment,name="next_payment"),
    path('assign_status(<int:pid>)',Assign_Status,name="assign_status"),
    path('edit_status(<int:pid>)',Edit_Status,name="edit_status"),
    path('delete_patient(<int:pid>)',delete_patient,name="delete_patient"),
    path('delete_attendance(<int:pid>)',delete_attendance,name="delete_attendance"),
    path('delete_resc(<int:pid>)',delete_resc,name="delete_resc"),
    path('delete_appointment(<int:pid>)',delete_appointment,name="delete_appointment"),
    path('delete_pat_appointment(<int:pid>)',delete_pat_appointment,name="delete_pat_appointment"),
    path('delete_doctor(<int:pid>)',delete_doctor,name="delete_doctor"),
    path('presbetweendate_reportdetails',presbetweendate_reportdetails, name='presbetweendate_reportdetails'),
    path('presbetweendate_report',presbetweendate_report, name='presbetweendate_report'),
    path('appbetweendate_reportdetails',appbetweendate_reportdetails, name='appbetweendate_reportdetails'),
    path('appbetweendate_report',appbetweendate_report, name='appbetweendate_report'),
    path('delete_prescription(<int:pid>)',delete_prescription,name="delete_prescription"),
    path('viewdoc_appoint(<int:pid>)',viewdoc_appoint,name="viewdoc_appoint"),
    path('send_feedback(<int:pid>)', Feedback, name='send_feedback'),
    path('view_feedback', View_feedback, name='view_feedback'),
path('delete_feedback(<int:pid>)', delete_feedback, name='delete_feedback'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)