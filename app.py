from flask.helpers import url_for
from werkzeug.utils import redirect, secure_filename
from config import *
from twilio.rest import Client
from datetime import datetime as Date, timedelta
import requests
import uuid
import string
import random
# import pyautogui
from PIL import Image
from reports import *
from search import *
from sqlalchemy import and_
# import netifaces as nif
from manageractions import *
from help import *


def get_mpesa_token():

    consumer_key = "fvGLqUuVGCST6YYD2bGOv4CoosCi7Jvn"
    consumer_secret = 'LewDYO7CdnQhDa1J'
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    # make a get request using python requests liblary
    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))

    # return access_token from response
    return r.json()['access_token']


@app.route("/send_sms")
def sent_sms():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
        to="+254726739857",
        from_="+13185232639",
        body="Hello there!")
    return 'success'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/admin_s', methods=['GET'])
def admin_s():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    user = admins.query.all()
    jsonResp = json.dumps([u.serialize() for u in user])
    return jsonify(jsonResp)


@app.route('/user_s', methods=['GET'])
def user_s():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    user = farmers.query.all()
    jsonResp = json.dumps([u.serialize() for u in user])

    return jsonify(jsonResp)


@app.route('/staff_s', methods=['GET'])
def staff_s():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    staf = staff.query.all()
    jsonResp = json.dumps([u.serialize() for u in staf])

    return jsonify(jsonResp)


@app.route('/signup', methods=['GET', 'POST'])
def signup(page=1):
    if 'user' in session:
        return redirect(url_for('login'))
    elif request.method == 'POST':
        if not request.form['farmer_national_id'] or not request.form['old_password'] or not request.form['password'] or not request.form['confirm_password']:
            flash('please fill all the fields', 'error')
            return render_template('user/verify.html')
        elif not(request.form['password'] == request.form['confirm_password']):
            flash('passwords entered don\'t match')
            return render_template('user/verify.html')
        else:
            farmer = verify.query.filter(
                verify.farmer_national_id == request.form['farmer_national_id']).first()
            if farmer:
                if sha256_crypt.verify(request.form['old_password'], farmer.password):
                    newfarmer = farmers(farmer_national_id=farmer.farmer_national_id, first_name=farmer.first_name, other_names=farmer.other_names, phone_number=farmer.phone_number,
                                        username=farmer.username, email=farmer.email, last_name=farmer.last_name, gender=farmer.gender, password=request.form['password'])
                    newfarmer.save()
                    db.session.delete(farmer)
                    db.session.commit()
                    session['user'] = farmer.username
                    records = db.session.query(milk_sale).filter(milk_sale.farmer_national_id == farmer.farmer_national_id).order_by(
                        milk_sale.milk_sale_date.desc()).paginate(page, per_page=3)

                    return render_template('user/index.html', farmer=farmer, records=records)
                else:
                    flash('wrong one time password', 'error')
                    return render_template('user/verify.html')
            else:
                flash('wrong farmer id', 'error')
                return render_template('user/verify.html')

    return render_template('signup.html', user='user')


@app.route('/manager_login', methods=['GET', 'POST'])
def manager_login():
    if 'manager' in session:
        notifications = Approval.query.count()
        return render_template('superadmin/admindash.html', admin='admin', notifications=notifications)
    if request.method == 'POST':
        if request.form['username'] == 'manager' and request.form['password'] == 'manager123#':
            notifications = Approval.query.count()
            session['manager'] = request.form['username']
            return render_template('superadmin/admindash.html', admin='admin', notifications=notifications)
    return render_template('login.html', user='manager')


@app.route("/login", methods=['GET', 'POST'])
def login(page=1):
    # print(request.environ['HTTP_X_FORWARDED_FOR'])
    if 'user' in session:
        farmer = farmers.query.filter(
            farmers.username == session['user']).first()
        records = db.session.query(milk_sale).filter(milk_sale.farmer_national_id == farmer.farmer_national_id).order_by(
            milk_sale.milk_sale_date.desc()).paginate(page, per_page=3)
        return render_template('user/index.html', farmer=farmer, records=records)

    elif request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            flash('please fill all the fields', 'error')
            return redirect(url_for('login'))
        farmer = farmers.query.filter(
            farmers.username == request.form['username'].capitalize()).first()
        if not farmer:
            flash('user doesn\'t exist', 'error')
            return redirect(url_for('login'))
        elif not sha256_crypt.verify(request.form['password'], farmer.password):
            flash('credentials don\'t match', 'error')
            return redirect(url_for('login'))
        else:

            session['user'] = farmer.username
            detail = farmers.query.filter(
                farmers.username == session['user']).first()
            records = db.session.query(milk_sale).filter(milk_sale.farmer_national_id == detail.farmer_national_id).order_by(
                milk_sale.milk_sale_date.desc()).paginate(page, per_page=3)
            return render_template('user/index.html', farmer=farmer, records=records)
    return render_template('login.html', user='user')


