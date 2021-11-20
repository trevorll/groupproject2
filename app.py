from flask.helpers import url_for
from werkzeug.utils import redirect, secure_filename
from config import *
from twilio.rest import Client
from datetime import datetime as Date,timedelta
import requests
import uuid
import string
import random
from PIL import Image
import flask
from reports import *

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


def get_mpesa_token():
    
    consumer_key = "fvGLqUuVGCST6YYD2bGOv4CoosCi7Jvn"
    consumer_secret = 'LewDYO7CdnQhDa1J'
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    # make a get request using python requests liblary
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

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


@app.route('/signup',methods=['GET','POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('login'))
    elif request.method=='POST':
        if not request.form['farmer_national_id'] or not request.form['old_password'] or not request.form['password'] or not request.form['confirm_password']:
            flash('please fill all the fields')
            return render_template('user/verify.html')
        elif not(request.form['password']==request.form['confirm_password']):
            flash('passwords entered don\'t match')
            return render_template('user/verify.html')
        else:
            farmer=verify.query.filter(verify.farmer_national_id==request.form['farmer_national_id']).first()
            if sha256_crypt.verify(request.form['old_password'],farmer.password):
                newfarmer=farmers(farmer_national_id=farmer.farmer_national_id,first_name=farmer.first_name,other_names=farmer.other_names,phone_number=farmer.phone_number,username=farmer.username,email=farmer.email,last_name=farmer.last_name,gender=farmer.gender,password=request.form['password'])
                newfarmer.save()
                db.session.delete(farmer)
                db.session.commit()
                session['user']=farmer.username
                return render_template('user/index.html',farmer=farmer)
    
    return render_template('signup.html',user='user')

@app.route("/login",methods=['GET','POST'])
def login():
    if 'user' in session:
        farmer=farmers.query.filter(farmers.username==session['user']).first()
        return render_template('user/index.html', farmer=farmer)

    elif request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            flash('please fill all the fields')
            return redirect(url_for('login'))
        farmer=farmers.query.filter(farmers.username==request.form['username']).first()
        if not farmer:
            flash('user doesn\'t exist')
            return redirect(url_for('login'))
        elif not sha256_crypt.verify(request.form['password'],farmer.password):
            flash('credentials don\'t match')
            return redirect(url_for('login'))
        else:
            session['user']=farmer.username
            flask.session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=30)
            return render_template('user/index.html',farmer=farmer)
    return render_template('login.html',user='user')

@app.route('/update_farmer_details',methods=['POST','GET'])
def update_farmer_details():
    if 'user' in session:
        if request.method=='POST':
            farmer=farmers.query.filter(farmers.username==session['user']).first()
            if not  request.form['first_name'] or not request.form['last_name'] or not request.form['email_address'] or not request.form['other_names'] or not request.form['phone_number']:
                flash('please fill all the fields')
                return redirect(url_for('login'))
            else:
                farmer.first_name=request.form['first_name'].capitalize()
                farmer.other_names=request.form['other_names'].capitalize()
                farmer.phone_number=request.form['phone_number']
                farmer.email=request.form['email_address']
                farmer.last_name=request.form['last_name'].capitalize()
                farmer.save()
                return redirect(url_for('login'))
        return redirect(url_for('login'))
    return redirect(url_for('login'))
@app.route('/update_admin_details',methods=['POST','GET'])
def update_admin_details():
    if 'superadmin' in session:
        admin1 = admins.query.all()
        if request.method=='POST':
            admin=admins.query.filter(admins.national_id==request.form['admin_national_id']).first()
            if not  request.form['first_name'] or not request.form['last_name'] or not request.form['email_address'] or not request.form['phone_number']:
                flash('please fill all the fields')
                return redirect(url_for('update_admin_details'))
            else:
                admin.first_name=request.form['first_name'].capitalize()
                admin.other_names=request.form['other_names'].capitalize()
                admin.phone_number=request.form['phone_number']
                admin.email=request.form['email_address']
                admin.last_name=request.form['last_name'].capitalize()
                admin.save()
                flash('successfully updated')
                return redirect(url_for('update_admin_details'))
        return render_template('admins.html',admin=admin1)
    return redirect(url_for('superadmin'))

@app.route('/logout')
def logout():
    if 'admin' in session:
        session.pop('admin', None)
        return redirect(url_for('adminlogin'))
    elif 'user' in session:
        session.pop('user',None)
        return redirect(url_for('login'))
    elif 'superadmin' in session:
        session.pop('superadmin',None)
        return redirect(url_for('superadmin'))
    
        


@app.route("/adminlogin",methods=['GET','POST'])
def adminlogin():
    if 'admin' in session:
        admin=admins.query.filter(admins.username==session['admin']).first()
        return render_template('admin/dashboard.html', admin=admin)

    elif request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            flash('please fill all the fields')
            return redirect(url_for('adminlogin'))
        admin=admins.query.filter(admins.username==request.form['username'].capitalize()).first()
        if not admin:
            flash('user doesn\'t exist')
            return redirect(url_for('login'))
        elif not sha256_crypt.verify(request.form['password'],admin.password):
            flash('credentials don\'t match')
            return redirect(url_for('adminlogin'))
        else:
            
            session['admin']=admin.username
            flask.session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=30)
            return render_template('admin/dashboard.html',admin=admin)
    return render_template('login.html',user='admin')

