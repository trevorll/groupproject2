

from flask import render_template
from app import app


@app.route('/login_help')
def login_help():
    return render_template('help/help1.html')


@app.route('/buy_cow_help')
def buy_cow_help():
    return render_template('help/help2.html')


@app.route('/order_milk_help')
def order_milk_help():
    return render_template('help/help3.html')


@app.route('/reset_pass_help')
def reset_pass_help():
    return render_template('help/help4.html')
