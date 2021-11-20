from flask_migrate import Migrate
from flask_script import Manager,Server
from app import app,db

manager=Manager(app)
migrate=Migrate(app,db)
manager.add_command("runserver", Server(host='0.0.0.0', port=8000,ssl_crt='cert.pem', ssl_key='key.pem'))


if __name__=="__main__":
    app.config['DEBUG']=True
    manager.run()