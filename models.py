from email.policy import default
from enum import unique
from logging import NullHandler
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import cast, String
from sqlalchemy import or_, func
from passlib.hash import sha256_crypt
from datetime import datetime

from sqlalchemy.orm import backref


db = SQLAlchemy()


class admins(db.Model):
    __tablename__ = 'admins'
    national_id = db.Column(db.Integer, primary_key=True,
                            nullable=False, unique=True)
    staff_id = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    other_names = db.Column(db.String)
    phone_number = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    gender = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    def __init__(self, national_id, staff_id, other_names, phone_number, role, username, password, email, first_name, last_name, gender):
        self.username = username
        self.staff_id = staff_id
        self.national_id = national_id
        self.password = sha256_crypt.encrypt(password)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.phone_number = phone_number
        self.other_names = other_names
        self.role = role

    def serialize(self):
        return {
            'username': self.username,
            'staff_id': self.staff_id,
            'national_id': self.national_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'phone_number': self.phone_number,
            'other_names': self.other_names,
            'role': self.role
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class cowsinfo(db.Model):
    __tablename__ = 'cowsinfo'
    cow_tag_id = db.Column(db.String, primary_key=True, nullable=False)
    cow_breed = db.Column(db.String, nullable=False)
    cow_gender = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.String, nullable=False)
    admin_national_id = db.Column(db.Integer, db.ForeignKey(
        'admins.national_id'), nullable=False)
    weight = db.Column(db.String, nullable=False)
    cow_image = db.Column(db.String, nullable=False)
    cow_status = db.Column(db.Boolean, default=True, nullable=False)
    cow_price = db.Column(db.Integer, nullable=True)
    admins = db.relationship('admins', backref=db.backref(
        'cowsinfo', cascade='all,delete,delete'))
    meat = db.Column(db.Boolean, default=True, nullable=False)
    milk = db.Column(db.Boolean, default=False, nullable=False)
    pregnant = db.Column(db.Boolean, default=False, nullable=False)
    sold = db.Column(db.Boolean, default=False)

    def __init__(self, cow_tag_id, cow_breed, cow_gender, cow_status, cow_price, cow_image, weight, admin_national_id, date_of_birth, meat, milk, pregnant, sold):
        self.cow_tag_id = cow_tag_id
        self.cow_status = cow_status
        self.cow_breed = cow_breed
        self.cow_price = cow_price
        self.weight = weight
        self.sold = sold
        self.cow_gender = cow_gender
        self.admin_national_id = admin_national_id
        self.date_of_birth = date_of_birth
        self.cow_image = cow_image
        self.meat = meat
        self.milk = milk
        self.pregnant = pregnant

    def serialize(self):
        return {
            'cow_tag_id': self.cow_tag_id,
            'cow_status': self.cow_status,
            'cow_breed': self.cow_breed,
            'cow_price': self.cow_price,
            'weight': self.weight,
            'cow_gender': self.cow_gender,
            'admin_national_id': self.admin_national_id,
            'date_of_birth': self.date_of_birth,
            'cow_image': self.cow_image
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class Approval(db.Model):
    __tablename__ = 'approvals'
    appproval_id = db.Column(db.String, primary_key=True, nullable=False)
    cow_tag_id = db.Column(db.String, nullable=False)
    cow_breed = db.Column(db.String, nullable=False)
    cow_gender = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.String, nullable=False)
    admin_national_id = db.Column(db.Integer, db.ForeignKey(
        'admins.national_id'), nullable=True)
    weight = db.Column(db.String, nullable=False)
    cow_image = db.Column(db.String, nullable=False)
    cow_status = db.Column(db.Boolean, default=True, nullable=False)
    cow_price = db.Column(db.Integer, nullable=True)
    admins = db.relationship('admins', backref=db.backref(
        'Approval', cascade='all,delete,delete'))
    meat = db.Column(db.Boolean, default=True, nullable=False)
    milk = db.Column(db.Boolean, default=False, nullable=False)
    pregnant = db.Column(db.Boolean, default=False, nullable=False)
    sold = db.Column(db.Boolean, default=False)
    farmer_id = db.Column(db.String, nullable=True)
    transaction_code = db.Column(db.String, nullable=True)

    def __init__(self, approval_id, farmer_id, transaction_code, cow_tag_id, cow_breed, cow_gender, cow_status, cow_price, cow_image, weight, admin_national_id, date_of_birth, meat, milk, pregnant, sold):
        self.appproval_id = approval_id
        self.transaction_code = transaction_code
        self.farmer_id = farmer_id
        self.cow_tag_id = cow_tag_id
        self.cow_status = cow_status
        self.cow_breed = cow_breed
        self.cow_price = cow_price
        self.weight = weight
        self.sold = sold
        self.cow_gender = cow_gender
        self.admin_national_id = admin_national_id
        self.date_of_birth = date_of_birth
        self.cow_image = cow_image
        self.meat = meat
        self.milk = milk
        self.pregnant = pregnant

    def save(self):
        db.session.add(self)
        db.session.commit()