@app.route('/update_farmer_details', methods=['POST', 'GET'])
def update_farmer_details():
    if 'user' in session:
        if request.method == 'POST':
            all_farmmers = farmers.query.all()
            if not request.form['first_name'] or not request.form['last_name'] or not request.form['email_address'] or not request.form['other_names'] or not request.form['phone_number']:
                flash('please fill all the fields', 'error')
                return redirect(url_for('login'))
            for item in all_farmmers:
                if item.username != session['user']:
                    if item.email == request.form['email_address']:
                        flash('please pick a different email address', 'warning')
                        return redirect(url_for('login'))
                    elif item.phone_number == request.form['phone_number']:
                        flash('please pick a different phone number', 'warning')
                        return redirect(url_for('login'))
                    elif item.email == request.form['email_address']:
                        flash('please pick a different email address', 'warning')
                        return redirect(url_for('login'))

            farmer = farmers.query.filter(
                farmers.username == session['user']).first()
            farmer.first_name = request.form['first_name'].capitalize()
            farmer.other_names = request.form['other_names'].capitalize()
            farmer.phone_number = request.form['phone_number']
            farmer.email = request.form['email_address']
            farmer.last_name = request.form['last_name'].capitalize()
            farmer.save()
            flash('successfully updated', 'success')
            return redirect(url_for('login'))
        return redirect(url_for('login'))
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/update_admin_details', methods=['POST', 'GET'])
@app.route('/update_admin_details/page/<int:page>', methods=['POST', 'GET'])
def update_admin_details(page=1):
    const_per_page = 6
    if 'superadmin' in session or 'manager' in session:

        admin1 = admins.query.order_by(
            admins.username.desc()
        ).paginate(page, per_page=const_per_page)
        if request.method == 'POST':
            admin = admins.query.filter(
                admins.national_id == request.form['admin_national_id']).first()
            # admin = admins.query.filter(
            #     admins.username == request.form['username']).first()
            if not request.form['first_name'] or not request.form['last_name'] or not request.form['email_address'] or not request.form['phone_number']:
                flash('please fill all the fields', 'error')
                return redirect(url_for('update_admin_details'))
            else:
                admin.first_name = request.form['first_name'].capitalize()
                # admin.national_id = int(request.form['admin_national_id'])
                admin.other_names = request.form['other_names'].capitalize()
                admin.phone_number = request.form['phone_number']
                admin.email = request.form['email_address']
                admin.last_name = request.form['last_name'].capitalize()
                admin.staff_id = request.form['staff_id']
                admin.save()
                flash('successfully updated ' + admin.username, 'success')
                return redirect(url_for('update_admin_details'))
        return render_template('admins.html', admin=admin1)
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/logout')
def logout():
    if 'admin' in session:
        session.pop('admin', None)
        return redirect(url_for('adminlogin'))
    elif 'user' in session:
        session.pop('user', None)
        return redirect(url_for('login'))
    elif 'superadmin' in session:
        session.pop('superadmin', None)
        return redirect(url_for('superadmin'))
    elif 'manager' in session:
        session.pop('manager', None)
        return redirect(url_for('manager_login'))


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin(page=1):
    if 'admin' in session:
        admin = admins.query.filter(
            admins.username == session['admin']).first()
        cows = cowsinfo.query.order_by(
            cowsinfo.date_of_birth.desc()
        ).paginate(page, per_page=9)
        info1 = db.session.query(healthinfo).order_by(
            healthinfo.date_of_vaccination.desc()).paginate(page, per_page=4)
        info5 = db.session.query(
            vaccineinventories).order_by(vaccineinventories.date_in.asc()).paginate(page, per_page=4)
        info2 = db.session.query(deathrecords).order_by(
            deathrecords.date_of_death.asc()).paginate(page, per_page=3)
        info3 = db.session.query(calvings).order_by(calvings.date_of_birth.desc(
        )).paginate(page, per_page=3)
        info4 = db.session.query(inseminations).order_by(
            inseminations.date_of_insemination.desc()).paginate(page, per_page=3)
        info6 = db.session.query(milk_collection).order_by(
            milk_collection.milk_collection_time.desc()).paginate(page, per_page=4)
        info7 = db.session.query(milk_sale).filter(milk_sale.admin_national_id != None).order_by(
            milk_sale.milk_sale_date.desc()).paginate(page, per_page=4)
        info8 = db.session.query(cowfeedinventory).order_by(
            cowfeedinventory.date_in.desc()).paginate(page, per_page=4)
        info9 = db.session.query(cowfeeds).order_by(
            cowfeeds.date_of_feeding.desc()).paginate(page, per_page=4)
        info10 = db.session.query(milk_sale).filter(milk_sale.admin_national_id == None).order_by(
            milk_sale.milk_sale_date.desc()).paginate(page, per_page=4)

        return render_template('admin/dashboard.html', admin=admin, cow=cows, info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8, info9=info9, info10=info10)

    elif request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            flash('please fill all the fields', 'error')
            return redirect(url_for('adminlogin'))
        admin = admins.query.filter(
            admins.username == request.form['username'].capitalize()).first()
        if not admin:
            flash('admin doesn\'t exist', 'error')
            return redirect(url_for('adminlogin'))
        elif not sha256_crypt.verify(request.form['password'], admin.password):
            flash('credentials don\'t match', 'error')
            return redirect(url_for('adminlogin'))
        else:
            cows = cowsinfo.query.order_by(
                cowsinfo.date_of_birth.desc()
            ).paginate(page, per_page=10)
            info1 = db.session.query(healthinfo).order_by(
                healthinfo.date_of_vaccination.desc()).paginate(page, per_page=10)
            info5 = db.session.query(
                vaccineinventories).order_by(vaccineinventories.date_in.asc()).paginate(page, per_page=10)
            info2 = db.session.query(deathrecords).order_by(
                deathrecords.date_of_death.desc()).paginate(page, per_page=10)
            info3 = db.session.query(calvings).order_by(calvings.date_of_birth.asc(
            )).paginate(page, per_page=10)
            info4 = db.session.query(inseminations).order_by(
                inseminations.date_of_insemination.desc()).paginate(page, per_page=10)
            info6 = db.session.query(milk_collection).order_by(
                milk_collection.milk_collection_time.desc()).paginate(page, per_page=10)
            info7 = db.session.query(milk_sale).filter(milk_sale.admin_national_id != None).order_by(
                milk_sale.milk_sale_date.desc()).paginate(page, per_page=10)
            info8 = db.session.query(cowfeedinventory).order_by(
                cowfeedinventory.date_in.desc()).paginate(page, per_page=10)
            info9 = db.session.query(cowfeeds).order_by(
                cowfeeds.date_of_feeding.desc()).paginate(page, per_page=10)
            info10 = db.session.query(milk_sale).filter(milk_sale.admin_national_id == None).order_by(
                milk_sale.milk_sale_date.desc()).paginate(page, per_page=4)
            dates = str(Date.now()-timedelta(days=1))

            date1 = dates[:4] + '/'+dates[5:7] + '/' + dates[8:10]
            record = milk_total.query.filter(
                milk_total.date_of_collection == date1).first()
            if record:
                if record.quantity > 0:
                    dates1 = str(Date.now())
                    date2 = dates1[:4] + '/'+dates1[5:7] + '/' + dates1[8:10]
                    record1 = milk_total.query.filter(
                        milk_total.date_of_collection == date1).first()
                    newrecorecod = milk_total(_id=uuid.uuid4(
                    ), date_of_collection=date2, carried_foward=record1.quantity, quantity=0, sold_out=0, spoilt=0)
                    newrecorecod.save()
                    record.quantity = 0
                    record.save()
            session['admin'] = admin.username
            return render_template('admin/dashboard.html', admin=admin, cow=cows, info1=info1, info2=info2, info3=info3, info4=info4, info5=info5, info6=info6, info7=info7, info8=info8, info9=info9, info10=info10)
    return render_template('login.html', user='admin')


@app.route('/verify', methods=['GET', 'POST'])
def verifyuser():
    if 'user' in session:
        return redirect(url_for('login'))
    elif request.method == 'POST':
        length = 8

        farmer = farmers.query.filter(
            farmers.farmer_national_id == request.form['farmer_national_id']).first()
        email = farmers.query.filter(
            farmers.email == request.form['email']).first()
        username = farmers.query.filter(
            farmers.username == request.form['username']).first()
        phone = farmers.query.filter(
            farmers.phone_number == request.form['phone_number']).first()
        farmer1 = verify.query.filter(
            verify.farmer_national_id == request.form['farmer_national_id']).first()
        email1 = verify.query.filter(
            verify.email == request.form['email']).first()
        username1 = verify.query.filter(
            verify.username == request.form['username']).first()
        phone1 = verify.query.filter(
            verify.phone_number == request.form['phone_number']).first()
        if farmer or farmer1:
            flash('please pick a different ID number', 'warning')
            return redirect(url_for('signup'))
        elif email or email1:
            flash('please pick a different email address', 'warning')
            return redirect(url_for('signup'))
        elif username or username1:
            flash('please pick a different username', 'warning')
            return redirect(url_for('signup'))
        elif phone or phone1:
            flash('please pick a different phone number', 'warning')
            return redirect(url_for('signup'))
        else:
            one_time_pass = ''.join(random.choices(
                string.ascii_letters+string.digits, k=length))
            msg = Message('Account creation',
                          sender='godwillkisia@noreply.com',
                          recipients=[request.form['email']])
            msg.html = render_template("email.html", user=request.form['username'], farmer_national_id=request.form[
                                       'farmer_national_id'], password=one_time_pass, link=(request.url_root + 'verify'))
            mail.send(msg)
            newfarmer = verify(farmer_national_id=request.form['farmer_national_id'], first_name=request.form['first_name'].capitalize(), other_names=request.form['other_names'].capitalize(), phone_number=request.form[
                               'phone_number'], username=request.form['username'].capitalize(), email=request.form['email'], last_name=request.form['last_name'].capitalize(), gender=request.form['gender'], password=one_time_pass)
            newfarmer.save()
            flash('success please check your email to finish registration', 'success')
            return redirect(url_for('signup'))
    return render_template('user/verify.html', user='user')