@app.route('/verify',methods=['GET','POST'])
def verifyuser():
    if 'user' in session:
        return redirect(url_for('login'))
    elif request.method=='POST':
        length = 8

        farmer=farmers.query.filter(farmers.farmer_national_id==request.form['farmer_national_id']).first()
        email = farmers.query.filter(farmers.email==request.form['email']).first()
        username = farmers.query.filter(farmers.username==request.form['username']).first()
        phone=farmers.query.filter(farmers.phone_number==request.form['phone_number']).first()
        if farmer:
            flash('please pick a different ID number')
            return redirect(url_for('signup'))
        elif email:
            flash('please pick a different email address')
            return redirect(url_for('signup'))
        elif username:
            flash('please pick a different username')
            return redirect(url_for('signup'))
        elif phone:
            flash('please pick a different phone number')
            return redirect(url_for('signup'))
        else:
            one_time_pass= ''.join(random.choices(string.ascii_letters+string.digits,k=length))
            msg=Message('Account creation',
                sender='godwillkisia@noreply.com',
                recipients=[request.form['email']])
            msg.html = render_template("email.html",user=request.form['username'],farmer_national_id=request.form['farmer_national_id'],password=one_time_pass,link=(request.url_root + 'verify'))
            mail.send(msg)
            newfarmer=verify(farmer_national_id=request.form['farmer_national_id'],first_name=request.form['first_name'],other_names=request.form['other_names'],phone_number=request.form['phone_number'],username=request.form['username'],email=request.form['email'],last_name=request.form['last_name'],gender=request.form['gender'],password=one_time_pass)
            newfarmer.save()
            return redirect(url_for('home'))
    return render_template('user/verify.html',user='user')


@app.route("/adminsignup",methods=["POST","GET"])
def adminsignup():
    admin1=admins.query.all()
    if request.method=="POST":
        if not(request.form['admin_national_id'] or request.form['first_name'].capitalize() or request.form['last_name'].capitalize()\
         or request.form['username'].capitalize() or request.form['password'] or request.form['confirm_password'] or  request.form['email']\
         or request.form['phone_number'] or request.form['staff_id'] or request.form['gender'],request.form['role']):
            flash('please fill all fields') 
            return redirect(url_for('adminsignup'))
        elif not request.form['password'] == request.form['confirm_password']:
            flash('passwords don\'t match')
            return redirect(url_for('adminsignup'))
        newAdmin=admins(national_id=request.form['admin_national_id'],staff_id=request.form['staff_id'],first_name=request.form['first_name'].capitalize(),\
        last_name=request.form['last_name'].capitalize(),other_names=request.form['other_names'].capitalize(),phone_number=request.form['phone_number'],email=request.form['email'],gender=request.form['gender'],username=request.form['username'].capitalize(),password=request.form['password'],role=request.form['role'])
        newAdmin.save()
        flash('success')
        return render_template("signup.html",admin=admin1)
    for admi in admin1:
        print(admi.username)
    return render_template("signup.html",admin=admin1)


