from ast import Str
from cmath import inf
from crypt import methods
import string
from app import app
from models import *
from sqlalchemy.sql import text, and_
from flask import request, flash, render_template, session


@app.route('/search_vaccine_inventory', methods=['GET', 'POST'])
@app.route('/search_vaccine_inventory/page/<int:page>')
def search_vaccine_inventory(page=1):
    if 'admin' in session or 'superadmin' in session:
        if request.method == 'POST':
            if request.form['filter'] == 'other':
                search = request.form['search'].lower()

                info = vaccineinventories.query.filter(or_(str(vaccineinventories.date_in) == search, str(vaccineinventories.supplier_contact) == search, func.lower(vaccineinventories.supplier_name) == search, func.lower(vaccineinventories.disease_treated) == search, func.lower(vaccineinventories.vaccine_name) == search)).order_by(
                    vaccineinventories.date_in.desc()
                ).paginate(page, per_page=1000)
                return render_template('search_templates/vaccineinventory.html', info=info)
            else:
                startdate = request.form['start']
                enddate = request.form['end']
                info = vaccineinventories.query.filter(vaccineinventories.date_in.between(
                    startdate, enddate)).order_by(vaccineinventories.date_in.asc()).paginate(page, per_page=1000)
                return render_template('search_templates/vaccineinventory.html', info=info)
        elif request.method == 'GET':
            info = db.session.query(vaccineinventories).order_by(
                vaccineinventories.date_in.asc()).paginate(page, per_page=10)
            return render_template('search_templates/vaccineinventory.html', info=info)


@app.route('/search_health_info', methods=['GET', 'POST'])
@app.route('/search_health_info/page/<int:page>')
def search_health_info(page=1):
    if 'admin' in session or 'superadmin' in session:
        if request.method == 'POST':
            if request.form['filter'] == 'other':
                search = request.form['search'].lower()

                info = healthinfo.query.filter(or_(func.lower(healthinfo.cow_tag_id) == search, func.lower(healthinfo.disease_treated) == search, func.lower(str(healthinfo.date_of_vaccination)) == search, func.lower(healthinfo.vaccine_name) == search, func.lower(healthinfo.vet_name) == search)).order_by(
                    healthinfo.date_of_vaccination.asc()
                ).paginate(page, per_page=1000)
                return render_template('search_templates/healthinfo.html', info=info)
            else:
                startdate = request.form['start']
                enddate = request.form['end']
                info = healthinfo.query.filter(healthinfo.date_of_vaccination.between(
                    startdate, enddate)).order_by(healthinfo.date_of_vaccination.asc()).paginate(page, per_page=1000)
                return render_template('search_templates/healthinfo.html', info=info)
        elif request.method == 'GET':
            info = db.session.query(healthinfo).order_by(
                healthinfo.date_of_vaccination.asc()).paginate(page, per_page=10)
            return render_template('search_templates/healthinfo.html', info=info)


@app.route('/search_food_inventory', methods=['GET', 'POST'])
@app.route('/search_food_inventory/page/<int:page>')
def search_food_inventory(page=1):
    if 'admin' in session or 'superadmin' in session:
        if request.method == 'POST':
            if request.form['filter'] == 'other':
                search = request.form['search'].lower()

                info = cowfeedinventory.query.filter(or_((cowfeedinventory.supplier_contact) == search, cowfeedinventory.type_of_food == search, func.lower(cowfeedinventory.feed_quantity) == search, func.lower(cowfeedinventory.food_name) == search, func.lower(cowfeedinventory.date_in) == search)).order_by(
                    cowfeedinventory.date_in.asc()
                ).paginate(page, per_page=1000)
                return render_template('search_templates/cowfeedinventory.html', info=info)
            else:
                startdate = request.form['start']
                enddate = request.form['end']
                info = cowfeedinventory.query.filter(cowfeedinventory.date_in.between(
                    startdate, enddate)).order_by(cowfeedinventory.date_in.asc()).paginate(page, per_page=1000)
                return render_template('search_templates/cowfeedinventory.html', info=info)
        elif request.method == 'GET':
            info = db.session.query(cowfeedinventory).order_by(
                cowfeedinventory.date_in).paginate(page, per_page=10)
            return render_template('search_templates/cowfeedinventory.html', info=info)


@app.route('/search_cowfeeds', methods=['GET', 'POST'])
@app.route('/search_cowfeeds/page/<int:page>')
def search_cowfeeds(page=1):
    if 'admin' in session or 'superadmin' in session:
        if request.method == 'POST':
            if request.form['filter'] == 'other':
                search = request.form['search'].lower()

                info = cowfeeds.query.filter(or_(cowfeeds.food_name == search, cowfeeds.type_of_food == search, func.lower(cowfeeds.quantity_given) == search, func.lower(cowfeeds.feeding_personel_id) == search, func.lower(cowfeeds.date_of_feeding) == search, func.lower(cowfeeds.cow_tag_id) == search)).order_by(
                    cowfeeds.date_of_feeding.asc()
                ).paginate(page, per_page=1000)
                return render_template('search_templates/cowfeeds.html', info=info)
            else:
                startdate = request.form['start']
                enddate = request.form['end']
                info = cowfeeds.query.filter(cowfeeds.date_of_feeding.between(
                    startdate, enddate)).order_by(cowfeeds.date_of_feeding.asc()).paginate(page, per_page=1000)
                return render_template('search_templates/cowfeeds.html', info=info)
        elif request.method == 'GET':
            info = db.session.query(cowfeeds).order_by(
                cowfeeds.date_of_feeding).paginate(page, per_page=10)
            return render_template('search_templates/cowfeeds.html', info=info)