@app.route("/adminsignup", methods=["POST", "GET"])
def adminsignup():
    if 'superadmin' in session:

        admin1 = admins.query.all()
        if request.method == "POST":
            if not(request.form['admin_national_id'] or request.form['first_name'].capitalize() or request.form['last_name'].capitalize()
                   or request.form['username'].capitalize() or request.form['confirm_password'] or request.form['email']
                   or request.form['phone_number'] or request.form['staff_id'] or request.form['gender'], request.form['role']):
                flash('please fill all fields', 'error')
                return redirect(url_for('adminsignup'))
            one_time_pass = ''.join(random.choices(
                string.ascii_letters+string.digits, k=8))
            msg = Message('Account creation',
                          sender='godwillkisia@noreply.com',
                          recipients=[request.form['email']])
            msg.html = render_template("email3.html", user=request.form['username'], farmer_national_id=request.form[
                                       'admin_national_id'], password=one_time_pass, link=(request.url_root + 'adminlogin'))
            mail.send(msg)
            newAdmin = admins(national_id=request.form['admin_national_id'], staff_id=request.form['staff_id'], first_name=request.form['first_name'].capitalize(),
                              last_name=request.form['last_name'].capitalize(), other_names=request.form['other_names'].capitalize(), phone_number=request.form['phone_number'], email=request.form['email'], gender=request.form['gender'], username=request.form['username'].capitalize(), password=one_time_pass, role=request.form['role'])
            newAdmin.save()
            flash('successfully saved', 'success')
            return render_template("signup.html", admin=admin1)
        return render_template("signup.html", admin=admin1)
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route("/cowinfo", methods=["POST", "GET"])
def cowinfo():
    rcd = cowscategory.query.filter(
        cowscategory.sex == 'female').all()
    if 'admin' in session:
        if request.method == "POST":

            admin = admins.query.filter(
                admins.username == session['admin']).first()
            print(admin.national_id)
            if not(request.form['cow_tag_id'] or request.form['cow_breed'] or request.form['date_of_birth'] or request.form['weight'] or request.form['gender'] or request.form['weight']):
                flash('enter all required details', 'error')
                return render_template("cowsinfo.html")
            cow = cowsinfo.query.filter(
                cowsinfo.cow_tag_id == request.form['cow_tag_id'].upper()).first()
            cow1 = Approval.query.filter(
                Approval.cow_tag_id == request.form['cow_tag_id'].upper()).first()
            if cow or cow1:
                flash('cow tag already exist', 'error')
                return render_template("cowsinfo.html")
            else:
                file = request.files['image']
                image = Image.open(file)
                newImage = image.resize((341, 512))
                filename = str(uuid.uuid4()) + secure_filename(file.filename)
                newImage.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename))
                newcowinfo = Approval(approval_id=uuid.uuid4(), farmer_id=None, transaction_code="", cow_tag_id=request.form['cow_tag_id'].upper(), cow_breed=request.form['cow_breed'], date_of_birth=request.form['date_of_birth'],
                                      weight=request.form['weight'], cow_gender=request.form['gender'], cow_price=0, cow_status=True, admin_national_id=admin.national_id, sold=False, cow_image=filename, meat=True, milk=False, pregnant=False)
                newcowinfo.save()
                flash('successfully saved', 'success')
                return redirect(url_for('cowinfo'))
        return render_template("cowsinfo.html", breed=rcd)
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route("/changephoto", methods=["POST", "GET"])
def changephoto():
    if request.method == "POST":
        if 'admin' in session:
            admin = admins.query.filter(
                admins.username == session['admin']).first()

            cow = cowsinfo.query.filter(
                and_(cowsinfo.cow_tag_id == request.form['cow_tag_id'], cowsinfo.cow_status == True)).first()
            if cow:
                if cow.cow_image != '':
                    path = os.path.join(UPLOAD_FOLDER, cow.cow_image)
                    os.remove(path)
                file = request.files['image']
                image = Image.open(file)
                newImage = image.resize((341, 512))
                filename = str(uuid.uuid4()) + secure_filename(file.filename)
                newImage.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], filename))
                cow.cow_image = filename
                cow.save()
                flash('successfully updated', 'success')
                return redirect(url_for('view'))
            flash('the cow status is no longer available', 'warning')
            return redirect(url_for('view'))
        return redirect(url_for('home'))
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/update_price', methods=['GET', 'POST'])
def updateprice():
    if 'admin' in session:
        if request.method == 'POST':
            if not request.form['cow_tag_id'] or not request.form['is_milked']:
                flash('fill all fields', 'error')
                return redirect(url_for('view'))
            milked = False
            expectant = False
            if request.form['is_milked'] == 'True':
                milked = True
            if request.form['is_expectant'] == 'True':
                expectant = True
            cow = cowsinfo.query.filter(
                and_(cowsinfo.cow_tag_id == request.form['cow_tag_id'], cowsinfo.cow_status == True)).first()
            if cow:
                cow.cow_price = int(request.form['price'])
                cow.weight = request.form['weight']
                cow.pregnant = expectant
                cow.milk = milked

                cow.save()
                flash('successfully updated ' + cow.cow_tag_id, 'success')
                return redirect(url_for('view'))
            else:
                flash('cow ' + request.form['cow_tag_id'] +
                      ' is no longer available', 'warning')
                return redirect(url_for('view'))
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/superadmin', methods=['GET', 'POST'])
def superadmin():
    if 'superadmin' in session:
        return render_template('superadmin/admindash.html', admin='admin')
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'pass':
            session['superadmin'] = request.form['username']
            return render_template('superadmin/admindash.html', admin='admin')
    return render_template('login.html', user='superadmin')


@app.route('/view', methods=['GET', 'POST'])
@app.route('/view/page/<int:page>')
def view(page=1):
    const_per_page = 8
    if "admin" in session:
        user = admins.query.filter(admins.username == session['admin']).first()

        cows = cowsinfo.query.filter(cowsinfo.cow_status == True).order_by(
            cowsinfo.cow_tag_id.asc()
        ).paginate(page, per_page=const_per_page)
        return render_template('viewcows.html', user=user, cows=cows)
    elif "user" in session:
        user = farmers.query.filter(
            farmers.username == session['user']).first()
        if request.method == 'POST':
            choice = request.form['choice']
            if choice == "meat and milk":
                cows = cowsinfo.query.filter(and_(cowsinfo.cow_price > 0, cowsinfo.sold == False, cowsinfo.milk == True, cowsinfo.pregnant == False)).order_by(
                    cowsinfo.cow_tag_id.asc()).paginate(page, per_page=const_per_page)
                return render_template('viewcows.html', user=user, cows=cows)
            elif choice == "meat and pregnant":
                cows = cowsinfo.query.filter(and_(cowsinfo.cow_price > 0, cowsinfo.sold == False, cowsinfo.milk == False, cowsinfo.pregnant == True)).order_by(
                    cowsinfo.cow_tag_id.asc()).paginate(page, per_page=const_per_page)
                return render_template('viewcows.html', user=user, cows=cows)
            elif choice == "meat milk and pregnant":
                cows = cowsinfo.query.filter(and_(cowsinfo.cow_price > 0, cowsinfo.sold == False, cowsinfo.milk == True, cowsinfo.pregnant == True)).order_by(
                    cowsinfo.cow_tag_id.asc()).paginate(page, per_page=const_per_page)
                return render_template('viewcows.html', user=user, cows=cows)
            elif choice == "meat":
                cows = cowsinfo.query.filter(and_(cowsinfo.cow_price > 0, cowsinfo.sold == False, cowsinfo.milk == False, cowsinfo.pregnant == False)).order_by(
                    cowsinfo.cow_tag_id.asc()).paginate(page, per_page=const_per_page)
                return render_template('viewcows.html', user=user, cows=cows)
        cows = cowsinfo.query.filter(and_(cowsinfo.cow_price > 0, cowsinfo.sold == False)).order_by(
            cowsinfo.cow_tag_id.asc()
        ).paginate(page, per_page=const_per_page)
        return render_template('viewcows.html', user=user, cows=cows)
    elif 'superadmin' in session:
        user = session['superadmin']

        cows = cowsinfo.query.filter(cowsinfo.cow_status == True).order_by(
            cowsinfo.cow_tag_id.asc()
        ).paginate(page, per_page=const_per_page)
        return render_template('viewcows.html', user=user, cows=cows)
    elif 'manager' in session:
        user = session['manager']

        cows = cowsinfo.query.filter(cowsinfo.cow_status == True).order_by(
            cowsinfo.cow_tag_id.asc()
        ).paginate(page, per_page=const_per_page)
        return render_template('viewcows.html', user=user, cows=cows)
    else:
        if request.method == 'POST':
            choice = request.form['choice']
            if choice == "meat and milk":
                cows = cowsinfo.query.filter(and_(cowsinfo.cow_price > 0, cowsinfo.sold == False, cowsinfo.cow_status == True, cowsinfo.milk == True, cowsinfo.pregnant == False)).order_by(
                    cowsinfo.cow_tag_id.asc()).paginate(page, per_page=const_per_page)
                return render_template('viewcows.html', cows=cows)
            elif choice == "meat and pregnant":
                cows = cowsinfo.query.filter(and_(cowsinfo.cow_price > 0, cowsinfo.milk == False, cowsinfo.cow_status == True, cowsinfo.sold == False, cowsinfo.pregnant == True)).order_by(
                    cowsinfo.cow_tag_id.asc()).paginate(page, per_page=const_per_page)
                return render_template('viewcows.html', cows=cows)
            elif choice == "meat milk and pregnant":
                cows = cowsinfo.query.filter(and_(cowsinfo.cow_price > 0, cowsinfo.milk == True, cowsinfo.cow_status == True, cowsinfo.sold == False, cowsinfo.pregnant == True)).order_by(
                    cowsinfo.cow_tag_id.asc()).paginate(page, per_page=const_per_page)
                return render_template('viewcows.html', cows=cows)
            elif choice == "meat":
                cows = cowsinfo.query.filter(and_(cowsinfo.cow_price > 0, cowsinfo.milk == False, cowsinfo.cow_status == True, cowsinfo.sold == False, cowsinfo.pregnant == False)).order_by(
                    cowsinfo.cow_tag_id.asc()).paginate(page, per_page=const_per_page)
                return render_template('viewcows.html', cows=cows)
        cows = cowsinfo.query.filter(and_(cowsinfo.cow_price > 0, cowsinfo.cow_status == True, cowsinfo.sold == False)).order_by(
            cowsinfo.cow_tag_id.asc()
        ).paginate(page, per_page=const_per_page)
        return render_template('viewcows.html', cows=cows)


