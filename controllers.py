#from sys import ps2
from re import UNICODE
#from sys import ps2
from config import app,db 
from config import *
from flask import render_template,request,redirect,url_for,session
from models import Appointment, Consultation, department
from models import Doctor
from models import Patient
import datetime


def Date(s):
    s=[int(i) for i in s.split('/')]
    return datetime.date(s[2],s[1],s[0])


#Controller for INDEX 
@app.route('/')
def index():
    return render_template('index.html')

#Controller for DOCTOR LOGIN
@app.route('/loginDoctor',methods=["POST","GET"])
def loginDoctor():
    if request.method == 'GET':
        return render_template('loginDoctor.html')
    elif request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        q=Doctor.query.all()
        for i in q:
            if i.doctor_username == username:
                if i.doctor_password == password:
                 session['user_id']=i.doctor_id
                 return redirect(url_for('doctor',doctor_id=i.doctor_id))
                else:
                    return render_template('loginDoctor.html',password_msg="INVALID PASSWORD !")
        return render_template('loginDoctor.html',user_msg="INVALID USERNAME !")


#Controller for Doctor Dashboard
@app.route('/doctor/<int:doctor_id>',methods=["GET","POST"])
def doctor(doctor_id):
    if session['user_id'] is None:
        return render_template('index.html')
    else:
        D=Doctor.query.filter(Doctor.doctor_id==doctor_id).one()
        return render_template('doctor.html',doctor_id=doctor_id,D=D)