@app.route('/search_cows_info', methods=['GET', 'POST'])
@app.route('/search_cows_info/page/<int:page>')
def search_cows_info(page=1):
    if 'admin' in session or 'superadmin' in session:
        if request.method == 'POST':
            if request.form['filter'] == 'other':
                search = request.form['search'].lower()

                info = cowsinfo.query.filter(or_(func.lower(cowsinfo.cow_tag_id) == search, str(cowsinfo.weight) == search, func.lower(cowsinfo.cow_breed) == search, func.lower(cowsinfo.date_of_birth) == search, func.lower(f'{cowsinfo.cow_price}') == search, func.lower(cowsinfo.cow_gender) == search)).order_by(
                    cowsinfo.date_of_birth.asc()
                ).paginate(page, per_page=1000)
                return render_template('search_templates/cowsinfo.html', info=info)
            else:
                startdate = request.form['start']
                enddate = request.form['end']
                info = cowsinfo.query.filter(cowsinfo.date_of_birth.between(
                    startdate, enddate)).order_by(cowsinfo.date_of_birth.asc()).paginate(page, per_page=1000)
                return render_template('search_templates/cowsinfo.html', info=info)
        elif request.method == 'GET':
            info = db.session.query(cowsinfo).order_by(
                cowsinfo.date_of_birth).paginate(page, per_page=10)
            return render_template('search_templates/cowsinfo.html', info=info)


@app.route('/search_inseminations', methods=['GET', 'POST'])
@app.route('/search_inseminations/page/<int:page>')
def search_inseminations(page=1):
    if 'admin' in session or 'superadmin' in session:
        if request.method == 'POST':
            if request.form['filter'] == 'other':
                search = request.form['search'].lower()

                info = inseminations.query.filter(or_(func.lower(inseminations.cow_tag_id) == search, cast(inseminations.age_at_insemination, String) == search, cast(inseminations.no_of_inseminations, String) == search, cast(inseminations.sperm_dose, String) == search, func.lower(inseminations.breed) == search, func.lower(inseminations.insemination_officer) == search, func.lower(inseminations.date_of_insemination) == search, func.lower(f'{inseminations.insemination_officer_contact}') == search)).order_by(
                    inseminations.date_of_insemination.asc()
                ).paginate(page, per_page=1000)
                return render_template('search_templates/inseminations.html', info=info)
            else:
                startdate = request.form['start']
                enddate = request.form['end']
                info = inseminations.query.filter(inseminations.date_of_insemination.between(
                    startdate, enddate)).order_by(inseminations.date_of_insemination.asc()).paginate(page, per_page=1000)
                return render_template('search_templates/inseminations.html', info=info)
        elif request.method == 'GET':
            info = db.session.query(inseminations).order_by(
                inseminations.date_of_insemination).paginate(page, per_page=10)
            return render_template('search_templates/inseminations.html', info=info)


@app.route('/search_calvings', methods=['GET', 'POST'])
@app.route('/search_calvings/page/<int:page>')
def search_calvings(page=1):
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        if request.method == 'POST':
            if request.form['filter'] == 'other':
                search = request.form['search'].lower()
                info = calvings.query.filter(or_(func.lower(calvings.cow_tag_id) == search, func.lower(calvings.gender) == search, func.lower(calvings.anomalies) == search, func.lower(calvings.breed) == search, cast(calvings.weight, String) == search, func.lower(calvings.time_of_birth) == search, func.lower(calvings.date_of_birth) == search)).order_by(
                    calvings.date_of_birth.desc()
                ).paginate(page, per_page=1000)
                return render_template('search_templates/calvings.html', info=info)
            else:
                startdate = request.form['start']
                enddate = request.form['end']
                info = calvings.query.filter(calvings.date_of_birth.between(
                    startdate, enddate)).order_by(calvings.date_of_birth.desc()).paginate(page, per_page=1000)
                return render_template('search_templates/calvings.html', info=info)
        elif request.method == 'GET':
            info = db.session.query(calvings).order_by(
                calvings.date_of_birth.desc()).paginate(page, per_page=10)
            return render_template('search_templates/calvings.html', info=info)