@app.route('/viewcow', methods=['GET', 'POST'])
def viewcow():
    if request.method == 'POST':
        if "admin" in session:
            user = admins.query.filter(
                admins.username == session['admin']).first()
            cows = cowsinfo.query.filter(
                cowsinfo.cow_tag_id == request.form['cow_tag_id']).first()
            return render_template('viewcow.html', user=user, cow=cows)
        elif "user" in session:
            user = farmers.query.filter(
                farmers.username == session['user']).first()
            cart_cows = cart_table.query.filter(
                cart_table.farmer_id == user.farmer_national_id).all()
            cows = cowsinfo.query.filter(
                cowsinfo.cow_tag_id == request.form['cow_tag_id']).first()
            return render_template('viewcow.html', user=user, cow=cows, cart=cart_cows)
        else:
            cows = cowsinfo.query.filter(
                cowsinfo.cow_tag_id == request.form['cow_tag_id']).first()
            return render_template('viewcow.html', cow=cows)
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route("/milk_sale", methods=['GET', 'POST'])
def milk_sales():
    if 'user' in session:
        dates = str(Date.now())
        date1 = dates[:4] + '/'+dates[5:7] + '/' + dates[8:10]
        if request.method == 'POST':
            if not request.form['transaction_code']:
                flash('fill the required fields', 'error')
            transaction_code = request.form['transaction_code']
            farmer = farmers.query.filter(
                farmers.username == session['user']).first()
            sale = transactions.query.filter(
                transactions.transaction_code == request.form['transaction_code'].upper()).first()
            if sale:
                quantity = int(sale.amount)/1

                newSale = milk_sale(milk_sale_id=uuid.uuid4(), milk_quantity=quantity, milk_sale_date=sale.date, milk_price=sale.amount,
                                    admin_national_id=None, farmer_national_id=farmer.farmer_national_id, farmer_phone_number=farmer.phone_number, transaction_code=transaction_code)
                newSale.save()
                remamount = milk_total.query.filter(
                    milk_total.date_of_collection == date1).first()
                if remamount.carried_foward > 0:
                    news = remamount.carried_foward - int(quantity)
                    if news > 0:
                        remamount.carried_foward = news
                        remamount.sold_out += int(quantity)
                        print(news)
                        remamount.save()
                        sale1 = transactions.query.filter(
                            transactions.transaction_code == request.form['transaction_code'].upper()).first()
                        db.session.delete(sale1)
                        db.session.commit()
                        flash('milk collection record saved successfully', 'success')
                        return redirect(url_for('login'))
                    else:
                        remamount.quantity += news
                        remamount.carried_foward = 0
                        remamount.sold_out += int(quantity)
                        remamount.save()
                        sale1 = transactions.query.filter(
                            transactions.transaction_code == request.form['transaction_code'].upper()).first()
                        db.session.delete(sale1)
                        db.session.commit()
                        flash('milk collection record saved successfully', 'success')
                        return redirect(url_for('login'))
                else:
                    remamount.quantity -= int(quantity)
                    remamount.sold_out += int(quantity)
                    remamount.save()
                    sale1 = transactions.query.filter(
                        transactions.transaction_code == request.form['transaction_code'].upper()).first()
                    db.session.delete(sale1)
                    db.session.commit()
                    flash('milk order placed successfully', 'success')
                    return redirect(url_for('login'))
            else:
                flash('enter a valid transaction code', 'error')
                return redirect(url_for('login'))
    if 'admin' in session:
        if request.method == 'POST':
            if not request.form['transaction_code']:
                flash('fill the required field', 'error')
            admin = admins.query.filter(
                admins.username == session['admin']).first()
            transaction_code = request.form['transaction_code']

            newSale = milk_sale.query.filter(
                and_(milk_sale.transaction_code == request.form['transaction_code'], milk_sale.admin_national_id == None)).first()
            if newSale:
                newSale.admin_national_id = admin.national_id
                newSale.save()
                flash('milk sold successfully', 'success')
                return redirect(url_for('milk_sales'))
            else:
                flash('the milk was sold already', 'warning')
                return redirect(url_for('milk_sales'))
        return render_template('milk_sale.html')
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/totals', methods=['GET'])
def totals():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    totl = milk_total.query.all()
    jsonResp = json.dumps([u.serialize() for u in totl])

    return jsonify(jsonResp)


@app.route("/cow_sale", methods=['GET', 'POST'])
def cow_sale():
    if 'user' in session:
        if request.method == 'POST':
            if not request.form['transaction_code']:
                flash('fill the required fields', 'error')
            transaction_code = request.form['transaction_code']
            farmer = farmers.query.filter(
                farmers.username == session['user']).first()

            sale = transactions.query.filter(
                transactions.transaction_code == transaction_code).first()

            items = cart_table.query.filter(
                cart_table.farmer_id == farmer.farmer_national_id)
            for cow1 in items:
                cow = cowsinfo.query.filter(
                    cowsinfo.cow_tag_id == cow1.cow_tag_id).first()
                if cow_sales.query.filter(cow_sales.cow_tag_id == cow1.cow_tag_id).first():
                    delt = cart_table.query.filter(
                        cart_table.cow_tag_id == cow1.cow_tag_id).first()

                    db.session.delete(delt)
                    db.session.commit()

                    flash('sorry the cow ' + cow.cow_tag_id +
                          ' is already sold out', 'success')
                    return redirect(url_for('get_post_cart'))
                newcowinfo = Approval(approval_id=uuid.uuid4(), farmer_id=farmer.farmer_national_id, transaction_code=sale.transaction_code, cow_tag_id=cow.cow_tag_id, cow_breed=cow.cow_breed, date_of_birth=cow.date_of_birth,
                                      weight=cow.weight, cow_gender=cow.cow_gender, cow_price=cow.cow_price, cow_status=True, admin_national_id=None, sold=True, cow_image=cow.cow_image, meat=cow.meat, milk=cow.milk, pregnant=cow.pregnant)

                # newSale = cow_sales(cow_tag_id=cow.cow_tag_id, cow_sale_date=sale.date, cow_price=sale.amount,
                #                     admin_national_id=None, farmer_national_id=farmer.farmer_national_id, farmer_phone_number=farmer.phone_number, transaction_code=transaction_code)

                newcowinfo.save()
                delt = cart_table.query.filter(
                    cart_table.cow_tag_id == cow.cow_tag_id).first()

                cowupdate = cowsinfo.query.filter(
                    cowsinfo.cow_tag_id == cow.cow_tag_id).first()
                cowupdate.cow_price = 0
                cowupdate.cow_status = False
                cowupdate.sold = True
                cowupdate.save()
                db.session.delete(delt)
                db.session.commit()
            flash('cow transaction successfully initiated you will be notified of the progress via email', 'success')
            return redirect(url_for('login'))
    if 'admin' in session:
        if request.method == 'POST':
            if not request.form['transaction_code']:
                flash('fill the required field', 'error')
            admin = admins.query.filter(
                admins.username == session['admin']).first()
            transaction_code = request.form['transaction_code']

            newSale = cow_sales.query.filter(
                cow_sales.transaction_code == request.form['transaction_code']).first()
            newSale.admin_national_id = admin.national_id
            newSale.save()
            flash('milk sold successfully', 'success')
            return redirect(url_for('milk_sales'))
        return render_template('milk_sale.html')
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route("/milk_collection", methods=['POST', 'GET'])
def milk_collections():

    if 'admin' in session:
        staf = staff.query.all()
        if request.method == 'POST':
            admin = admins.query.filter(
                admins.username == session['admin']).first()
            cow = cowsinfo.query.filter(
                and_(cowsinfo.cow_tag_id == request.form['cow_tag_id'], cowsinfo.cow_status == True)).first()
            if cow:
                newCollection = milk_collection(milk_collection_id=uuid.uuid4(), milk_quantity=float(request.form['milk_quantity']), milk_collection_date=request.form['milk_collection_date'], milk_quality=request.form[
                                                'milk_quality'], milk_collection_time=request.form['milk_collection_time'], admin_national_id=admin.national_id, cow_tag_id=request.form['cow_tag_id'], milking_personel=request.form['milking_personel'])
                newCollection.save()

                milk_totals(request.form['milk_quantity'])
            else:
                flash(
                    'The cow tag ' + request.form['cow_tag_id'] + ' entered is invalid', 'warning')
                return redirect(url_for('milk_collections'))
        return render_template('milk_collection.html', staff=staf)

    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/cow_s', methods=['GET'])
