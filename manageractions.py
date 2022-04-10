from app import app
from flask import request, session, flash, redirect, url_for, render_template
from models import *
from config import *
from sqlalchemy import and_


@app.route('/approve_approval', methods=['GET', 'POST'])
def approve_approval():
    if 'manager' in session:
        if request.method == 'POST':
            approval_id = request.form['approval_id']
            approved = Approval.query.filter(
                Approval.appproval_id == approval_id).first()
            if approved.sold == True:
                sale = transactions.query.filter(
                    transactions.transaction_code == approved.transaction_code).first()
                cow = cowsinfo.query.filter(
                    and_(cowsinfo.cow_tag_id == approved.cow_tag_id, cowsinfo.cow_status == True)).first()
                if cow:
                    farmer = farmers.query.filter(
                        farmers.farmer_national_id == approved.farmer_id).first()
                    newSale = cow_sales(cow_tag_id=approved.cow_tag_id, cow_sale_date=sale.date, cow_price=sale.amount,
                                        admin_national_id=None, farmer_national_id=farmer.farmer_national_id, farmer_phone_number=farmer.phone_number, transaction_code=sale.transaction_code)

                    cow.sold = True
                    cow.cow_status = False
                    cow.cow_price = 0
                    db.session.delete(approved)
                    db.session.commit()
                    db.session.delete(sale)
                    db.session.commit()
                    msg = Message('Update on your cow purchase',
                                  sender='godwillkisia@noreply.com',
                                  body="Your purchase has been approved and you are required to pick the animal at the farm",
                                  recipients=[farmer.email])
                    mail.send(msg)
                    cow.save()
                    newSale.save()
                    db.session.commit()

                    flash('cow purchase successfully approved', 'success')

                    return redirect(url_for('display'))
                else:
                    farmer = farmers.query.filter(
                        farmers.farmer_national_id == approved.farmer_id).first()
                    msg = Message('Update on the cow sale',
                                  sender='godwillkisia@noreply.com',
                                  body="Sorry the cow has already been sold out you will be refunded the money within 24 hours or can buy another cow with the same price the come with this email and transaction id " +
                                  sale.transaction_code+" for further inquiries",
                                  recipients=[farmer.email])
                    mail.send(msg)
                    db.session.delete(approved)
                    db.session.commit()
                    flash('cow has already been sold ', 'warning')

                    return redirect(url_for('display'))
            elif approved.sold == False:
                cow = cowsinfo(cow_tag_id=approved.cow_tag_id, cow_breed=approved.cow_breed, cow_gender=approved.cow_gender, cow_status=approved.cow_status, cow_price=approved.cow_price, cow_image=approved.cow_image,
                               weight=approved.weight, admin_national_id=approved.admin_national_id, date_of_birth=approved.date_of_birth, meat=approved.meat, milk=approved.milk, pregnant=approved.pregnant, sold=approved.sold)
                admin = admins.query.filter(
                    admins.national_id == approved.admin_national_id).first()
                msg = Message('Update on the cow addition',
                              sender='godwillkisia@noreply.com',
                              body="The update has been successfull effected you can view cows to verify",
                              recipients=[admin.email])
                mail.send(msg)
                cow.save()
                db.session.delete(approved)
                db.session.commit()
                flash('Addition successfully effected', 'success')
                return redirect(url_for('display'))


@app.route('/decline_approval', methods=['GET', 'POST'])
def decline_approval():
    if 'manager' in session:
        if request.method == 'POST':
            approved = Approval.query.filter(
                Approval.appproval_id == request.form['decline_id']).first()
            # sale = transactions.query.filter(
            #     transactions.transaction_code == approved.transaction_code).first()
            decline_id = request.form['decline_id']
            cow = Approval.query.filter(
                Approval.appproval_id == decline_id).first()
            cowinf = cowsinfo.query.filter(
                cowsinfo.cow_tag_id == cow.cow_tag_id).first()
            if cowinf:
                farmer = farmers.query.filter(
                    farmers.farmer_national_id == approved.farmer_id).first()
                cowinf.cow_status = True
                cowinf.sold = False
                cowinf.cow_price = approved.cow_price
                msg = Message('Update on your cow purchase',
                              sender='godwillkisia@noreply.com',
                              recipients=[farmer.email])
                msg.html = render_template(
                    "response.html", user=farmer.username, message=request.form['response'])
                mail.send(msg)
                cowinf.save()
                db.session.delete(cow)
                db.session.commit()
                flash('Purchase declined', 'success')
                flash('addition declined', 'success')
                return redirect(url_for('display'))
            if cow.cow_image != '':
                path = os.path.join(UPLOAD_FOLDER, cow.cow_image)
                os.remove(path)
            admin = admins.query.filter(
                admins.national_id == approved.admin_national_id).first()
            msg = Message('Update on the cow addition',
                          sender='godwillkisia@noreply.com',
                          body="The update addition has been decline because " +
                          request.form['response'] +
                          " you can view cows to verify",
                          recipients=[admin.email])
            mail.send(msg)
            db.session.delete(cow)
            db.session.commit()
            flash('addition declined', 'success')
            return redirect(url_for('display'))


@app.route('/dispay', methods=['GET', 'POST'])
@app.route('/display/page/<int:page>')
def display(page=1):
    if 'manager' in session:
        const_per_page = 10
        notifications = Approval.query.count()
        pending_approvals = Approval.query.paginate(
            page, per_page=const_per_page)
        return render_template('approval.html', pending_approvals=pending_approvals, notifications=notifications)