#Controller to View Doctor Appointments
@app.route('/doctor/<int:doctor_id>/viewAppointment',methods=["GET","POST"])
def viewDoctorAppointment(doctor_id):
    if session['user_id'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            app=Appointment.query.filter(Appointment.doctor_id==doctor_id).all()
            P=Patient.query.all()
            D=Doctor.query.all()
            return render_template('viewDoctorAppointment.html',App=app,P=P,D=D,doctor_id=doctor_id)

#Controller to View Patient's of Doctor
@app.route('/doctor/<int:doctor_id>/myPatients',methods=["GET","POST"])
def viewDoctorPatients(doctor_id):
    if session['user_id'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            pat=Consultation.query.filter(Consultation.doctor_id==doctor_id).distinct(Consultation.patient_id).all()
            #pat= db.engine.execute( 'select distinct  P.patient_id,P.patient_name from Consultation C join Patient P on C.patient_id=P.patient_id  where Consultation.doctor_id={{doctor_id}}')
            print(pat)
            return render_template('myPatients.html',doctor_id = doctor_id,P=pat)

    
#Controller to View Patient's Profile by Doctor
@app.route('/doctor/<int:doctor_id>/myPatients/<int:patient_id>',methods=["GET","POST"])
def viewDoctorPatientsProfile(doctor_id,patient_id):
    if session['user_id'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            P=Patient.query.filter(Patient.patient_id == patient_id).one()
            Con = Consultation.query.filter(Consultation.patient_id == patient_id).all()
            return render_template('myPatientProfile.html',P=P,Con=Con,doctor_id=doctor_id)








#Controller to view History
@app.route('/patient/<int:patient_id>/viewHistory',methods=["GET","POST"])
def viewHistory(patient_id):
    if session['user_id'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            Con=Consultation.query.filter(Consultation.patient_id==patient_id).all()
            return render_template("viewHistory.html",Con=Con,patient_id=patient_id)

#Controller to Add Consultation
@app.route('/doctor/<int:doctor_id>/addConsultation/<int:patient_id>/<int:app_id>',methods=["GET","POST"])
def addConsultation(doctor_id,patient_id,app_id):
    if session['user_id'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            D=Doctor.query.all()
            return render_template('addConsultation.html',D=D,doctor_id=doctor_id,patient_id=patient_id,app_id=app_id)
        elif request.method == "POST":
            consult_type=request.form.get('con_type')
            in_date=request.form.get('in_date')
            out_date = request.form.get('out_date')
            problem=request.form.get('problem')
            prescription = request.form.get('prescription')
            follow_up_doctor_id = int(request.form.get('follow_up_doctor'))
            remarks = request.form.get('remarks')
            p2=consult_type
            p3=doctor_id
            p4=patient_id
            p5=in_date
            p6=out_date
            p7=problem
            p8=prescription
            p9=follow_up_doctor_id
            p10=remarks
            object=Consultation(p2,p3,p4,p5,p6,p7,p8,p9,p10)
            db.session.add(object)
            db.session.commit()
            app=Appointment.query.filter(Appointment.app_id==app_id).one()
            db.session.delete(app)
            db.session.commit()
            return redirect(url_for('viewDoctorAppointment',doctor_id=p3))



#Controller for PATIENT LOGIN
@app.route('/loginPatient',methods=["POST","GET"])
def loginPatient():
    if request.method == 'GET':
        return render_template('loginPatient.html')
    elif request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        q=Patient.query.all()
        for i in q:
            if i.patient_username == username:
                if i.patient_password == password:
                 session['user_id']=i.patient_id
                 return redirect(url_for('patient',patient_id=i.patient_id))
                else:
                    return render_template('loginPatient.html',password_msg="INVALID PASSWORD !")
        return render_template('loginPatient.html',user_msg="INVALID USERNAME !")


#Controller for Patient Dashboard
@app.route('/patient/<int:patient_id>',methods=["GET","POST"])
def patient(patient_id):
    if session['user_id'] is None:
        return render_template('index.html')
    else:
        P=Patient.query.filter(Patient.patient_id==patient_id).one()
        if P.patient_gender == 'M':
            return render_template('patient.html',patient_id=patient_id,P=P,ms='Mr ')

            pass
        else:
            return render_template('patient.html',patient_id=patient_id,P=P,ms='Ms ')

#Controller for New Appointment
@app.route('/patient/<int:patient_id>/addAppointment',methods=["GET","POST"])
def addAppointment(patient_id):
    if session['user_id'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            D=Doctor.query.all()
            return render_template('addAppointment.html',patient_id=patient_id,D=D)
        elif request.method == "POST":
            doctor_id=request.form.get('doctor_id')
            app_date=request.form.get('app_date')
            referred_by=int(request.form.get('referred_by'))
            problem=request.form.get('problem')
            remarks=request.form.get('remarks')
            p2=doctor_id
            p3=patient_id
            p4=app_date
            p5=referred_by
            p6=problem
            p7=remarks
            object=Appointment(p2,p3,p4,p5,p6,p7)
            db.session.add(object)
            db.session.commit()            
            return redirect(url_for('patient',patient_id=patient_id))

#Controller to VIEW PATIENT Appointments
@app.route('/patient/<int:patient_id>/viewAppointment',methods=["GET","POST"])
def viewPatientAppointment(patient_id):
    if session['user_id'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            Apt=Appointment.query.filter(Appointment.patient_id==patient_id).all()
            #print(Apt)
            return render_template('viewPatientAppointment.html',Apt=Apt,patient_id=patient_id)



#Controller for ADMIN LOGIN
@app.route('/loginAdmin',methods=["POST","GET"])
def loginAdmin():
    if request.method == 'GET':
        return render_template('loginAdmin.html')
    elif request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if username == 'admin':
            if 'admin' == password:
                session['user_name']= 'admin'
                return redirect(url_for('admin'))
            else:
                return render_template('loginAdmin.html',password_msg="INVALID PASSWORD !")
        return render_template('loginAdmin.html',user_msg="INVALID USERNAME !")


#Controller for ADMIN Dashboard
@app.route('/admin',methods=["GET","POST"])
def admin():
    if session['user_name'] is None:
        return render_template('index.html')
    else:
        return render_template('admin.html')

#Controller to VIEW DOCTORS
@app.route('/admin/doctor',methods=["GET","POST"])
def viewDoctor():
    if session['user_name'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            q=Doctor.query.all()
            return render_template('viewDoctor.html',doc=q)


#Controller to VIEW DEPARTMENTS
@app.route('/admin/department',methods=["GET","POST"])
def viewDepartment():
    if session['user_name'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            dept=department.query.all()
            print(dept)
            return render_template('viewDepartment.html',Dept=dept)

#Controller to VIEW DEPARTMENT PROFILE
@app.route('/admin/department/<int:dept_id>',methods=["GET","POST"])
def viewDepartmentProfile(dept_id):
    if session['user_name'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            d=department.query.filter(department.dept_id == dept_id).one()
            return render_template('viewDepartmentProfile.html',D=d)


#Controller to Doctor Profile View
@app.route('/admin/doctor/<int:doctor_id>',methods=["GET","POST"])
def vieewDoctorProfile(doctor_id):
    if session['user_name'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            q=Doctor.query.filter(Doctor.doctor_id==doctor_id).one()
            return render_template('viewDoctorProfile.html',D=q)


#Controller to View Doctor Profile by Patient
@app.route('/patient/<int:patient_id>/allDoctors/<int:doctor_id>')
def viewAllDoctors(patient_id,doctor_id):
    if session['user_id'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            q=Doctor.query.filter(Doctor.doctor_id==doctor_id).one()
            return render_template('viewAllDoctor.html',patient_id=patient_id,D=q)



#Controller to View Doctor List for Patient
@app.route('/patient/<int:patient_id>/allDoctors')
def allDoctors(patient_id):
    if session['user_id'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            D=Doctor.query.all()
            return render_template('allDoctors.html',doc=D,patient_id=patient_id)




#Controller to Patient Profile View
@app.route('/admin/patient/<int:patient_id>',methods=["GET","POST"])
def vieewPatientProfile(patient_id):
    if session['user_name'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            q=Patient.query.filter(Patient.patient_id==patient_id).one()
            return render_template('viewPatientProfile.html',P=q)


#Controller to Patient History from Admin
@app.route('/admin/patient/<int:patient_id>/viewHistory',methods=["GET","POST"])
def viewPatientProfileHistory(patient_id):
    if session['user_name'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            Con=Consultation.query.filter(Consultation.patient_id==patient_id).all()
            return render_template('adminViewPatientHistory.html',Con=Con,patient_id=patient_id)






#Controller for VIEW PATIENTS
@app.route('/admin/patient',methods=["GET","POST"])
def viewPatient():
    if session['user_name'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
            q=Patient.query.all()
            return render_template('viewPatient.html',pat=q)


#Controller for ADD NEW DOCTOR
@app.route('/admin/doctor/addDoctor',methods=["GET","POST"])
def addDoctor():
    if session['user_name'] is None:
        return render_template('index.html')
    else:
        if request.method=='GET':
            q=department.query.all()
            return render_template('addDoctor.html',dept=q)
        elif request.method == 'POST':
            doctor_name=request.form.get('doctor_name')
            dept_id=request.form.get('dept_id')
            gender=request.form.get('gender')
            dob=request.form.get('dob')
            experience=request.form.get('experience')
            contact_number=int(request.form.get('contact_number'))
            doctor_email=request.form.get('doctor_email')
            room_no=int(request.form.get('room_no'))
            doctor_username=request.form.get('doctor_username')
            doctor_password=request.form.get('doctor_password')
            d=department.query.all()
            print("**********")
            print(doctor_username)
            print(doctor_password)
            print("**********")
            q = Doctor.query.all()       
            if contact_number<1111111111 or contact_number>9999999999 :
                return render_template("addDoctor.html", dept=d,mobile_msg = "MOBILE NUMBER SHOULD BE 10 DIGITS !")
            for i in q:
                if(i.doctor_username == doctor_username):
                    return render_template("addDoctor.html",dept=d, user_msg = "USER ALREADY EXISTS !")
            for i in q:
                if(i.contact_number == contact_number):
                    return render_template("addDoctor.html", dept=d,mobile_msg = "MOBILE NUMBER ALREADY EXISTS !")
            for i in q:
                if(i.doctor_email == doctor_email):
                     return render_template("addDoctor.html", dept=d,email_msg = "EMAIL ID ALREADY EXISTS !")
            
            p2=dept_id
            p3=doctor_name
            p4=gender
            p5=dob
            p6=experience
            p7=contact_number
            p8=doctor_email
            p9=room_no
            p10=doctor_username
            p11=doctor_password
            object=Doctor(p2,p3,p4,p5,p6,p7,p8,p9,p10,p11)
            db.session.add(object)
            db.session.commit()
            return redirect(url_for('viewDoctor'))

#Controller to ADD NEW DEPARTMENT
@app.route('/admin/department/addDepartment',methods=["GET","POST"])
def addDepartment():
    if session['user_name'] is None:
        return render_template('index.html')
    else:
        if request.method == "GET":
                return render_template('addDepartment.html')
        elif request.method == "POST":
            dept_name=request.form.get('dept_name')
            block_name=request.form.get('block_name')
            block_contact=int(request.form.get('block_contact'))
            d=department.query.all()
            print(d)
            if block_contact<1111111111 or block_contact>9999999999 :
                return render_template("addDepartment.html", dept=d,mobile_msg = "MOBILE NUMBER SHOULD BE 10 DIGITS !")
            p2=dept_name
            p3=block_name
            p4=block_contact
            object=department(p2,p3,p4)
            db.session.add(object)
            db.session.commit()
            return redirect(url_for('viewDepartment'))



#Controller for ADD NEW DOCTOR
@app.route('/patient/addPatient',methods=["GET","POST"])
def addPatient():
    if request.method=='GET':
        return render_template('addPatient.html')
    elif request.method == 'POST':
        patient_name=request.form.get('patient_name')
        patient_gender=request.form.get('patient_gender')
        patient_dob=request.form.get('patient_dob')
        patient_contact=int(request.form.get('patient_contact'))
        patient_email=request.form.get('patient_email')
        patient_username=request.form.get('patient_username')
        patient_password=request.form.get('patient_password')
        q = Patient.query.all()       
        if patient_contact<1111111111 or patient_contact>9999999999 :
            return render_template("addPatient.html", mobile_msg = "MOBILE NUMBER SHOULD BE 10 DIGITS !")
        for i in q:
            if(i.patient_username == patient_username):
                return render_template("addPatient.html", user_msg = "USER ALREADY EXISTS !")
        for i in q:
            if(i.patient_contact == patient_contact):
                return render_template("addPatient.html", mobile_msg = "MOBILE NUMBER ALREADY EXISTS !")
        for i in q:
            if(i.patient_email == patient_email):
                return render_template("addPatient.html", email_msg = "EMAIL ID ALREADY EXISTS !")
        p2=patient_name
        p3=patient_gender
        p4=patient_contact
        p5=patient_email
        p6=patient_dob
        p7=patient_username
        p8=patient_password
        object=Patient(p2,p3,p4,p5,p6,p7,p8)
        db.session.add(object)
        db.session.commit()
        return redirect(url_for('loginPatient'))


#Controller for Admin Logout
@app.route('/admin/logout')
def adminLogout():
    session['user_name'] = None
    return redirect(url_for('index'))


#Controller for User Logout
@app.route('/logout')
def userLogout():
    session['user_id'] = None
    return redirect(url_for('index'))



#Controller to change Patient Password
@app.route('/patient/<int:patient_id>/changePassword',methods=["GET","POST"])
def changePatientPassword(patient_id):
    if session['user_id'] is None:
        return render_template('index.html')
    else:
        if request.method == "POST":
            P=Patient.query.filter(Patient.patient_id == patient_id).one()
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            re_password = request.form.get('re-type_password')
            if P.patient_password == old_password:
                if new_password == re_password:
                    P.patient_password = new_password
                    db.session.commit()
                    return redirect(url_for('index'))

                else:
                    return render_template('changePatientPassword.html',msg_re_type_password='RE-TYPE NEW PASSWORD CORRECTLY !',patient_id=P.patient_id)
            else:
                return render_template('changePatientPassword.html',msg_old_password = 'INVALID OLD PASSWORD !',patient_id=P.patient_id)

        elif request.method=="GET":
            return render_template('changePatientPassword.html',patient_id=patient_id)



#Controller to change Doctor Password
@app.route('/doctor/<int:doctor_id>/changePassword',methods=["GET","POST"])
def changeDoctorPassword(doctor_id):
    if session['user_id'] is None:
        return render_template('index.html')
    else:
        if request.method == "POST":
            D=Doctor.query.filter(Doctor.doctor_id == doctor_id).one()
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            re_password = request.form.get('re-type_password')
            if D.doctor_password == old_password:
                if new_password == re_password:
                    D.doctor_password = new_password
                    db.session.commit()
                    return redirect(url_for('index'))

                else:
                    return render_template('changeDoctorPassword.html',msg_re_type_password='RE-TYPE NEW PASSWORD CORRECTLY !',doctor_id=D.doctor_id)
            else:
                return render_template('changeDoctorPassword.html',msg_old_password = 'INVALID OLD PASSWORD !',doctor_id=D.doctor_id)

        elif request.method=="GET":
            return render_template('changeDoctorPassword.html',doctor_id=doctor_id)