def cow_s():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    cowinf = cowsinfo.query.all()
    jsonResp = json.dumps([u.serialize() for u in cowinf])

    return jsonify(jsonResp)


@app.route("/feed", methods=['GET', 'POST'])
def feed():
    if 'admin' in session:
        staf = staff.query.all()
        foods = cowfeedinventory.query.all()
        if request.method == 'POST':
            if not cowsinfo.query.filter(and_(cowsinfo.cow_tag_id == request.form['cow_tag_id'], cowsinfo.cow_status == True)).first():
                flash('please enter a valid cow_tag_id', 'error')
                return redirect(url_for('feed'))
            admin = admins.query.filter(
                admins.username == session['admin']).first()
            if not request.form['type_of_food'] or not request.form['cow_tag_id'] or not request.form['cow_feed_name'] or not request.form['quantity_fed'] or not request.form['time_fed'] or not request.form['feeding_personnel']:
                flash('fill all fields', 'error')
            newfeed = cowfeeds(cow_feed_id=uuid.uuid4(), type_of_food=request.form['type_of_food'], quantity_given=request.form['quantity_fed'], time_of_feeding=request.form['time_fed'],
                               cow_tag_id=request.form['cow_tag_id'], admin_national_id=admin.national_id, feeding_personnel_id=request.form['feeding_personnel'], food_name=request.form['cow_feed_name'], date_of_feeding=request.form['date_of_feeding'])
            newfeed.save()
            flash('record saved successfully', 'success')
            return redirect(url_for('feed'))

        return render_template('feed/cowfeeds.html', staff=staf, food=foods)
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route("/inseminationrecord", methods=["POST", "GET"])
def inseminationrecord():
    if 'admin' in session:
        breed = cowscategory.query.filter(cowscategory.sex == 'male').all()
        if request.method == "POST":
            if not request.form['cow_tag_id'] or not request.form['date_of_insemination'] or not request.form['breed'] or not request.form['sperm_dose'] or not request.form['insemination_officer'] or not request.form['no_of_inseminations'] or not request.form['insemination_officer_id'] or not request.form['insemination_officer_contact'] or not request.form['age_at_insemination']:
                flash('fill all required fields', 'error')
                return redirect(url_for('inseminationrecord', breed=breed))
            elif not cowsinfo.query.filter(and_(cowsinfo.cow_tag_id == request.form['cow_tag_id'], cowsinfo.cow_status == True)).first():
                flash('cow the cow tag ' + request.form['cow_tag_id'] +
                      ' you have entered is wrong please check it again', 'error')
                return redirect(url_for('inseminationrecord', breed=breed))
            admin = admins.query.filter(
                admins.username == session['admin']).first()
            newinsem = inseminations(insem_id=uuid.uuid4(), cow_tag_id=request.form['cow_tag_id'], date_of_insemination=request.form['date_of_insemination'], admin_national_id=admin.national_id, breed=request.form['breed'], sperm_dose=request.form['sperm_dose'], insemination_officer=request.form[
                                     'insemination_officer'], no_of_inseminations=request.form['no_of_inseminations'], insemination_officer_contact=request.form['insemination_officer_contact'], insemination_officer_id=request.form['insemination_officer_id'], age_at_insemination=request.form['age_at_insemination'])
            newinsem.save()
            flash('successfully saved', 'success')
            return redirect(url_for('inseminationrecord', breed=breed))
        return render_template("insemination.html", breed=breed)
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route("/cowscategory", methods=["POST", "GET"])
def cowscat():
    if 'admin' in session:
        admin = admins.query.filter(
            admins.username == session['admin']).first()
        if request.method == "POST":
            if not request.form['breed'] or not request.form['description'] or not request.form['sex']:
                flash('please fill all required information', 'error')
                return redirect(url_for("cowscat"))
            newcategory = cowscategory(category_id=uuid.uuid4(
            ), breed=request.form['breed'], description=request.form['description'], sex=request.form['sex'], admin_national_id=admin.national_id, breed_id=uuid.uuid4())
            newcategory.save()
            flash('succesfully saved', 'success')
            return redirect(url_for("cowscat"))
        return render_template("cowscategory.html", admin=admin)
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route("/vaccineinventory", methods=["POST", "GET"])
def vaccineinventory():
    if 'admin' in session:
        admin = admins.query.filter(
            admins.username == session['admin']).first()
        if request.method == "POST":
            if not(request.form['vaccine_name'] or request.form['disease_treated'] or request.form['available_vaccine_quantity'] or request.form['date_in'] or request.form['supplier_name'] or request.form['admin_national_id'] or not request.form['supplier_contact']):
                flash('enter all credentials', 'error')
                return render_template("healthinfo.html")
            elif vaccineinventories.query.filter(vaccineinventories.vaccine_name == request.form['vaccine_name'].capitalize()).first():
                vaccine = vaccineinventories.query.filter(
                    vaccineinventories.vaccine_name == request.form['vaccine_name'].capitalize()).first()
                vaccine.available_vaccine_quantity += int(
                    request.form['available_vaccine_quantity'])
                flash('updated successfully', 'success')
                return redirect(url_for('vaccineinventory'))
            else:
                newvaccine = vaccineinventories(vaccine_name=request.form['vaccine_name'].capitalize(), disease_treated=request.form['disease_treated'].capitalize(
                ), available_vaccine_quantity=request.form['available_vaccine_quantity'], date_in=Date.now(), supplier_name=request.form['supplier_name'], admin_national_id=admin.national_id, supplier_contact=request.form['supplier_contact'])
                newvaccine.save()
                flash('record successfully saved', 'success')
                return redirect(url_for('vaccineinventory'))
        return render_template("vaccineinventory.html")
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route("/health", methods=["POST", "GET"])
def health():
    if 'admin' in session:
        vaccine = vaccineinventories.query.all()
        if request.method == "POST":

            admin = admins.query.filter(
                admins.username == session['admin']).first()
            if not(request.form['date_of_vaccination'] or request.form['disease_name'] or request.form['prescription'] or request.form['duration'] or request.form['vet_name'] or request.form['vet_id'] or request.form['admin_national_id']):
                flash('fill all fields', 'error')
                return render_template("health.html")
            elif not vaccineinventories.query.filter(vaccineinventories.vaccine_name == request.form['vaccine_name']).first():
                flash('the vaccine does not exist', 'error')
                return redirect(url_for("health"))
            elif not cowsinfo.query.filter(and_(cowsinfo.cow_tag_id == request.form['cow_tag_id'], cowsinfo.cow_status == True)).first():
                flash('invalid cow tag id', 'error')
                return redirect(url_for('health'))
            newhealthinfo = healthinfo(healthinfo_id=uuid.uuid4(), date_of_vaccination=request.form['date_of_vaccination'], disease_treated=request.form['disease_treated'], prescription=request.form['prescription'], treatment_duration=request.form[
                                       'treatment_duration'], vet_name=request.form['vet_name'], vet_id=request.form['vet_id'], admin_national_id=admin.national_id, vaccine_name=request.form['vaccine_name'], cow_tag_id=request.form['cow_tag_id'], weight=request.form['weight'])
            newhealthinfo.save()
            flash("saved successfully", 'success')
            return redirect(url_for('health'))
        return render_template('health.html', vaccine=vaccine)
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/feedinventory', methods=["POST", "GET"])
def cowfeedinventori():
    if 'admin' in session:
        admin = admins.query.filter(
            admins.username == session['admin']).first()
        if request.method == "POST":
            feed = cowfeedinventory.query.filter(
                cowfeedinventory.food_name == request.form['feed_name']).first()
            if feed:
                quant = int(feed.feed_quantity)
                quanty = quant + int(request.form['feed_quantity'])
                feed.quantity = quanty
                feed.save()
                flash(
                    'feed existed therefore quantity has neen updated successfully', 'success')
                return redirect(url_for('cowfeedinventori'))
            newfeed = cowfeedinventory(feed_id=uuid.uuid4(), food_name=request.form['feed_name'], type_of_food=request.form['type_of_feed'], feed_quantity=request.form[
                                       'feed_quantity'], supplier_name=request.form['supplier_name'], supplier_contact=request.form['supplier_contact'], date_in=request.form['date_in'], admin_national_id=admin.national_id)
            newfeed.save()
            flash('successfully saved', 'success')
            return redirect(url_for('cowfeedinventori'))
        return render_template("feed/feeding.html")
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    if 'user' in session:
        if request.method == 'POST':
            farmer = farmers.query.filter(
                farmers.username == session['user']).first()
            phone = farmer.phone_number
            amount = request.form['amount']
            dates = str(Date.now())
            date1 = dates[:4] + '/'+dates[5:7] + '/' + dates[8:10]
            if milk_total.query.filter(milk_total.date_of_collection == date1).first() or milk_total.query.filter(milk_total.date_of_collection == date1).first():
                if int(request.form['quantity']) > milk_total.query.filter(milk_total.date_of_collection == date1).first().quantity + milk_total.query.filter(milk_total.date_of_collection == date1).first().carried_foward:
                    flash('the amount requested for is not available', 'warning')
                    return redirect(url_for('login'))
                payload = {
                    "business_shortcode": 174379,
                    "passcode": "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919",
                    "amount": int(amount),
                    "phone_number": "+254" + phone[1:],
                    "reference_code": "Dairy Farm",
                    "callback_url": request.url_root + 'confirm',
                    "description": "payment for a service"
                }

                mpesa_api.MpesaExpress.stk_push(**payload)
                flash('please enter the transaction code here', 'success')
                return redirect(url_for('pay'))
            else:
                flash('No milk available', 'success')
                return redirect(url_for('login'))

        return render_template('payment.html')
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/paycow', methods=['GET', 'POST'])
def paycow():
    if 'user' in session:
        if request.method == 'POST':
            farmer = farmers.query.filter(
                farmers.username == session['user']).first()
            phone = farmer.phone_number
            cows = cart_table.query.filter(
                cart_table.farmer_id == farmer.farmer_national_id).all()
            amount = 0
            if cows:
                for cow in cows:
                    amount += cow.cow_price

                # amount = 1  # request.form['total_price']
                payload = {
                    "business_shortcode": 174379,
                    "passcode": "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919",
                    "amount": int(amount),
                    "phone_number": "+254" + phone[1:],
                    "reference_code": "Dairy Farm",
                    "callback_url": request.url_root + 'confirm_cow/' + farmer.username,
                    "description": "payment for a service"
                }

                mpesa_api.MpesaExpress.stk_push(**payload)
                flash('please enter the transaction code here', 'success')
                return render_template('paycow.html')
            flash('the cow(s) has already been sold out please contact our customer care for more direction', 'warning')
            return get_post_cart()
        return render_template('paycow.html')
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/confirm', methods=['GET', 'POST'])
def confirm():

    json_data = request.json
    print(json_data)

    # if result code is 0 you can proceed and save the data else if its any other number you can track the transaction

    print(json_data['Body']['stkCallback']['ResultDesc'])
    if json_data['Body']['stkCallback']['ResultDesc'] == 'The service request is processed successfully.' and json_data['Body']['stkCallback']['CallbackMetadata']:
        transction_cod = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
        amnt = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
        phone = str(json_data['Body']['stkCallback']
                    ['CallbackMetadata']['Item'][4]['Value'])
        phone_nmber = "0" + phone[3:]
        date = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
        newTransaction = transactions(
            transaction_code=transction_cod, phone_number=phone_nmber, amount=amnt, date=date)
        newTransaction.save()

        return('success')
    flash('transaction failed! a problem occured', 'error')
    # pyautogui.hotkey('f5')
    flash('oops! an error occured' 'error')
    return render_template('errors/error1.html')