class farmers(db.Model):
    __tablename__ = 'farmers'
    farmer_national_id = db.Column(
        db.String, primary_key=True, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    other_names = db.Column(db.String)
    phone_number = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    gender = db.Column(db.String, nullable=False)

    def __init__(self, farmer_national_id, other_names, phone_number, username, password, email, first_name, last_name, gender):
        self.username = username

        self.farmer_national_id = farmer_national_id
        self.password = sha256_crypt.encrypt(password)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.phone_number = phone_number
        self.other_names = other_names

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            'username': self.username,
            'farmer_national_id': self.farmer_national_id,
            'email': self.email,
            'first_name': self.first_name,
            'first_name': self.last_name,
            'gender': self.gender,
            'phone_number': self.phone_number,
            'other_names': self.other_names
        }


class verify(db.Model):
    __tablename__ = 'verify'
    farmer_national_id = db.Column(
        db.String, primary_key=True, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    other_names = db.Column(db.String)
    phone_number = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    gender = db.Column(db.String, nullable=False)

    def __init__(self, farmer_national_id, other_names, phone_number, username, email, first_name, last_name, gender, password=password):
        self.username = username

        self.farmer_national_id = farmer_national_id
        self.email = email
        self.first_name = first_name
        self.password = sha256_crypt.encrypt(password)
        self.last_name = last_name
        self.gender = gender
        self.phone_number = phone_number
        self.other_names = other_names

    def save(self):
        db.session.add(self)
        db.session.commit()


class milk_sale(db.Model):
    __tablename__ = "milk_sale"
    milk_sale_id = db.Column(db.String, primary_key=True)
    admin_national_id = db.Column(db.Integer, db.ForeignKey(
        'admins.national_id'), nullable=True)
    admins = db.relationship('admins', backref=db.backref(
        'milk_sale', cascade='all,delete,delete'))
    milk_quantity = db.Column(db.Float, nullable=False)
    milk_price = db.Column(db.Float, nullable=False)
    farmer_phone_number = db.Column(db.String, nullable=False)
    farmer_national_id = db.Column(db.String, nullable=False)
    transaction_code = db.Column(db.String,  nullable=False)
    milk_sale_date = db.Column(db.String, nullable=False)

    def __init__(self, milk_sale_id, milk_quantity, milk_price, transaction_code, milk_sale_date, admin_national_id, farmer_phone_number, farmer_national_id):
        self.milk_sale_id = milk_sale_id
        self.milk_quantity = milk_quantity
        self.milk_price = milk_price
        self.transaction_code = transaction_code
        self.cow_tag_id = milk_price
        self.milk_sale_date = milk_sale_date
        self.admin_national_id = admin_national_id
        self.farmer_national_id = farmer_national_id
        self.farmer_phone_number = farmer_phone_number

    def save(self):
        db.session.add(self)
        db.session.commit()


class milk_collection(db.Model):
    __tablename__ = "milk_collection"
    milk_collection_id = db.Column(db.String, primary_key=True)
    milk_quality = db.Column(db.String, nullable=False)
    admin_national_id = db.Column(db.Integer, db.ForeignKey(
        'admins.national_id'), nullable=False)
    admins = db.relationship('admins', backref=db.backref(
        'milk_collection', cascade='all,delete,delete'))
    milk_quantity = db.Column(db.Float, nullable=False)
    cow_tag_id = db.Column(db.String, db.ForeignKey(
        'cowsinfo.cow_tag_id'), nullable=False)
    cowsinfo = db.relationship('cowsinfo', backref=db.backref(
        'milk_collection', cascade='all,delete,delete'))
    milk_collection_time = db.Column(db.String, nullable=False)
    milk_collection_date = db.Column(db.String, nullable=False)
    milking_personel = db.Column(
        db.String, db.ForeignKey('staff.staff_id'), nullable=True)
    staff = db.relationship('staff', backref=db.backref(
        'milk_collection', cascade='all,delete,delete'))

    def __init__(self, milk_collection_id, milk_quality, milking_personel, milk_collection_date, milk_quantity, milk_collection_time, admin_national_id, cow_tag_id):
        self.milk_collection_id = milk_collection_id
        self.milking_personel = milking_personel
        self.milk_quality = milk_quality
        self.milk_collection_date = milk_collection_date
        self.milk_quantity = milk_quantity
        self.cow_tag_id = cow_tag_id
        self.milk_collection_time = milk_collection_time
        self.admin_national_id = admin_national_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class inseminations(db.Model):
    __tablename__ = 'inseminations'
    insem_id = db.Column(db.String, primary_key=True, nullable=False)
    cow_tag_id = db.Column(db.String, db.ForeignKey(
        'cowsinfo.cow_tag_id'), nullable=False)
    date_of_insemination = db.Column(db.String, nullable=False)
    admin_national_id = db.Column(db.Integer, db.ForeignKey(
        'admins.national_id'), nullable=False)
    breed = db.Column(db.String, nullable=False)
    sperm_dose = db.Column(db.Integer, nullable=False)
    insemination_officer = db.Column(db.String, nullable=False)
    insemination_officer_id = db.Column(db.Integer, nullable=False)
    insemination_officer_contact = db.Column(db.String, nullable=False)
    no_of_inseminations = db.Column(db.Integer, nullable=False)
    age_at_insemination = db.Column(db.Integer, nullable=False)

    def __init__(self, insem_id, cow_tag_id, date_of_insemination, admin_national_id, breed, insemination_officer_contact, sperm_dose, insemination_officer, no_of_inseminations, insemination_officer_id, age_at_insemination):
        self.insem_id = insem_id
        self.cow_tag_id = cow_tag_id
        self.date_of_insemination = date_of_insemination
        self.admin_national_id = admin_national_id
        self.breed = breed
        self.sperm_dose = sperm_dose
        self.insemination_officer = insemination_officer
        self.insemination_officer_contact = insemination_officer_contact
        self.no_of_inseminations = no_of_inseminations
        self.insemination_officer_id = insemination_officer_id
        self.age_at_insemination = age_at_insemination

    def save(self):
        db.session.add(self)
        db.session.commit()


class cowscategory(db.Model):
    __tablename__ = 'cowscategory'
    category_id = db.Column(db.String, primary_key=True, nullable=False)
    breed = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    admin_national_id = db.Column(db.Integer, db.ForeignKey(
        'admins.national_id'), nullable=False)
    breed_id = db.Column(db.String, nullable=False, unique=True)
    sex = db.Column(db.String, nullable=False)

    def __init__(self, category_id, breed, description, admin_national_id, breed_id, sex):
        self.category_id = category_id
        self.breed = breed
        self.sex = sex,
        self.description = description
        self.admin_national_id = admin_national_id
        self.breed_id = breed_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class cowfeedinventory(db.Model):
    __tablename__ = 'cowfeedinventory'
    feed_id = db.Column(db.String, primary_key=True, nullable=False)
    food_name = db.Column(db.String, unique=True, nullable=False)
    type_of_food = db.Column(db.String, unique=True, nullable=False)
    feed_quantity = db.Column(db.String, nullable=False)
    supplier_name = db.Column(db.String, nullable=False)
    supplier_contact = db.Column(db.String, nullable=False)
    date_in = db.Column(db.String, nullable=False)
    admin_national_id = db.Column(db.Integer, db.ForeignKey(
        'admins.national_id'), nullable=False)
    admins = db.relationship, backref = db.backref(
        'cowfeedinventory', cascade='all,delete,delete')

    def __init__(self, feed_id, food_name, date_in, type_of_food, feed_quantity, supplier_name, admin_national_id, supplier_contact):
        self.feed_id = feed_id
        self.date_in = date_in
        self.food_name = food_name
        self.type_of_food = type_of_food
        self.feed_quantity = feed_quantity
        self.supplier_name = supplier_name

        self.supplier_contact = supplier_contact
        self.admin_national_id = admin_national_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class cowfeeds(db.Model):
    __tablename__ = 'cowfeeds'
    cow_feed_id = db.Column(db.String, primary_key=True, nullable=False)
    cow_tag_id = db.Column(db.String, db.ForeignKey(
        'cowsinfo.cow_tag_id'), nullable=False)
    type_of_food = db.Column(db.String, db.ForeignKey(
        'cowfeedinventory.type_of_food'), nullable=False)
    food_name = db.Column(db.String, db.ForeignKey(
        'cowfeedinventory.food_name'), nullable=False)
    quantity_given = db.Column(db.String, nullable=False)
    time_of_feeding = db.Column(db.String, nullable=False)
    feeding_personel_id = db.Column(db.String, nullable=False)
    admin_national_id = db.Column(db.Integer, db.ForeignKey(
        'admins.national_id'), nullable=False)
    admins = db.relationship, backref = db.backref(
        'cowfeeds', cascade='all,delete,delete')
    cowsinfo = db.relationship, backref = db.backref(
        'cowfeeds', cascade='all,delete,delete')
    cowfeedinventory = db.relationship, backref = db.backref(
        'cowfeeds', cascade='all,delete,delete')
    date_of_feeding = db.Column(db.String, nullable=False)

    def __init__(self, cow_feed_id, type_of_food, date_of_feeding, food_name, quantity_given, time_of_feeding, cow_tag_id, admin_national_id, feeding_personnel_id):
        self.cow_feed_id = cow_feed_id
        self.date_of_feeding = date_of_feeding
        self.food_name = food_name
        self.type_of_food = type_of_food
        self.quantity_given = quantity_given
        self.time_of_feeding = time_of_feeding
        self.cow_tag_id = cow_tag_id
        self.admin_national_id = admin_national_id
        self.feeding_personel_id = feeding_personnel_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class vaccineinventories(db.Model):
    __tablename__ = 'vaccineinventories'
    vaccine_name = db.Column(db.String, primary_key=True, nullable=False)
    disease_treated = db.Column(db.String, nullable=False)
    available_vaccine_quantity = db.Column(db.Integer, nullable=False)
    date_in = db.Column(db.String, nullable=False,)
    supplier_name = db.Column(db.String, nullable=False)
    supplier_contact = db.Column(db.Integer, nullable=False)
    admin_national_id = db.Column(db.Integer, db.ForeignKey(
        'admins.national_id'), nullable=False)
    admins = db.relationship, backref = db.backref(
        'vaccineinventories', cascade='all,delete,delete')

    def __init__(self, vaccine_name, supplier_contact, disease_treated, available_vaccine_quantity, date_in, supplier_name, admin_national_id):
        self.vaccine_name = vaccine_name
        self.supplier_contact = supplier_contact
        self.disease_treated = disease_treated
        self.admin_national_id = admin_national_id
        self.available_vaccine_quantity = available_vaccine_quantity
        self.date_in = date_in
        self.supplier_name = supplier_name

    def save(self):
        db.session.add(self)
        db.session.commit()


class healthinfo(db.Model):
    __tablename__ = 'healthinfo'
    healthinfo_id = db.Column(db.String, primary_key=True, nullable=False)
    cow_tag_id = db.Column(db.String, db.ForeignKey(
        'cowsinfo.cow_tag_id'), nullable=False)
    vaccine_name = db.Column(db.String, db.ForeignKey(
        'vaccineinventories.vaccine_name'), nullable=False)
    date_of_vaccination = db.Column(db.String, nullable=False)
    vet_id = db.Column(db.String, nullable=False)
    vet_name = db.Column(db.String, nullable=False)
    admin_national_id = db.Column(db.Integer, db.ForeignKey(
        'admins.national_id'), nullable=False)
    weight = db.Column(db.String, nullable=False)
    prescription = db.Column(db.String, nullable=False)
    disease_treated = db.Column(db.String, nullable=False)
    treatment_duration = db.Column(db.String, nullable=False)
    admins = db.relationship, backref = db.backref(
        'healthinfo', cascade='all,delete,delete')
    cowsinfo = db.relationship, backref = db.backref(
        'healthinfo', cascade='all,delete,delete')

    def __init__(self, healthinfo_id, vaccine_name, cow_tag_id, date_of_vaccination, disease_treated, weight, prescription, treatment_duration, vet_name, vet_id, admin_national_id):
        self.healthinfo_id = healthinfo_id
        self.cow_tag_id = cow_tag_id
        self.vaccine_name = vaccine_name
        self.date_of_vaccination = date_of_vaccination
        self.vet_id = vet_id
        self.vet_name = vet_name
        self.admin_national_id = admin_national_id
        self.weight = weight
        self.prescription = prescription
        self.treatment_duration = treatment_duration
        self.disease_treated = disease_treated

    def save(self):
        db.session.add(self)
        db.session.commit()


class transactions(db.Model):
    transaction_code = db.Column(db.String, primary_key=True)
    phone_number = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)

    def __init__(self, transaction_code, phone_number, amount, date):
        self.transaction_code = transaction_code
        self.phone_number = phone_number
        self.amount = amount
        self.date = date

    def save(self):
        db.session.add(self)
        db.session.commit()