@app.route("/cowinfo", methods=["POST","GET"])
def cowinfo():
    if request.method=="POST":
        if 'admin' in session:
            admin=admins.query.filter(admins.username==session['admin']).first()
            print(admin.national_id)
            if not( request.form['cow_tag_id'] or request.form['cow_breed'] or request.form['date_of_birth'] or request.form['weight'] or request.form['gender'] or request.form['weight'] ):
                flash('enter all required details')
                return render_template("cowsinfo.html")
            cow=cowsinfo.query.filter(cowsinfo.cow_tag_id==request.form['cow_tag_id']).first()
            if cow:
                flash('cow tag already exist')
                return render_template("cowsinfo.html")
            file=request.files['image']
            image=Image.open(file)
            newImage=image.resize((200,200))
            filename=str(uuid.uuid4()) + secure_filename(file.filename)
            newImage.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print(admin.username)
            newcowinfo=cowsinfo(cow_tag_id=request.form['cow_tag_id'],cow_breed=request.form['cow_breed'],date_of_birth=request.form['date_of_birth'],weight=request.form['weight'],cow_gender=request.form['gender'],cow_price=None,cow_status=True,admin_national_id=admin.national_id,cow_image=filename) 
            newcowinfo.save() 
            flash('success')
            return redirect(url_for('cowinfo'))
        return redirect(url_for('home'))
    return render_template("cowsinfo.html")
@app.route('/superadmin',methods=['GET', 'POST'])

def superadmin():
    if 'superadmin' in session:
        return render_template('superadmin/admindash.html',admin='admin')
    if request.method == 'POST':
        if request.form['username']=='admin' and request.form['password']=='pass':
            session['superadmin']=request.form['username']
            return render_template('superadmin/admindash.html',admin='admin')
    return render_template('login.html',user='superadmin')


@app.route('/view')
def view():
    cows=cowsinfo.query.all()
    return render_template('viewcows.html',cows=cows)

@app.route("/milk_sale",methods=['GET','POST'])
def milk_sales():
    if 'user' in session:
        if request.method=='POST':
            if not request.form['transaction_code']:
                flash('fill the required field')
            price_per_litre=float(50)
            transaction_code = request.form['transaction_code']
            farmer=farmers.query.filter(farmers.username==session['user']).first()
            sale=transactions.query.filter(transactions.transaction_code==request.form['transaction_code']).first()
            quantity=int(sale.amount)/45
           
            
            newSale = milk_sale(milk_sale_id=uuid.uuid4(),milk_quantity=quantity,milk_sale_date=sale.date,milk_price=sale.amount,\
                admin_national_id=None,farmer_national_id=farmer.farmer_national_id,farmer_phone_number=farmer.phone_number,transaction_code=transaction_code)
            newSale.save()
            flash('milk collection record saved successfully')
            return redirect(url_for('login'))
    if 'admin' in session:
        if request.method=='POST':
            if not request.form['transaction_code']:
                flash('fill the required field')
            admin=admins.query.filter(admins.username==session['admin']).first()
            transaction_code = request.form['transaction_code']

            newSale = milk_sale.query.filter(milk_sale.transaction_code==request.form['transaction_code']).first()
            newSale.admin_national_id=admin.national_id
            newSale.save()
            flash('milk sold successfully')
            return redirect(url_for('milk_sales'))
        return render_template('milk_sale.html')
        
        