@app.route('/confirm_cow', methods=['GET', 'POST'])
@app.route('/confirm_cow/<string:user>', methods=['GET', 'POST'])
def confirm_cow(user):
    curent_user = farmers.query.filter(
        farmers.username == request.path[13:]).first()
    json_data = request.json

    # if result code is 0 you can proceed and save the data else if its any other number you can track the transaction

    print(json_data['Body']['stkCallback']['ResultDesc'])
    if json_data['Body']['stkCallback']['ResultDesc'] == 'The service request is processed successfully.' and json_data['Body']['stkCallback']['CallbackMetadata']:
        transction_cod = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
        amnt = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
        phone = str(json_data['Body']['stkCallback']
                    ['CallbackMetadata']['Item'][4]['Value'])
        phone_nmber = "0" + phone[3:]
        date = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
        newTransaction = transactions(
            transaction_code=transction_cod, phone_number=phone_nmber, amount=amnt, date=date)
        newTransaction.save()
        items = cart_table.query.filter(
            cart_table.farmer_id == curent_user.farmer_national_id).all()
        for item in items:
            item.transaction_code = transction_cod
            item.save()

        return('success')
    flash('transaction failed! a problem occured', 'error')
    # pyautogui.hotkey('f5')
    flash('oops! an error occured' 'error')
    return render_template('errors/error1.html')


@app.route('/calving', methods=['POST', 'GET'])
def calving():
    if 'admin' in session:
        if request.method == 'POST':
            admin = admins.query.filter(
                admins.username == session['admin']).first()
            if not request.form['cow_tag_id'] or not request.form['cow_breed'] or not request.form['date_of_birth'] or not request.form['time_of_birth'] or not request.form['gender'] or not request.files['image']:
                flash('please fill all required fields', 'error')
                return redirect(url_for('calving'))
            file = request.files['image']
            image = Image.open(file)
            newImage = image.resize((200, 200))
            filename = str(uuid.uuid4()) + secure_filename(file.filename)
            newImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if calvings.query.filter(calvings.cow_tag_id == request.form['cow_tag_id']).first():
                flash('The cow tag id ' +
                      request.form['cow_tag_id'] + ' you have entered already exists', 'error')
                return redirect(url_for('calving'))

            newRecord = calvings(calving_id=uuid.uuid4(), cow_tag_id=request.form['cow_tag_id'], anomalies=request.form['anomalies'], breed=request.form['cow_breed'], date_of_birth=request.form[
                                 'date_of_birth'], weight=request.form['weight'], time_of_birth=request.form['time_of_birth'], gender=request.form['gender'], image=filename, admin_national_id=admin.national_id)
            newRecord.save()
            flash('successfully saved', 'success')
            return render_template('calvingrecords.html')
        return render_template('calvingrecords.html')
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route("/deathrecord", methods=["POST", "GET"])
def deathrecord():
    if 'admin' in session:
        if request.method == "POST":

            admin = admins.query.filter(
                admins.username == session['admin']).first()
            if deathrecords.query.filter(deathrecords.cow_tag_id == request.form['cow_tag_id']).first():
                flash('record already exists', 'error')
                return redirect(url_for('deathrecord'))
            available = cowsinfo.query.filter(
                and_(cowsinfo.cow_tag_id == request.form['cow_tag_id'], cowsinfo.cow_status == True)).first()
            if available:
                newdeath = deathrecords(death_record_id=uuid.uuid4(), admin_national_id=admin.national_id,
                                        cow_tag_id=request.form['cow_tag_id'], cause_of_death=request.form['cause_of_death'], date_of_death=request.form['date_of_death'])
                cow = cowsinfo.query.filter(
                    cowsinfo.cow_tag_id == request.form['cow_tag_id']).first()
                cow.cow_price = 0
                cow.cow_status = False
                cow.save()
                flash('successfully updated', 'success')
                newdeath.save()
                return redirect(url_for("deathrecord"))
            else:
                flash(
                    'The cow entered is not valid please enter a valid cow tag id', 'error')
                return redirect(url_for("deathrecord"))
        return render_template("death.html")
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/staff', methods=["POST", "GET"])
def staffs():
    if 'admin' in session:
        admin = admins.query.filter(
            admins.username == session['admin']).first()
        if request.method == "POST":
            if(staff.query.filter(staff.staff_id == request.form['staff_id'])).first():
                flash("Staff_ID exists", 'error')
                return redirect(url_for('staffs'))
            nrecords = staff(first_name=request.form['first_name'].capitalize(), staff_id=request.form['staff_id'].upper(),
                             last_name=request.form['last_name'].capitalize(), other_name=request.form['other_names'].capitalize(), national_id=request.form['national_id'], gender=request.form['gender'], role=request.form['role'], phone_number=request.form['phone_number'])
            flash("Record successfully added", 'success')
            nrecords.save()
            return redirect(url_for('staffs'))
        return render_template('staff.html', admin=admin)
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/changepassword', methods=['POST', 'GET'])
def changepassword():
    if 'user' in session:
        if request.method == 'POST':
            if not request.form['old_password'] or not request.form['new_password'] or not request.form['confirm_password']:
                flash('please fill all the required details', 'error')
                return redirect(url_for('login'))
            elif request.form['new_password'] != request.form['confirm_password']:
                flash('passwords don\'t match!', 'error')
                return redirect(url_for('login'))
            farmer = farmers.query.filter(
                farmers.username == session['user']).first()
            if sha256_crypt.verify(request.form['old_password'], farmer.password):
                farmer.password = sha256_crypt.encrypt(
                    request.form['new_password'])
                farmer.save()
                flash('password successfully changed', 'success')
                return redirect(url_for('login'))
            flash('wrong old password', 'error')
            return redirect(url_for('login'))
    elif 'admin' in session:
        if request.method == 'POST':
            if not request.form['old_password'] or not request.form['new_password'] or not request.form['confirm_password']:
                flash('please fill all the required details', 'error')
                return redirect(url_for('adminlogin'))
            elif request.form['new_password'] != request.form['confirm_password']:
                flash('passwords don\'t match!', 'error')
                return redirect(url_for('adminlogin'))
            admin = admins.query.filter(
                admins.username == session['admin']).first()
            if sha256_crypt.verify(request.form['old_password'], admin.password):
                admin.password = sha256_crypt.encrypt(
                    request.form['new_password'])
                admin.save()
                flash('password successfully changed', 'success')
                return redirect(url_for('adminlogin'))
            flash('wrong old password', 'error')
            return redirect(url_for('adminlogin'))
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/call_modal', methods=['GET', 'POST'])
def call_modal():
    if 'superadmin' in session:
        if request.method == 'POST':
            admin2 = admins.query.filter(
                admins.username == request.form['username']).first()
            return render_template('update_admin.html', admin2=admin2)
        flash('oops! not allowed', 'error')
        return render_template('errors/error1.html')
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/farmers')
@app.route('/farmers/page/<int:page>')
def farmer(page=1):
    const_per_page = 6
    farmer = farmers.query.order_by(
        farmers.username.asc()
    ).paginate(page, per_page=const_per_page)
    return render_template('users.html', farmers=farmer)


