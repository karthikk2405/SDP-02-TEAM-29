import datetime
from django.utils.datastructures import MultiValueDictKeyError

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Signup_User

from .models import *
from .utils import render_to_pdf


# Create your views here.
def get2(request,book_id):
    pro = Doctor.objects.get(id=book_id)
    template = get_template('invoice.html')
    data = {
        'pro': pro,
        'book_id':book_id
    }
    html = template.render(data)
    pdf = render_to_pdf('invoice.html',data)
    return HttpResponse(pdf,content_type='application/pdf')

def get3(request,book_id):
    pro = Appointment.objects.get(id=book_id)
    fee = Fee_Patient.objects.get(appoint=pro)
    template = get_template('invoice1.html')
    data = {
        'fee': fee,
        'pro': pro,
        'book_id':book_id
    }
    html = template.render(data)
    pdf = render_to_pdf('invoice1.html',data)
    return HttpResponse(pdf,content_type='application/pdf')

def Home(request):
    return render(request,'carousel.html')

def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')

def Login_User(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = Signup_User.objects.filter(user=user).first()
        if user:
            if sign.reg == "Patient":
                login(request, user)
                error = "pat"
            elif sign.reg == "Doctor":
                login(request, user)
                error = "doc"
        else:
            error = "not"
    d = {'error': error}
    return render(request,'login_user.html',d)


def Login_Admin(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get('uname')
        password = request.POST.get('pwd')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('admin_home')
            else:
                signup_user = Signup_User.objects.filter(user=user).first()
                if signup_user is not None and signup_user.reg == "res":
                    login(request, user)
                    return redirect('res_home')
                else:
                    error = "Invalid user type"
        else:
            error = "Invalid username or password"

    context = {'error': error}
    return render(request, 'login_admin.html', context)


def Signup(request):
    error = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        reg = request.POST.get('reg', 'default_value')
        con = request.POST['contact']
        user = User.objects.create_user(email=e,username=u, password=p, first_name=f,last_name=l)
        sign = Signup_User.objects.create(user=user,mobile=con,image=i,reg=reg)
        if reg == "Doctor":
            status = Doc_Status.objects.get(status="Active")
            pat = Doctor.objects.create(sign=sign,status=status)
        else:
            doc = Patient.objects.create(sign=sign)
        error = True
    d = {'error':error}
    return render(request, 'signup.html',d)

def Signup_Res(request):
    error = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        reg = request.POST['reg']
        con = request.POST['contact']
        user = User.objects.create_user(email=e,username=u, password=p, first_name=f,last_name=l)
        sign = Signup_User.objects.create(user=user,mobile=con,image=i,reg=reg)
    d = {'error':error}
    return render(request, 'add_receptionist.html',d)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    user = User.objects.get(id=request.user.id)
    sign = Signup_User.objects.get(user=user)
    pat = Patient.objects.filter(sign=sign).first()
    d={'sign':sign,'pat':pat,'user':user}
    return render(request,'profile.html',d)

def Patient_Detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    pat = Patient.objects.get(id=pid)
    d={'pat':pat}
    return render(request,'detail_patient.html',d)

def Doctor_profile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    user = User.objects.get(id=request.user.id)
    sign = Signup_User.objects.get(user=user)
    pat = Doctor.objects.get(sign=sign)
    d={'sign':sign,'pat':pat,'user':user}
    return render(request,'doctor_profile.html',d)

def Doctor_detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    pat = Doctor.objects.get(id=pid)
    d={'pat':pat}
    return render(request,'doctor_detail.html',d)

def Edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = False
    user=User.objects.get(id=request.user.id)
    pro = Signup_User.objects.get(user=user)
    pat = Patient.objects.get(sign=pro)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        try:
            fi = request.FILES['img']
            pro.image = fi
            pro.save()
        except:
            pass
        con = request.POST['contact']
        try:
            gen = request.POST['gen']
            pat.gender = gen
            pat.save()
        except:
            pass

        ag = request.POST['age']
        b_gro = request.POST['group']
        add = request.POST['add']
        #pat.gender = gen
        pat.age = ag
        pat.b_group = b_gro
        pat.address = add
        user.email=e
        user.first_name=f
        user.last_name=l
        pro.mobile=con
        pro.save()
        pro.user.save()
        user.save()
        pat.save()
        error = True
    d = {'error':error,'pro':pro,'pat':pat}
    return render(request, 'edit_profile.html',d)

def Edit_doctor_profile(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = False
    user=User.objects.get(id=request.user.id)
    pro = Signup_User.objects.get(user=user)
    pat = Doctor.objects.get(sign=pro)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        try:
            fi = request.FILES['img']
            pro.image = fi
            pro.save()
        except:
            pass
        con = request.POST['contact']
        try:
            gen = request.POST['gen']
            pat.gender = gen
            pat.save()
        except:
            pass
        ag = request.POST['age']
        sp = request.POST['special']
        q = request.POST['qualification']
        add = request.POST['add']
        pat.specialist = sp
        pat.qualification = q
        pat.age = ag

        pat.address = add
        user.email=e
        user.first_name=f
        user.last_name=l
        pro.mobile=con
        pro.save()
        pro.user.save()
        user.save()
        pat.save()
        error = True
    d = {'error':error,'pro':pro,'pat':pat}
    return render(request, 'edit_doctor_profile.html',d)

def Add_Appointment(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = False
    user=User.objects.get(id=request.user.id)
    sign = Signup_User.objects.get(user=user)
    pat = Patient.objects.get(sign=sign)
    doc = Doctor.objects.get(id=pid)
    if request.method == 'POST':
        d = request.POST['d_name']
        n = request.POST['name']
        e = request.POST['email']
        con = request.POST['contact']
        di = request.POST['dis']
        de = request.POST['desc']
        add = request.POST['add']
        pat.address = add
        sign.mobile=con
        user.email=e
        sign.save()
        user.save()
        pat.save()
        status = Status.objects.get(status="pending")
        app = Appointment.objects.create(pat=pat,doc=doc,status=status,desc=de,disease=di)
        error = True
    d = {'error':error,'sign':sign,'pat':pat,'doc':doc}
    return render(request, 'add_appointment.html',d)

def View_Appointment(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    user = User.objects.get(id=request.user.id)
    sign = Signup_User.objects.get(user=user)
    pat = Patient.objects.get(sign=sign)
    appoint = Appointment.objects.filter(pat=pat).all
    d={'appoint':appoint}
    return render(request,'view_appointment.html',d)

def Doctor_View_Appointment(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    user = User.objects.get(id=request.user.id)
    sign = Signup_User.objects.get(user=user)
    pat = Doctor.objects.get(sign=sign)
    status  =Status.objects.get(status="Accept")
    appoint = Appointment.objects.filter(doc=pat,status=status).all
    d={'appoint':appoint}
    return render(request,'doctor_view_appointment.html',d)

def All_Doctor(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    doc = Doctor.objects.all()
    d={'doc':doc}
    return render(request,'all_doctor.html',d)

def Pat_Change_Password(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'change_password1.html',d)

def Hr_Change_Password(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'change_password4.html',d)

def Res_Change_Password(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    error = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'change_password3.html',d)

def Doc_Change_Password(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'change_password2.html',d)

def Add_Prescription(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_user')
    pat1=""
    try:
        pat1 = Patient.objects.get(id=pid)
    except:
        pass
    pat = Patient.objects.all()
    error = False
    if request.method=="POST":
        pa = request.POST['pat']
        d = request.POST['disease']
        p = request.POST['presc']
        user = User.objects.get(username=pa)
        user1 = User.objects.get(id=request.user.id)
        sign1 = Signup_User.objects.get(user=user1)
        sign = Signup_User.objects.get(user=user)
        pa1 = Patient.objects.get(sign=sign)
        pa2 = Doctor.objects.get(sign=sign1)
        Prescription.objects.create(prescription=p,pat=pa1,doc=pa2,disease=d,date1=datetime.date.today())
        error = True
    d = {'error':error,'pat':pat,'pat1':pat1}
    return render(request,'add_prescription.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

def View_Prescription(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    user = User.objects.get(id=request.user.id)
    sign = Signup_User.objects.get(user=user)
    doc = Doctor.objects.get(sign=sign)
    presc = Prescription.objects.filter(doc=doc)
    d={'presc':presc}
    return render(request,'view_prescription.html',d)

def Pat_History(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    user = User.objects.get(id=request.user.id)
    sign = Signup_User.objects.get(user=user)
    doc = Patient.objects.get(sign=sign)
    presc = Prescription.objects.filter(pat=doc)
    d={'presc':presc}
    return render(request,'pat_history.html',d)

def View_Doctor(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    doc = Doctor.objects.all()
    d = {'doc':doc}
    return render(request,'view_doctor.html',d)

def View_Patient(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    doc = Patient.objects.all()
    d = {'pat':doc}
    return render(request,'view_patient.html',d)

def View_rs_Patient(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    doc = Patient.objects.all()
    d = {'pat':doc}
    return render(request,'view_rs_patient.html',d)

def View_Res(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    doc = Signup_User.objects.filter(reg="res").all()
    d = {'res':doc}
    return render(request,'view_receptionist.html',d)

def Admin_Home(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    total_pat=0
    total_active=0
    total_doc=0
    pat = Patient.objects.all()
    doc = Doctor.objects.all()
    for i in pat:
        total_pat+=1

    for i in doc:
        if i.status.status=="Active":
            total_active+=1
        total_doc+=1
    d = {'total_pat':total_pat,'total_doc':total_doc,'total_active':total_active}
    return render(request,'admin_home.html',d)

def Res_Home(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    new=0
    all=0
    done=0
    doc = Appointment.objects.all()
    for i in doc:
        all+=1
        if i.status.status =="Accept":
            done+=1
        if i.status.status =="pending":
            new+=1
    d = {'new':new,'done':done,'all':all}
    return render(request,'res_home.html',d)

def New_Appointment(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    status = Status.objects.get(status = "pending")
    appoint = Appointment.objects.filter(status=status).all
    d={'appoint':appoint}
    return render(request,'new_appointment.html',d)

def Done_Appointment(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    status = Status.objects.get(status = "Accept")
    appoint = Appointment.objects.filter(status=status).all
    d={'appoint':appoint}
    return render(request,'done_appointment.html',d)

def All_Appointment(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    appoint = Appointment.objects.all()
    d={'appoint':appoint}
    return render(request,'all_appointment.html',d)

def Assign_Status(request,pid):
    data = Appointment.objects.get(id=pid)
    status = Status.objects.all()
    error = False
    if request.method=="POST":
        a = request.POST['status']
        t = request.POST['time']
        d = request.POST['date']
        stats = Status.objects.get(status = a)
        data.status = stats
        data.date1 = d
        data.time1 = t
        data.save()
        Fee_Patient.objects.create(appoint = data,total=60000,outstanding=60000,paid=0)
        error = True
    d = {'error':error,'status':status,'data':data}
    return render(request,'assign_status.html',d)

def Edit_Status(request,pid):
    data = Doctor.objects.get(id=pid)
    status = Doc_Status.objects.all()
    error = False
    if request.method=="POST":
        a = request.POST['status']
        i = request.POST['id']
        stats = Doc_Status.objects.get(status = a)
        data.status = stats
        data.save()
        error = True
    d = {'error':error,'status':status,'data':data}
    return render(request,'edit_status.html',d)

def delete_resc(request,pid):
    appoint = Signup_User.objects.get(id=pid)
    appoint.delete()
    return redirect('view_receptionist')

def delete_appointment(request,pid):
    appoint = Appointment.objects.get(id=pid)
    appoint.delete()
    return redirect('all_appointment')

def delete_pat_appointment(request,pid):
    appoint = Appointment.objects.get(id=pid)
    appoint.delete()
    return redirect('view_appointment')

def delete_doctor(request,pid):
    appoint = Doctor.objects.get(id=pid)
    appoint.delete()
    return redirect('view_doctor')

def delete_attendance(request,pid):
    appoint = Attendance.objects.get(id=pid)
    appoint.delete()
    return redirect('view_attendance',appoint.doc.id)

def delete_patient(request,pid):
    appoint = Patient.objects.get(id=pid)
    appoint.delete()
    if not request.user.is_staff:
        return redirect('view_rs_patient')
    else:
        return redirect('view_patient')

def Create_Appointment(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    error = False
    pat = Patient.objects.all()
    doc = Doctor.objects.all()
    status1 = Status.objects.all()
    if request.method == 'POST':
        d = request.POST['d_name']
        n = request.POST['name']
        da = request.POST['date']
        ti = request.POST['time']
        di = request.POST['dis']
        st = request.POST['status']
        status = Status.objects.get(status=st)
        user = User.objects.get(id=d)
        user1 = User.objects.get(id=n)
        sign = Signup_User.objects.get(user=user)
        sign1 = Signup_User.objects.get(user=user1)
        pat1 = Patient.objects.get(sign=sign1)
        doc1 = Doctor.objects.get(sign=sign)
        Appointment.objects.create(time1=ti,date1=da,pat=pat1,doc=doc1,status=status,disease=di)
        error = True
    d = {'error':error,'pat':pat,'doc':doc,'status':status1}
    return render(request, 'create_appointment.html',d)

def add_patient(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    error = False
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        fi = request.FILES['img']
        con = request.POST['contact']
        gen = request.POST['gen']
        ag = request.POST['age']
        b_gro = request.POST['group']
        c_num = request.POST['c_number']
        add = request.POST['add']
        user = User.objects.create_user(username=f,first_name=f,last_name=l,email=e)
        sign = Signup_User.objects.create(user=user,mobile=con,image=fi,reg="Patient")
        pat = Patient.objects.create(sign=sign,address=add,gender=gen,age=ag,b_group=b_gro,c_number=c_num,)
        error = True
    d = {'error':error}
    return render(request, 'add_patient.html',d)

def Edit_patient(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    error = False
    pat = Patient.objects.get(id=pid)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        ag = request.POST['age']
        b_gro = request.POST['group']
        c_num = request.POST['c_number']
        add = request.POST['add']
        user = User.objects.get(username=f)
        sign = Signup_User.objects.get(user=user)
        try:
            fi = request.FILES['img']
            sign.image = fi
            sign.save()
        except:
            pass

        try:
            gen = request.POST['gen']
            pat.gender = gen
            pat.save()
        except:
            pass
        user.first_name=f
        user.last_name=l
        user.email=e
        sign.mobile = con
        pat.c_number=c_num
        pat.b_group=b_gro
        pat.age=ag
        pat.address=add
        pat.save()
        sign.save()
        user.save()
        error = True
    d = {'error':error,'pat':pat}
    return render(request, 'edit_patient.html',d)

def Add_Attendance(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    error = False
    doc1 = Doctor.objects.all()
    if request.method == 'POST':
        f = request.POST['d_name']
        m = request.POST['month']
        y = request.POST['year']
        s = request.POST['salary']
        a = request.POST['attend']
        user = User.objects.get(id=f)
        sign = Signup_User.objects.get(user=user)
        doc = Doctor.objects.get(sign=sign)
        doc.last_date=datetime.date.today()
        doc.last_attend=a
        doc.salary=s
        doc.save()
        Attendance.objects.create(doc=doc,salary=s,month=m,year=y,attend=a)
        error = True
    d = {'error':error,'doc':doc1}
    return render(request, 'add_attendance.html',d)

def Next_Payment(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    error = False
    fee = Fee_Patient.objects.get(id=pid)
    if request.method == 'POST':
        f = request.POST['name']
        n = request.POST['payment']
        t = request.POST['total']
        o = request.POST['outstanding']
        fee.last_date = datetime.date.today()
        fee.total = t
        fee.paid = n
        if fee.outstanding:
            fee.outstanding = int(fee.outstanding) - int(fee.paid)
        else:
            fee.outstanding = int(fee.total) - int(fee.paid)
        fee.save()
        error = True
    d = {'error':error,'fee':fee}
    return render(request, 'next_payment.html',d)

def Doctor_Accouting(request):
    account = Doctor.objects.all()
    d= {'account':account}
    return render(request,'doctor_accounting.html',d)

def Patient_Accouting(request):
    account = Fee_Patient.objects.all()
    d= {'account':account}
    return render(request,'patient_accounting.html',d)

def Patient_Invoice(request):
    user = User.objects.get(id=request.user.id)
    sign = Signup_User.objects.get(user=user)
    pat = Patient.objects.get(sign=sign)
    appoint = Appointment.objects.filter(pat=pat).first()
    account = Fee_Patient.objects.filter(appoint=appoint)
    d= {'account':account}
    return render(request,'patent_invoice.html',d)

def Add_Accounts(request,pid):
    account = Doctor.objects.get(id=pid)
    d= {'account':account}
    return render(request,'doctor_accounting.html',d)

def View_Attendance(request,pid):
    doc = Doctor.objects.get(id=pid)
    attend = Attendance.objects.filter(doc=doc)
    d= {'attend':attend,'doc':doc}
    return render(request,'view_attendance.html',d)

def presbetweendate_reportdetails(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    return render(request, 'presbetweendate_reportdetails.html')



def presbetweendate_report(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        user = User.objects.get(id=request.user.id)
        sign = Signup_User.objects.get(user=user)
        doc = Doctor.objects.get(sign=sign)
        prescription = Prescription.objects.filter(date1__range=[fd,td],doc=doc)
        d = {'prescription':prescription,'fd':fd,'td':td}
        return render(request, 'presbetweendate_reportdetails.html', d)
    return render(request, 'presbetweendate_report.html')


def appbetweendate_reportdetails(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    return render(request, 'appbetweendate_reportdetails.html')



def appbetweendate_report(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']
        user = User.objects.get(id=request.user.id)
        sign = Signup_User.objects.get(user=user)
        doc = Doctor.objects.get(sign=sign)
        appointment = Appointment.objects.filter(date1__range=[fd,td],doc=doc)
        d = {'appointment':appointment,'fd':fd,'td':td}
        return render(request, 'appbetweendate_reportdetails.html', d)
    return render(request, 'appbetweendate_report.html')


def delete_prescription(request,pid):
    prescription = Prescription.objects.get(id=pid)
    prescription.delete()
    return redirect('view_prescription')

def viewdoc_appoint(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    #user = User.objects.get(id=pid)
    #sign = Signup_User.objects.get(user=user)
    doc = Doctor.objects.get(id=pid)
    appointment = Appointment.objects.filter(doc=doc)
    d = {'appointment':appointment,'doc':doc}
    return render(request, 'viewdoc_appoint.html', d)

def View_feedback(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    feed = Send_Feedback.objects.all()
    d = {'feed': feed}
    return render(request, 'view_feedback.html', d)

def delete_feedback(request, pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    feed = Send_Feedback.objects.get(id=pid)
    feed.delete()
    return redirect('view_feedback')

def Feedback(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error = False
    user1 = User.objects.get(id=request.user.id)
    profile = Signup_User.objects.get(user=user1)
    date1 = datetime.date.today()
    user = User.objects.get(id=pid)
    pro = Signup_User.objects.filter(user=user).first()
    if request.method == "POST":
        d = request.POST['date']
        u = request.POST['uname']
        e = request.POST['email']
        con = request.POST['contact']
        m = request.POST['desc']
        user = User.objects.filter(username=u, email=e).first()
        pro = Signup_User.objects.filter(user=user, mobile=con).first()
        Send_Feedback.objects.create(profile=pro, date=d, message1=m)
        error = True
    d = {'pro': pro, 'date1': date1,'error': error}
    return render(request, 'feedback.html', d)