@app.route("/milk_collection",methods=['POST','GET'])
def milk_collections():
    if 'admin' in session:
        if request.method=='POST':
            admin = admins.query.filter(admins.username==session['admin']).first()
            newCollection = milk_collection(milk_collection_id=uuid.uuid4(),milk_quantity=float(request.form['milk_quantity']),milk_collection_date=request.form['milk_collection_date'],milk_quality=request.form['milk_quality']\
                ,milk_collection_time=request.form['milk_collection_time'],admin_national_id=admin.national_id,cow_tag_id=request.form['cow_tag_id'])
            newCollection.save()
            flash('milk collection record saved successfully')
            return render_template('milk_collection.html')
        return render_template('milk_collection.html')
    return render_template('milk_collection.html')

@app.route("/feed",methods=['GET','POST'])
def feed():
    if 'admin' in session:
        if request.method=='POST':
            admin=admins.query.filter(admins.username==session['admin']).first()
            if not request.form['type_of_food'] or not request.form['cow_tag_id'] or not request.form['cow_feed_name'] or not request.form['quantity_fed'] or not request.form['time_fed'] or not request.form['feeding_personnel']:
                flash('fill all fields')
            newfeed=cowfeeds(cow_feed_id=uuid.uuid4(),type_of_food=request.form['type_of_food'],quantity_given=request.form['quantity_fed'],time_of_feeding=request.form['time_fed'],cow_tag_id=request.form['cow_tag_id'],admin_national_id=admin.national_id,feeding_personnel_id=request.form['feeding_personnel'],food_name=request.form['cow_feed_name'])
            newfeed.save()
            flash('record saved successfully')
            return redirect(url_for('feed'))



        return render_template('feed/cowfeeds.html')





@app.route("/inseminationrecord",methods=["POST","GET"])
def inseminationrecord():
    if 'admin' in session:
        if request.method=="POST":
            if not request.form['cow_tag_id'] or not request.form['date_of_insemination'] or not request.form['breed'] or not request.form['sperm_dose'] or not request.form['insemination_officer'] or not request.form['no_of_inseminations'] or not request.form['insemination_officer_id'] or not request.form['insemination_officer_contact'] or not request.form['age_at_insemination']:
                flash('fill all required fields')
            admin=admins.query.filter(admins.username==session['admin']).first()         
            newinsem=inseminations(insem_id=uuid.uuid4(),cow_tag_id=request.form['cow_tag_id'],date_of_insemination=request.form['date_of_insemination'],admin_national_id=admin.national_id,breed=request.form['breed'],sperm_dose=request.form['sperm_dose'],insemination_officer=request.form['insemination_officer'],no_of_inseminations=request.form['no_of_inseminations'],insemination_officer_contact=request.form['insemination_officer_contact'],insemination_officer_id=request.form['insemination_officer_id'],age_at_insemination=request.form['age_at_insemination'])
            newinsem.save()
            flash('success')
            return redirect(url_for('inseminationrecord'))
        return render_template("insemination.html")  


@app.route("/cowscategory",methods=["POST","GET"])
def cowscat():
    if 'admin' in session:
        admin=admins.query.filter(admins.username==session['admin']).first()
        if request.method=="POST":
            category=cowscategory.query.all()
            
            newcategory=cowscategory(category_id=uuid.uuid4(),breed=request.form['breed'],description=request.form['description'],admin_national_id=admin.national_id,breed_id=request.form['reed_id'])
            newcategory.save()        
            return render_template("cowscategory.html")
        return render_template("cowscategory.html")

@app.route("/vaccineinventory",methods=["POST","GET"])
def vaccineinventory():
    if 'admin' in session:
        admin=admins.query.filter(admins.username==session['admin']).first()
        if request.method=="POST":
            if not(request.form['vaccine_name'] or request.form['disease_treated'] or request.form['available_vaccine_quantity'] or request.form['date_in'] or request.form['supplier_name'] or request.form['admin_national_id'] or not request.form['supplier_contact']):
                flash('enter all credentials')
                return render_template("healthinfo.html")
            newvaccine=vaccineinventories(vaccine_name=request.form['vaccine_name'].capitalize(),disease_treated=request.form['disease_treated'].capitalize(),available_vaccine_quantity=request.form['available_vaccine_quantity'],date_in=Date.now(),supplier_name=request.form['supplier_name'],admin_national_id=admin.national_id,supplier_contact=request.form['supplier_contact'])
            newvaccine.save()
            flash('record successfully saved')
            return redirect(url_for('vaccineinventory'))
    return render_template("vaccineinventory.html")