class calvings(db.Model):
    __tablename__ = 'calvings'
    calving_id = db.Column(db.String, primary_key=True,
                           nullable=False, unique=True)
    gender = db.Column(db.String, nullable=False)
    breed = db.Column(db.String, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    anomalies = db.Column(db.String, default=None, nullable=False)
    date_of_birth = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    time_of_birth = db.Column(db.String, nullable=False)
    admin_national_id = db.Column(db.Integer, db.ForeignKey(
        'admins.national_id'), nullable=False)
    cow_tag_id = db.Column(db.String, unique=True, nullable=False)
    admins = db.relationship, backref = db.backref(
        'calvings', cascade='all,delete,delete')

    def __init__(self, time_of_birth, weight, gender, image, breed, calving_id, anomalies, date_of_birth, cow_tag_id, admin_national_id):
        self.time_of_birth = time_of_birth
        self.weight = weight
        self.gender = gender
        self.image = image
        self.breed = breed
        self.calving_id = calving_id
        self.anomalies = anomalies
        self.date_of_birth = date_of_birth
        self.cow_tag_id = cow_tag_id
        self.admin_national_id = admin_national_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class deathrecords(db.Model):
    __tablename__ = 'deathrecords'
    cow_tag_id = db.Column(db.String, unique=True, nullable=False)
    cause_of_death = db.Column(db.String, nullable=False)
    date_of_death = db.Column(db.String, nullable=False)
    admin_national_id = db.Column(db.Integer, db.ForeignKey(
        'admins.national_id'), nullable=False)
    death_record_id = db.Column(db.String, primary_key=True, nullable=False)

    def __init__(self, cow_tag_id, cause_of_death, date_of_death, admin_national_id, death_record_id):
        self.cow_tag_id = cow_tag_id
        self.cause_of_death = cause_of_death
        self.date_of_death = date_of_death
        self.admin_national_id = admin_national_id
        self.death_record_id = death_record_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.String, nullable=False, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    other_name = db.Column(db.String, nullable=False)
    national_id = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=True)
    role = db.Column(db.String, nullable=True)

    def add(self, first_name, staff_id, role, phone_number, last_name, gender, other_name, national_id):
        self.first_name = first_name
        self.staff_id = staff_id
        self.phone_number = phone_number
        self.gender = gender
        self.role = role
        self.last_name = last_name
        self.other_name = other_name
        self.national_id = national_id

    def serialize(self):
        return {
            'staff_id': self.staff_id,
            'national_id': self.national_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'phone_number': self.phone_number,
            'other_name': self.other_name,
            'role': self.role
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class cow_sales(db.Model):
    __tablename__ = "cow_sales"
    cow_tag_id = db.Column(db.String, primary_key=True)
    admin_national_id = db.Column(db.Integer, db.ForeignKey(
        'admins.national_id'), nullable=True)
    admins = db.relationship, backref = db.backref(
        "cow_sales", cascade='all,delete,delete')
    cow_price = db.Column(db.Integer, nullable=False)
    farmer_phone_number = db.Column(db.String, nullable=False)
    farmer_national_id = db.Column(db.String, nullable=False)
    transaction_code = db.Column(db.String, nullable=False)
    cow_sale_date = db.Column(db.String, nullable=False)

    def __init__(self, cow_tag_id, cow_price, transaction_code, cow_sale_date, admin_national_id, farmer_phone_number, farmer_national_id):
        self.cow_tag_id = cow_tag_id
        self.cow_price = cow_price
        self.transaction_code = transaction_code
        self.cow_sale_date = cow_sale_date
        self.admin_national_id = admin_national_id
        self.farmer_national_id = farmer_national_id
        self.farmer_phone_number = farmer_phone_number

    def save(self):
        db.session.add(self)
        db.session.commit()


class cart_table(db.Model):
    __tablename__ = 'cart_table'
    cart_id = db.Column(db.String, primary_key=True, nullable=False)
    farmer_id = db.Column(db.String, nullable=False)
    cow_tag_id = db.Column(db.String, db.ForeignKey(
        'cowsinfo.cow_tag_id'), nullable=False)
    cow_price = db.Column(db.Integer, nullable=False)
    cow_image = db.Column(db.String, nullable=False)
    cowsinfo = db.relationship, db.backref = backref(
        'cowsinfo', cascade='all,delete,delete')
    transaction_code = db.Column(
        db.String)

    def __init__(self, cart_id, farmer_id, cow_tag_id, cow_price, cow_image, transaction_code):
        self.cart_id = cart_id
        self.cow_tag_id = cow_tag_id
        self.farmer_id = farmer_id
        self.cow_price = cow_price
        self.cow_image = cow_image
        self.transaction_code = transaction_code

    def save(self):
        db.session.add(self)
        db.session.commit()


class milk_total(db.Model):
    __tablename__ = 'milk_total'
    _id = db.Column(db.String, primary_key=True, nullable=False)
    date_of_collection = db.Column(db.String, unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sold_out = db.Column(db.Integer, default=0, nullable=False)
    spoilt = db.Column(db.Integer, default=0, nullable=False)
    carried_foward = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, _id, date_of_collection, quantity, sold_out, spoilt, carried_foward):
        self._id = _id
        self.date_of_collection = date_of_collection
        self.quantity = quantity
        self.sold_out = sold_out
        self.spoilt = spoilt
        self.carried_foward = carried_foward

    def serialize(self):
        return {
            '_id': self._id,
            'date_of_collection': self.date_of_collection,
            'quantity': self.quantity,
            'carried_foward': self.carried_foward
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