@app.route('/search_users', methods=['POST', 'GET'])
@app.route('/search_users/page/<int:page>')
def search_users(page=1):
    if request.method == 'POST':
        if request.form['flag'] == 'farmers':
            if 'admin' in session or 'superadmin' in session:

                const_per_page = 6
                search = (request.form["search"]).lower()
                farmer = farmers.query.filter(or_(func.lower(farmers.first_name) == search, farmers.phone_number == search, func.lower(farmers.last_name) == search, func.lower(farmers.other_names) == search, func.lower(farmers.username) == search, func.lower(farmers.email) == search, func.lower(farmers.gender) == search)).order_by(
                    farmers.username.asc()
                ).paginate(page, per_page=const_per_page)
                return render_template('users.html', farmers=farmer)
        elif request.form['flag'] == 'admins':
            if 'superadmin' in session or 'manager' in session:
                const_per_page = 1000
                search = (request.form["search"]).lower()
                admin = admins.query.filter(or_(func.lower(admins.first_name) == search, cast(admins.phone_number, String) == search, func.lower(admins.last_name) == search, func.lower(admins.other_names) == search, func.lower(admins.username) == search, func.lower(admins.email) == search, func.lower(admins.gender) == search, func.lower(admins.staff_id) == search)).order_by(
                    admins.username.asc()
                ).paginate(page, per_page=const_per_page)
                return render_template('search/adminsearch.html', admin=admin)
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/search_cow', methods=['GET', 'POST'])
def search_cow():
    if request.method == 'POST':
        startdate = request.form['start']
        enddate = request.form['end']
        if "admin" in session:
            user = admins.query.filter(
                admins.username == session['admin']).first()

            cows = cowsinfo.query.filter(and_(cowsinfo.cow_status == True, cowsinfo.date_of_birth.between(
                startdate, enddate))).order_by(
                    cowsinfo.date_of_birth.asc())
            return render_template('searchcows.html', user=user, cows=cows)
        elif "superadmin" in session:

            cows = cowsinfo.query.filter(cowsinfo.date_of_birth.between(
                startdate, enddate)).order_by(
                    cowsinfo.date_of_birth.asc())
            return render_template('searchcows.html', user=session['superadmin'], cows=cows)
        elif "manager" in session:

            cows = cowsinfo.query.filter(cowsinfo.date_of_birth.between(
                startdate, enddate)).order_by(
                    cowsinfo.date_of_birth.asc())
            return render_template('searchcows.html', user=session['manager'], cows=cows)
        elif "user" in session:
            user = farmers.query.filter(
                farmers.username == session['user']).first()
            cows = cowsinfo.query.filter(and_(cowsinfo.cow_price > 0, cowsinfo.cow_status == True, cowsinfo.date_of_birth.between(
                startdate, enddate))).order_by(
                    cowsinfo.date_of_birth.asc())
            return render_template('searchcows.html', user=user, cows=cows)
        else:
            cows = cowsinfo.query.filter(and_(cowsinfo.cow_price > 0, cowsinfo.cow_status == True, cowsinfo.date_of_birth.between(
                startdate, enddate))).order_by(
                    cowsinfo.date_of_birth.asc())
            return render_template('searchcows.html', cows=cows)
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@app.route('/search_other', methods=['GET', 'POST'])
def search_other():
    if request.method == 'POST':
        search = request.form['start'].lower()
        if "admin" in session:
            print(search)
            user = admins.query.filter(
                admins.username == session['admin']).first()

            cows = cowsinfo.query.filter(
                and_(cowsinfo.cow_status == True, or_(func.lower(cowsinfo.cow_breed) == search, func.lower(
                    cowsinfo.cow_tag_id) == search, cast(cowsinfo.cow_price, String) == search))).order_by(
                cowsinfo.cow_tag_id.asc())
            return render_template('searchcows.html', user=user, cows=cows)
        elif "manager" in session:

            cows = cowsinfo.query.filter(
                or_(func.lower(cowsinfo.cow_breed) == search, func.lower(
                    cowsinfo.cow_tag_id) == search, cast(cowsinfo.cow_price, String) == search)).order_by(
                cowsinfo.cow_tag_id.asc())
            return render_template('searchcows.html', user=session['manager'], cows=cows)
        elif "superadmin" in session:

            cows = cowsinfo.query.filter(
                or_(func.lower(cowsinfo.cow_breed) == search, func.lower(
                    cowsinfo.cow_tag_id) == search, cast(cowsinfo.cow_price, String) == search)).order_by(
                cowsinfo.cow_tag_id.asc())
            return render_template('searchcows.html', user=session['superadmin'], cows=cows)
        elif "user" in session:
            user = farmers.query.filter(
                farmers.username == session['user']).first()
            cows = cowsinfo.query.filter(
                and_(cowsinfo.cow_price > 0, cowsinfo.cow_status == True, or_(func.lower(cowsinfo.cow_breed) == search, func.lower(
                    cowsinfo.cow_tag_id) == search, cast(cowsinfo.cow_price, String) == search))).order_by(
                cowsinfo.cow_tag_id.asc())
            return render_template('searchcows.html', user=user, cows=cows)
        else:
            cows = cowsinfo.query.filter(
                and_(cowsinfo.cow_price > 0, cowsinfo.cow_status == True, or_(func.lower(cowsinfo.cow_breed) == search, func.lower(
                    cowsinfo.cow_tag_id) == search, cast(cowsinfo.cow_price, String) == search))).order_by(
                cowsinfo.cow_tag_id.asc())
            return render_template('searchcows.html', cows=cows)
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@ app.route('/reset_pass_request', methods=['GET', 'POST'])
def reset_pass_request():

    if request.method == 'POST':
        if not request.form['username'] or not request.form['email']:
            flash('please fill all fields', 'error')
            return redirect(url_for('reset_pass_request'))
        else:
            user = farmers.query.filter(
                farmers.username == request.form['username'].capitalize()).first()
            if user and user.email == request.form['email']:
                length = 8
                one_time_pass = ''.join(random.choices(
                    string.ascii_letters+string.digits, k=length))
                msg = Message('Password Reset',
                              sender='gtreksolution@noreply.com',
                              recipients=[request.form['email']])
                msg.html = render_template(
                    "email/resetemail.html", user=request.form['username'], password=one_time_pass, link=(request.url_root + 'reset_pass'))
                mail.send(msg)
                user.password = sha256_crypt.encrypt(one_time_pass)
                user.save()
                flash('password reset check your email', 'success')
                return redirect(url_for('reset_pass_request'))
            elif user and user.email != request.form['email']:
                flash('wrong details', 'error')
                return redirect(url_for('reset_pass_request'))
            else:
                flash('user doesn\'t exist ', 'error')
                return redirect(url_for('reset_pass_request'))
    return render_template('reset/reset.html')