@app.route("/health",methods=["POST","GET"])
def health():
    if request.method=="POST":
        if 'admin' in session:
            admin=admins.query.filter(admins.username==session['admin']).first()
            if not(request.form['date_of_vaccination'] or request.form['disease_name'] or request.form['prescription'] or request.form['duration'] or request.form['vet_name'] or request.form['vet_id'] or request.form['admin_national_id']):
                flash('fill all fields')
                return render_template("health.html")
            newhealthinfo=healthinfo(healthinfo_id=uuid.uuid4(), date_of_vaccination=request.form['date_of_vaccination'],disease_treated=request.form['disease_treated'],prescription=request.form['prescription'],treatment_duration=request.form['treatment_duration'],vet_name=request.form['vet_name'],vet_id=request.form['vet_id'],admin_national_id=admin.national_id,vaccine_name=request.form['vaccine_name'],cow_tag_id=request.form['cow_tag_id'],weight=request.form['weight'])
            newhealthinfo.save()
            return redirect(url_for('health'))
        return render_template("home.html")
    return render_template('health.html')

@app.route('/feedinventory',methods=["POST","GET"])
def cowfeedinventori():
    if 'admin' in session:
        admin=admins.query.filter(admins.username==session['admin']).first()
        if request.method=="POST":
            if cowfeedinventory.query.filter(cowfeedinventory.food_name==request.form['feed_name']).first():
                flash('feed already exist')
                return render_template('feed/feeding.html')
            newfeed=cowfeedinventory(feed_id=uuid.uuid4(),food_name=request.form['feed_name'],type_of_food=request.form['type_of_feed'],feed_quantity=request.form['feed_quantity'],supplier_name=request.form['supplier_name'],supplier_contact=request.form['supplier_contact'],admin_national_id=admin.national_id)
            newfeed.save()
            return redirect(url_for('feed'))
        return render_template("feed/feeding.html") 





@app.route('/pay',methods=['GET','POST'])
def pay():
    if 'user' in session:
        if request.method=='POST':
            farmer = farmers.query.filter(farmers.username==session['user']).first()
            phone = farmer.phone_number
            amount = request.form['amount']
            payload = {
                "business_shortcode":174379,
                "passcode": "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919",
                "amount": int(amount),
                "phone_number":"+254" + phone[1:],
                "reference_code": "Dairy Farm",
                "callback_url": request.url_root + 'confirm', 
                "description": "payment for a service" 
            }

            mpesa_api.MpesaExpress.stk_push(**payload)
            flash('please enter the transaction code here') 
            return render_template('payment.html')
        return render_template('payment.html')

