from enum import unique
import os
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import ForeignKey
from config import db
from sqlalchemy.orm import relationship

# current_dir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)


#
class Doctor(db.Model):
    doctor_id = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    dept_id = db.Column(db.Integer,ForeignKey('department.dept_id'),nullable=False)
    doctor_name = db.Column(db.String(25),nullable=False)
    gender = db.Column(db.String(1),nullable=False)
    dob = db.Column(db.Date,nullable=False)
    experience = db.Column(db.Integer)
    contact_number = db.Column(db.BigInteger,unique=True,nullable=False)
    doctor_email = db.Column(db.String(25),unique=True,nullable=False)
    room_no = db.Column(db.Integer,unique=True,nullable=False)
    doctor_username = db.Column(db.String(25),unique=True,nullable=False)
    doctor_password = db.Column(db.String(25),nullable=False)
    dept = relationship("department",back_populates="doctors")
    #doc = relationship("Consultation",back_populates="consulting_doctor")
    docToConsultant = relationship("Consultation",back_populates="doc_part")
    


    def __init__(self,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11):
        self.dept_id = p2
        self.doctor_name = p3
        self.gender = p4
        self.dob = p5
        self.experience = p6
        self.contact_number = p7
        self.doctor_email = p8
        self.room_no = p9
        self.doctor_username = p10
        self.doctor_password = p11


class department(db.Model):
    dept_id = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    dept_name = db.Column(db.String(25),unique=True,nullable=False)
    block_name = db.Column(db.String(1),unique=True,nullable=False)
    block_contact = db.Column(db.String(10),unique=True,nullable=False)
    doctors = relationship("Doctor",back_populates="dept")

    def __init__(self,p2,p3,p4):
        self.dept_name=p2
        self.block_name=p3
        self.block_contact=p4


class Patient(db.Model):
    patient_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    patient_name=db.Column(db.String(25),nullable=False)
    patient_gender=db.Column(db.String(1),nullable=False)
    patient_contact = db.Column(db.BigInteger,unique=True,nullable=False)
    patient_email = db.Column(db.String(25),unique=True,nullable=False)
    patient_dob = db.Column(db.Date,nullable=False)
    patient_username = db.Column(db.String(25),unique=True,nullable=False)
    patient_password = db.Column(db.String(25),nullable=False)
    #pat = relationship("Consultation",back_populates="consulting_patient")
    patToConsultant=relationship("Consultation",back_populates="pat_part")
    def __init__(self,p2,p3,p4,p5,p6,p7,p8):
        self.patient_name=p2
        self.patient_gender=p3
        self.patient_contact = p4
        self.patient_email = p5
        self.patient_dob =p6
        self.patient_username =p7
        self.patient_password = p8

class Appointment(db.Model):
    app_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    doctor_id = db.Column(db.Integer,ForeignKey(Doctor.doctor_id),nullable=False)
    patient_id = db.Column(db.Integer,ForeignKey(Patient.patient_id),nullable=False)
    app_date=  db.Column(db.Date,nullable=False)
    referred_by=db.Column(db.Integer,nullable=True)
    problem=db.Column(db.String(100),nullable=False)
    remarks=db.Column(db.String(100),nullable=True)

    def __init__(self,p2,p3,p4,p5,p6,p7):
        self.doctor_id=p2
        self.patient_id=p3
        self.app_date=p4
        self.referred_by=p5
        self.problem=p6
        self.remarks=p7

class Consultation(db.Model):
    con_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False,unique=True)
    con_type=db.Column(db.String(3),nullable=False)
    doctor_id = db.Column(db.Integer,ForeignKey(Doctor.doctor_id),nullable=False)
    patient_id = db.Column(db.Integer,ForeignKey(Patient.patient_id),nullable=False)
    in_date = db.Column(db.Date,nullable=False)
    out_date= db.Column(db.Date,nullable=True)
    problem= db.Column(db.String(100),nullable=False)
    prescription= db.Column(db.String(100),nullable=True)
    follow_up_doctor=db.Column(db.Integer,nullable=True)
    remarks=db.Column(db.String(100),nullable=True)
    #consulting_doctor = relationship("Doctor",back_populates="doc")
    #consulting_patient = relationship("Patient",back_populates="pat")
    doc_part=relationship("Doctor",back_populates="docToConsultant")
    pat_part=relationship("Patient",back_populates="patToConsultant")

    

    def __init__(self,p2,p3,p4,p5,p6,p7,p8,p9,p10):
        self.con_type=p2
        self.doctor_id=p3
        self.patient_id=p4
        self.in_date=p5
        self.out_date=p6
        self.problem=p7
        self.prescription=p8
        self.follow_up_doctor=p9
        self.remarks=p10
db.create_all()