@ app.route('/reset_pass', methods=['GET', 'POST'])
def reset_pass():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['one_time_pass'] or not request.form['new_pass'] or not request.form['confirm_pass']:
            flash('fill all fields', 'errror')
            return redirect(url_for('reset_pass'))
        elif request.form['new_pass'] != request.form['confirm_pass']:
            flash("passwords don'\t match ", 'error')
            return redirect(url_for('reset_pass'))
        user = farmers.query.filter(
            farmers.username == request.form['username'].capitalize()).first()
        user.password = sha256_crypt.encrypt(request.form['new_pass'])
        user.save()
        flash('password reset successfully', 'success')
        return redirect(url_for('login'))
    return render_template('reset/pass.html')


@app.route('/get_post_cart', methods=['GET', 'POST'])
def get_post_cart():
    print(Date.now())
    if 'user' in session:
        farmer = farmers.query.filter(
            farmers.username == session['user']).first()
        if request.method == 'POST':
            if request.form['get'] == 'get':
                price = 0

                cart_cows = cart_table.query.filter(
                    cart_table.farmer_id == farmer.farmer_national_id).all()

                for item in cart_cows:
                    delt = cowsinfo.query.filter(
                        cowsinfo.cow_tag_id == item.cow_tag_id).first()
                    if delt.sold == True or delt.cow_status == False:
                        delcow = cart_table.query.filter(
                            cart_table.cow_tag_id == item.cow_tag_id).first()
                        db.session.delete(delcow)
                        db.session.commit()
                    cow = cowsinfo.query.filter(
                        cowsinfo.cow_tag_id == item.cow_tag_id).first()
                    price += int(cow.cow_price)
                return render_template('user/cart.html', price=price, cart_cows=cart_cows)
            cow = cowsinfo.query.filter(
                and_(cowsinfo.cow_tag_id == request.form['cow_tag_id'], cowsinfo.cow_status == True)).first()
            cowcart = cart_table.query.filter(
                and_(cart_table.cow_tag_id == request.form['cow_tag_id'], cart_table.farmer_id == farmer.farmer_national_id)).first()
            if cowcart:
                flash('cow already added', 'success')
                return redirect(url_for('view'))
            if cow:
                newcart = cart_table(cart_id=uuid.uuid4(), farmer_id=farmer.farmer_national_id,
                                     cow_tag_id=cow.cow_tag_id, cow_price=int(cow.cow_price), cow_image=cow.cow_image, transaction_code="")
                newcart.save()
                cart_cows = cart_table.query.filter(
                    cart_table.farmer_id == farmer.farmer_national_id).all()

                flash('cow added to cart successfully', 'success')
                return render_template('viewcow.html', cow=cow, cart=cart_cows)
            flash('Cow does not exist', 'error')
            return redirect(url_for('view'))
        else:
            price = 0

            cart_cows = cart_table.query.filter(
                cart_table.farmer_id == farmer.farmer_national_id).all()

            for item in cart_cows:
                delt = cowsinfo.query.filter(
                    cowsinfo.cow_tag_id == item.cow_tag_id).first()
                if delt.sold == True or delt.cow_status == False:
                    delcow = cart_table.query.filter(
                        cart_table.cow_tag_id == item.cow_tag_id).first()
                    db.session.delete(delcow)
                    db.session.commit()
                cow = cowsinfo.query.filter(
                    cowsinfo.cow_tag_id == item.cow_tag_id).first()
                price += int(cow.cow_price)
            return render_template('user/cart.html', price=price, cart_cows=cart_cows)
    return redirect(url_for('login'))


@ app.route('/remove_from_cart', methods=['GET', 'POST'])
def remove_from_cart():
    if 'user' in session:
        if request.method == 'POST':
            farmer = farmers.query.filter(
                farmers.username == session['user']).first()
            cow_tag_id = request.form['cow_tag_id']
            farmer_id = farmer.farmer_national_id
            items = cart_table.query.filter(
                cart_table.farmer_id == farmer_id).all()
            for item in items:
                if item.farmer_id == farmer_id and item.cow_tag_id == cow_tag_id:
                    db.session.delete(item)
                    db.session.commit()
                    flash('successfully removed ' +
                          cow_tag_id + ' from cart', 'success')

            return redirect(url_for('get_post_cart'))
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@ app.route('/milk_totals', methods=['GET', 'POST'])
def milk_totals(amount):
    if 'admin' in session:
        dates = str(Date.now())
        date1 = dates[:4] + '/'+dates[5:7] + '/' + dates[8:10]
        record = milk_total.query.filter(
            milk_total.date_of_collection == date1).first()
        if record:
            record.quantity += int(amount)
            record.save()
            flash('successfully saved', 'success')
            return redirect(url_for('milk_collections'))
        newtotal = milk_total(_id=uuid.uuid4(), quantity=int(
            amount), date_of_collection=dates[:4] + '/'+dates[5:7] + '/' + dates[8:10], sold_out=0, spoilt=0, carried_foward=0)
        newtotal.save()
        flash('successfully saved', 'success')
        return redirect(url_for('milk_collections'))
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@ app.route('/spoilt_milk', methods=['GET', 'POST'])
def spoilt_milk():
    if request.method == 'POST':
        dates = str(Date.now())
        date1 = dates[:4] + '/'+dates[5:7] + '/' + dates[8:10]
        record = milk_total.query.filter(
            milk_total.date_of_collection == date1).first()
        if not request.form['quantity']:
            flash('please fill all the required fields', 'error')
            return redirect(url_for('adminlogin'))

        amount = int(request.form['quantity'])
        record.spoilt = amount
        if record.carried_foward > 0:
            news = record.carried_foward - amount
            if news < 0:
                record.quantity += news
                record.save()
                flash('successfully added the record', 'success')
                return redirect(url_for('adminlogin'))
            else:
                record.carried_foward = news
                record.save()
                flash('successfully added the record', 'success')
                return redirect(url_for('adminlogin'))
        else:
            record.quantity -= amount
            record.save()
            flash('successfully added the record', 'success')
            return redirect(url_for('adminlogin'))


@ app.route('/sendemail', methods=['GET', 'POST'])
def sendemail():
    if 'manager' in session:
        if request.method == 'POST':
            msg = Message(request.form['subject'],
                          sender='godwillkisia@noreply.com',
                          recipients=[request.form['send_to']])
            msg.html = request.form['email']
            mail.send(msg)
            flash('email sent successfully', 'success')
            return redirect(url_for('sendemail'))
        return render_template('emails.html', flag='one')
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@ app.route('/sendemailtoadmins', methods=['GET', 'POST'])
@ app.route('/sendemailtoadmins/<reciepient>', methods=['GET', 'POST'])
def sendemailtoadmins(reciepient):
    if 'manager' in session:
        emails = []
        if reciepient == 'admins':
            if request.method == 'POST':
                admin = admins.query.all()
                for item in admin:
                    emails.append(item.email)
                msg = Message(request.form['subject'],
                              sender='godwillkisia@noreply.com',
                              recipients=emails)
                msg.html = request.form['email']
                mail.send(msg)
                flash('email sent successfully', 'success')
                return render_template('emails.html', flag='admins')
            return render_template('emails.html', flag='admins')
        if reciepient == 'farmers':
            if request.method == 'POST':
                farmer = farmers.query.all()
                for item in farmer:
                    emails.append(item.email)
                msg = Message(request.form['subject'],
                              sender='godwillkisia@noreply.com',
                              recipients=emails)
                msg.html = request.form['email']
                mail.send(msg)
                flash('email sent successfully', 'success')
                return render_template('emails.html', flag='farmers')
            return render_template('emails.html', flag='farmers')
    flash('oops! not allowed', 'error')
    return render_template('errors/error1.html')


@ app.route('/get_calving_info')
@ app.route('/get_calving_info/page/<int:page>')
def get_calving_info(page=1):
    const_per_page = 10
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        calving_records = calvings.query.order_by(
            calvings.cow_tag_id.asc()).paginate(page, per_page=const_per_page)
    return render_template('calvings.html', calving_records=calving_records)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port='8000')