@app.route('/search_death_records', methods=['GET', 'POST'])
@app.route('/search_death_records/page/<int:page>')
def search_death_records(page=1):
    if 'admin' in session or 'superadmin' in session:
        if request.method == 'POST':
            if request.form['filter'] == 'other':
                search = request.form['search'].lower()
                print(search)
                info = deathrecords.query.filter(or_(func.lower(deathrecords.cow_tag_id) == search, func.lower(deathrecords.cause_of_death) == search, func.lower(deathrecords.date_of_death) == search)).order_by(
                    deathrecords.date_of_death.desc()
                ).paginate(page, per_page=1000)
                return render_template('search_templates/deathrecords.html', info=info)
            else:
                startdate = request.form['start']
                enddate = request.form['end']
                info = deathrecords.query.filter(deathrecords.date_of_death.between(
                    startdate, enddate)).order_by(deathrecords.date_of_death.desc()).paginate(page, per_page=1000)
                return render_template('search_templates/deathrecords.html', info=info)
        elif request.method == 'GET':
            info = db.session.query(deathrecords).order_by(
                deathrecords.date_of_death.desc()).paginate(page, per_page=10)
            return render_template('search_templates/deathrecords.html', info=info)


@app.route('/search_milksale', methods=['GET', 'POST'])
@app.route('/search_milksale/page/<int:page>')
def search_milksale(page=1):
    if 'admin' in session or 'superadmin' in session:
        if request.method == 'POST':
            if request.form['filter'] == 'other':
                search = request.form['search'].lower()

                info = milk_sale.query.filter(and_(milk_sale.admin_national_id != None, or_(func.lower(str(milk_sale.farmer_phone_number)) == search, func.lower(milk_sale.transaction_code) == search, func.lower(str(milk_sale.milk_price)) == search, func.lower(str(milk_sale.milk_quantity)) == search))).order_by(
                    milk_sale.milk_sale_date
                ).paginate(page, per_page=1000)
                return render_template('search_templates/milk_sale.html', info=info)
            else:
                startdate = request.form['start']
                enddate = request.form['end']
                info = milk_sale.query.filter(and_(milk_sale.admin_national_id != None, milk_sale.milk_sale_date.between(
                    startdate, enddate))).order_by(milk_sale.milk_sale_date.desc()).paginate(page, per_page=1000)
                return render_template('search_templates/milk_sale.html', info=info)
        else:
            info = db.session.query(milk_sale).filter(milk_sale.admin_national_id != None).order_by(
                milk_sale.milk_sale_date.desc()).paginate(page, per_page=10)
            return render_template('search_templates/milk_sale.html', info=info)


@app.route('/search_milksales', methods=['GET', 'POST'])
@app.route('/search_milksales/page/<int:page>')
def search_milksales(page=1):
    if 'admin' in session or 'superadmin' in session:
        if request.method == 'POST':
            if request.form['filter'] == 'other':
                search = request.form['search'].lower()

                info = milk_sale.query.filter(and_(milk_sale.admin_national_id == None, or_(func.lower(str(milk_sale.farmer_phone_number)) == search, func.lower(milk_sale.transaction_code) == search, func.lower(str(milk_sale.milk_price)) == search, func.lower(str(milk_sale.milk_quantity)) == search))).order_by(
                    milk_sale.milk_sale_date
                ).paginate(page, per_page=1000)
                return render_template('search_templates/milk_sale.html', info=info)
            else:
                startdate = request.form['start']
                enddate = request.form['end']
                info = milk_sale.query.filter(and_(milk_sale.admin_national_id == None, milk_sale.milk_sale_date.between(
                    startdate, enddate))).order_by(milk_sale.milk_sale_date.desc()).paginate(page, per_page=1000)
                return render_template('search_templates/milk_sale.html', info=info)
        else:
            info = db.session.query(milk_sale).filter(milk_sale.admin_national_id == None).order_by(
                milk_sale.milk_sale_date.desc()).paginate(page, per_page=10)
            return render_template('search_templates/milk_sale.html', info=info)


@app.route('/search_milk_collection', methods=['GET', 'POST'])
@app.route('/search_milk_collection/page/<int:page>')
def search_milk_collection(page=1):
    if 'admin' in session or 'superadmin' in session:
        if request.method == 'POST':
            if request.form['filter'] == 'other':
                search = request.form['search'].lower()

                info = milk_collection.query.filter(or_((milk_collection.milk_quality) == search, str(milk_collection.milk_quantity) == search, func.lower((milk_collection.cow_tag_id)) == search, func.lower(milk_collection.milk_collection_date) == search, func.lower(milk_collection.milk_collection_time) == search, func.lower(milk_collection.milking_personel) == search)).order_by(
                    milk_collection.milk_collection_date
                ).paginate(page, per_page=1000)
                return render_template('search_templates/milk_collection.html', info=info)
            else:
                startdate = request.form['start']
                enddate = request.form['end']
                info = milk_collection.query.filter(milk_collection.milk_collection_date.between(
                    startdate, enddate)).order_by(milk_collection.milk_collection_date.desc()).paginate(page, per_page=1000)
                return render_template('search_templates/milk_collection.html', info=info)
        elif request.method == 'GET':
            info = db.session.query(milk_collection).order_by(
                milk_collection.milk_collection_date.desc()).paginate(page, per_page=10)
            return render_template('search_templates/milk_collection.html', info=info)
