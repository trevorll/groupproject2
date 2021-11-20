from flask import *
from dotenv import *
from requests.models import HTTPBasicAuth
from flask_migrate import Migrate
from models import *
from flask_mpesa import MpesaAPI
from flask_mail import Message,Mail
import os


app=Flask(__name__, static_folder="public")
mpesa_api=MpesaAPI()
load_dotenv()

app.config["API_ENVIRONMENT"] = os.getenv('API_ENVIRONMENT')
app.config["APP_KEY"] = os.getenv('APP_KEY') # App_key from developers portal
app.config["APP_SECRET"] = os.getenv('APP_SECRET') #App_Secret from developers portal
mpesa_api.init_app(app)

POSTGRES = {
    'user':'godwill',
    'pw' : 'godwill63',
    'port' :'5432',
    'host' : 'localhost',
    'db' : 'database1'
}
UPLOAD_FOLDER=os.path.dirname(os.path.abspath(__file__)) + "/public/img"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.secret_key= 'godwill8764'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SESSION_COOKIE_NAME'] = 'session_lvning'
db.init_app(app)
migrate = Migrate(app,db)


app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USE_TLS=False,
    MAIL_USERNAME='gtreksolution@gmail.com',
    MAIL_PASSWORD='godwill8764'

)
mail=Mail(app)
db.init_app(app)