@app.route('/confirm',methods=['GET','POST'])
def confirm():

    json_data = request.json
    
    #if result code is 0 you can proceed and save the data else if its any other number you can track the transaction
    print(json_data['Body']["stkCallback"]['ResultDesc'])
    flag=json_data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    # if (flag=='The service request is processed successfully.'):
    transction_cod=json_data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    amnt=json_data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
    phone= str(json_data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value'])
    phone_nmber="0" + phone[3:]
    date = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
    newTransaction = transactions(transaction_code=transction_cod,phone_number=phone_nmber,amount=amnt,date=date)
    newTransaction.save()
    flash('successfully place your order')
    return redirect(url_for('login'))


@app.route('/calving',methods=['Post','GET'])
def calving():
    if 'admin' in session:
        if request.method=='POST':
            admin = admins.query.filter(admins.username==session['admin']).first()
            if not request.form['cow_tag_id'] or not request.form['cow_breed'] or not request.form['date_of_birth'] or not request.form['time_of_birth'] or not request.form['gender'] or not request.files['image']:
                flash('please fill all required fields')
            file=request.files['image']
            image=Image.open(file)
            newImage=image.resize((200,200))
            filename=str(uuid.uuid4()) + secure_filename(file.filename)
            newImage.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

            newRecord = calvings(calving_id=uuid.uuid4(),cow_tag_id = request.form['cow_tag_id'],anomalies=request.form['anomalies'],breed=request.form['cow_breed'],date_of_birth=request.form['date_of_birth'],weight=request.form['weight'],time_of_birth=request.form['time_of_birth'],gender=request.form['gender'],image=filename,admin_national_id=admin.national_id)
            newRecord.save()
            flash('success')
            return render_template('calvingrecords.html')
        return render_template('calvingrecords.html')
@app.route("/deathrecord",methods=["POST","GET"])
def deathrecord():
    if request.method=="POST":
        if 'admin' in session:
            admin=admins.query.filter(admins.username==session['admin']).first()
            if deathrecords.query.filter(deathrecords.death_record_id==request.form['cowtag_id']).first():
                flash('cow already exist')
                return redirect(url_for('deathrecord'))
            newdeath=deathrecords(death_record_id=uuid.uuid4(),admin_national_id=admin.national_id,cow_tag_id=request.form['cowtag_id'],cause_of_death=request.form['cause_of_death'],date_of_death=request.form['date_of_death'])
            flash('success')
            newdeath.save()
            return render_template("death.html")
        return render_template("death.html")
    return render_template("death.html")

@app.route('/staff',methods=["POST","GET"])
def staffs():
    if 'admin' in session:
        if request.method == "POST":
            if(staff.query.filter(staff.staff_id==request.form['staff_id'])).first():
                flash("Staff_ID exists")
                return render_template('staff.html')
            nrecords=staff(first_name=request.form['first_name'],staff_id=request.form['staff_id'],last_name=request.form['last_name'],other_name=request.form['other_names'],national_id=request.form['national_id'])
            flash("Record successfully added")
            nrecords.save()
            return redirect(url_for('staffs'))
        return render_template('staff.html')

@app.route('/changepassword',methods=['POST','GET'])
def changepassword():
    if 'user' in session:
        if request.method=='POST':
            if not request.form['old_password'] or not request.form['new_password'] or not request.form['confirm_password']:
                flash('please fill all the required details')
            elif request.form['new_password'] != request.form['confirm_password']:
                flash('passwords don\'t match!')
            farmer=farmers.query.filter(farmers.username==session['user']).first()
            if sha256_crypt.verify(request.form['old_password'],farmer.password):
                farmer.password=sha256_crypt.encrypt(request.form['new_password'])
                farmer.save()
                flash('password successfully changed')
                return redirect(url_for('login'))
            flash('wrong old password')
            return redirect(url_for('login'))
    elif 'admin' in session:
        if request.method=='POST':
            if not request.form['old_password'] or not request.form['new_password'] or not request.form['confirm_password']:
                flash('please fill all the required details')
            elif request.form['new_password'] != request.form['confirm_password']:
                flash('passwords don\'t match!')
            admin=admins.query.filter(admins.username==session['admin']).first()
            if sha256_crypt.verify(request.form['old_password'],admin.password):
                admin.password=sha256_crypt.encrypt(request.form['new_password'])
                admin.save()
                flash('password successfully changed')
                return redirect(url_for('adminlogin'))
            flash('wrong old password')
            return redirect(url_for('adminlogin'))

@app.route('/farmers')
def farmer():
    farmer = farmers.query.all()
    return render_template('users.html',farmers=farmer)









@app.route('/filter')
def filter():
    # startdate = request.form['start']
    # enddate = request.form['end']
    query = cowsinfo.query.filter(cowsinfo.date_of_birth.between('09/05/2021 8:46 PM', '10/05/2021 8:46 PM')).all()
    for cow in query:
        print(cow.date_of_birth)
    print(query)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port='8000' )