from app import app
from models import *
from fpdf import FPDF
from flask import request, flash, render_template, session
from flask.wrappers import Response
from sqlalchemy import and_


def test():
    # save the transaction code in the database
    data = {'Body': {'stkCallback': {'MerchantRequestID': '4827-3022771-1', 'CheckoutRequestID': 'ws_CO_201020211417243449', 'ResultCode': 0, 'ResultDesc': 'The service request is processed successfully.', 'CallbackMetadata': {
        'Item': [{'Name': 'Amount', 'Value': 1.0}, {'Name': 'MpesaReceiptNumber', 'Value': 'PJK9HS9EZV'}, {'Name': 'Balance'}, {'Name': 'TransactionDate', 'Value': 20211020141737}, {'Name': 'PhoneNumber', 'Value': 254702514570}]}}}}
    transction_code = data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    amount = data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
    return transction_code


@app.route('/cowinfo_report', methods=['GET', 'POST'])
def cowinfo_report():
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        if request.method == 'POST':
            results = None
            startdate = request.form['start']
            enddate = request.form['end']
            if not startdate or not enddate:
                results = cowsinfo.query.order_by(cowsinfo.date_of_birth.asc())
            elif startdate and enddate:
                results = cowsinfo.query.filter(cowsinfo.date_of_birth.between(
                    startdate, enddate)).order_by(cowsinfo.date_of_birth.asc())
            if results.count() == 0:
                flash("oops no records found for that period")
                return render_template('errors/error.html', messages='adminlogin')
            pdf = FPDF()
            pdf.add_page()

            page_width = pdf.w - 2 * pdf.l_margin

            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(page_width, 0.0, 'Cows information', align='C')
            pdf.ln(10)

            col_width = page_width/5

            pdf.ln(1)
            pdf.cell(col_width, 4, "cow tag", border=1)
            pdf.cell(col_width, 4, "cowbreed", border=1)
            pdf.cell(col_width, 4, "gender", border=1)
            pdf.cell(col_width, 4, "weight", border=1)
            pdf.cell(col_width, 4, "date of birth", border=1)
            pdf.ln(4)
            pdf.set_font('Courier', '', 12)

            th = pdf.font_size

            for row in results:
                date = row.date_of_birth
                pdf.cell(col_width, th, row.cow_tag_id, border=1)
                pdf.cell(col_width, th, row.cow_breed, border=1)
                pdf.cell(col_width, th, row.cow_gender, border=1)
                pdf.cell(col_width, th, row.weight, border=1)
                pdf.cell(col_width, th, date[:10], border=1)
                pdf.ln(th)

            pdf.ln(10)

            pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')

            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=cow_info.pdf'})
        flash("oops not allowed")
        return render_template('errors/error1.html')
    flash("oops not allowed")
    return render_template('errors/error1.html')


@app.route('/milksale_report', methods=['GET', 'POST'])
def milksale_report():
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        if request.method == 'POST':
            results = None
            one = request.form['start']
            two = request.form['end']

            startdate = one[0:4] + one[5:7] + \
                one[8:10] + one[11:13] + one[14:16] + '00'
            enddate = two[0:4] + two[5:7] + two[8:10] + \
                two[11:13] + two[14:16] + '00'

            if not one or not two:
                results = milk_sale.query.filter(milk_sale.admin_national_id != None).order_by(
                    milk_sale.milk_sale_date.asc())
            elif startdate and enddate:
                results = milk_sale.query.filter(and_(milk_sale.admin_national_id != None, milk_sale.milk_sale_date.between(
                    startdate, enddate))).order_by(milk_sale.milk_sale_date.asc())
            if results.count() == 0:
                flash("oops no records found for that period")
                return render_template('errors/error.html', messages='adminlogin')
            pdf = FPDF(orientation="l")
            pdf.add_page()

            page_width = pdf.w - 2 * pdf.l_margin

            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(page_width, 0.0, 'Milk Sale Report', align='C')
            pdf.ln(10)

            col_width = page_width/6

            pdf.ln(1)
            pdf.cell(col_width, 4, "ID of seller", border=1)
            pdf.cell(col_width, 4, "milk_quantity", border=1)
            pdf.cell(col_width, 4, "milk_price", border=1)
            pdf.cell(col_width, 4, "buyer\'s_phone", border=1)
            pdf.cell(col_width, 4, "transaction code", border=1)
            pdf.cell(col_width, 4, "date of sale", border=1)
            pdf.ln(4)
            pdf.set_font('Courier', '', 12)

            th = pdf.font_size

            for row in results:
                quantity = str(row.milk_quantity)
                date = row.milk_sale_date
                processed_date = date[:4]+'/' + date[4:6] + '/' + date[6:8]
                pdf.cell(col_width, th, str(row.admin_national_id), border=1)
                pdf.cell(col_width, th, quantity[:4], border=1)
                pdf.cell(col_width, th, str(row.milk_price), border=1)
                pdf.cell(col_width, th, row.farmer_phone_number, border=1)
                pdf.cell(col_width, th, row.transaction_code, border=1)
                pdf.cell(col_width, th, processed_date, border=1)
                pdf.ln(th)

            pdf.ln(10)

            pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')

            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=milk_sale.pdf'})
        flash("oops not allowed")
        return render_template('errors/error1.html')
    flash("oops not allowed")
    return render_template('errors/error1.html')


@app.route('/milksale_reports', methods=['GET', 'POST'])
def milksale_reports():
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        if request.method == 'POST':
            results = None
            one = request.form['start']
            two = request.form['end']

            startdate = one[0:4] + one[5:7] + \
                one[8:10] + one[11:13] + one[14:16] + '00'
            enddate = two[0:4] + two[5:7] + two[8:10] + \
                two[11:13] + two[14:16] + '00'

            if not one or not two:
                results = milk_sale.query.filter(milk_sale.admin_national_id == None).order_by(
                    milk_sale.milk_sale_date.asc())
            elif startdate and enddate:
                results = milk_sale.query.filter(and_(milk_sale.admin_national_id == None, milk_sale.milk_sale_date.between(
                    startdate, enddate))).order_by(milk_sale.milk_sale_date.asc())
            if results.count() == 0:
                flash("oops no records found for that period")
                return render_template('errors/error.html', messages='adminlogin')
            pdf = FPDF(orientation="l")
            pdf.add_page()

            page_width = pdf.w - 2 * pdf.l_margin

            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(page_width, 0.0, 'Milk Sale Report', align='C')
            pdf.ln(10)

            col_width = page_width/6

            pdf.ln(1)
            pdf.cell(col_width, 4, "ID of seller", border=1)
            pdf.cell(col_width, 4, "milk_quantity", border=1)
            pdf.cell(col_width, 4, "milk_price", border=1)
            pdf.cell(col_width, 4, "buyer\'s_phone", border=1)
            pdf.cell(col_width, 4, "transaction code", border=1)
            pdf.cell(col_width, 4, "date of sale", border=1)
            pdf.ln(4)
            pdf.set_font('Courier', '', 12)

            th = pdf.font_size

            for row in results:
                quantity = str(row.milk_quantity)
                date = row.milk_sale_date
                processed_date = date[:4]+'/' + date[4:6] + '/' + date[6:8]
                pdf.cell(col_width, th, str(row.admin_national_id), border=1)
                pdf.cell(col_width, th, quantity[:4], border=1)
                pdf.cell(col_width, th, str(row.milk_price), border=1)
                pdf.cell(col_width, th, row.farmer_phone_number, border=1)
                pdf.cell(col_width, th, row.transaction_code, border=1)
                pdf.cell(col_width, th, processed_date, border=1)
                pdf.ln(th)

            pdf.ln(10)

            pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')

            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=milk_sale.pdf'})
        flash("oops not allowed")
        return render_template('errors/error1.html')
    flash("oops not allowed")
    return render_template('errors/error1.html')


@app.route('/cowsale_report', methods=['GET', 'POST'])
def cowsale_report():
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        if request.method == 'POST':
            results = None
            startdate = request.form['start']
            enddate = request.form['end']

            if not startdate or not enddate:
                results = cow_sales.query.order_by(
                    cow_sales.cow_sale_date.desc())
            elif startdate and enddate:
                results = cow_sales.query.filter(cow_sales.cow_sale_date.between(
                    startdate, enddate)).order_by(cow_sales.cow_sale_date.asc())
            if results.count() == 0:
                flash("oops no records found for that period")
                return render_template('errors/error.html', messages='adminlogin')
            pdf = FPDF(orientation="l")
            pdf.add_page()

            page_width = pdf.w - 2 * pdf.l_margin

            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(page_width, 0.0, 'Cow Sale Report', align='C')
            pdf.ln(10)

            col_width = page_width/6

            pdf.ln(1)
            pdf.cell(col_width, 4, "Cow Tag ID", border=1)
            pdf.cell(col_width, 4, "Cow Price", border=1)
            pdf.cell(col_width, 4, "Buyer\'s phone", border=1)
            pdf.cell(col_width, 4, "buyer\'s_national", border=1)
            pdf.cell(col_width, 4, "Transaction code", border=1)
            pdf.cell(col_width, 4, "date of sale", border=1)
            pdf.ln(4)
            pdf.set_font('Courier', '', 12)

            th = pdf.font_size

            for row in results:
                date = row.cow_sale_date
                processed_date = date[:4]+'/' + date[4:6] + '/' + \
                    date[6:8] + ' ' + date[8:10] + ':' + date[10:12]
                pdf.cell(col_width, th, row.cow_tag_id, border=1)
                pdf.cell(col_width, th, str(row.cow_price), border=1)
                pdf.cell(col_width, th, str(row.farmer_phone_number), border=1)
                pdf.cell(col_width, th, str(row.farmer_national_id), border=1)
                pdf.cell(col_width, th, row.transaction_code, border=1)
                pdf.cell(col_width, th, processed_date, border=1)
                pdf.ln(th)

            pdf.ln(10)

            pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')

            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=cow_sales.pdf'})
        flash("oops not allowed")
        return render_template('errors/error1.html')
    flash("oops not allowed")
    return render_template('errors/error1.html')


@app.route('/milkcollection_report', methods=['GET', 'POST'])
def milkcollection_report():
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        if request.method == 'POST':
            results = None
            startdate = request.form['start']
            enddate = request.form['end']
            if not startdate or not enddate:
                results = milk_collection.query.order_by(
                    milk_collection.milk_collection_date.asc())
            elif startdate and enddate:
                results = milk_collection.query.filter(milk_collection.milk_collection_date.between(
                    startdate, enddate)).order_by(milk_collection.milk_collection_date.asc())
            if results.count() == 0:
                flash("oops no records found for that period")
                return render_template('errors/error.html', messages='adminlogin')
            pdf = FPDF(orientation="l")
            pdf.add_page()

            page_width = pdf.w - 2 * pdf.l_margin

            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(page_width, 0.0, 'Milk Collection Report', align='C')
            pdf.ln(10)

            col_width = page_width/6

            pdf.ln(1)
            pdf.cell(col_width, 4, "Cow Tag Id", border=1)
            pdf.cell(col_width, 4, "milk_quantity", border=1)
            pdf.cell(col_width, 4, "milk_quality", border=1)
            # pdf.cell(col_width,4, "Milking Personel",border=1)
            pdf.cell(col_width, 4, "Admin National Id", border=1)
            pdf.cell(col_width, 4, "date of collection", border=1)
            pdf.cell(col_width, 4, "time of collection", border=1)
            pdf.ln(4)
            pdf.set_font('Courier', '', 12)

            th = pdf.font_size

            for row in results:
                pdf.cell(col_width, th, row.cow_tag_id, border=1)
                pdf.cell(col_width, th, str(row.milk_quantity), border=1)
                pdf.cell(col_width, th, row.milk_quality, border=1)
                # pdf.cell(col_width, th, row.milking_personel,border=1)
                pdf.cell(col_width, th, str(row.admin_national_id), border=1)
                pdf.cell(col_width, th,
                         row.milk_collection_date[:10], border=1)
                pdf.cell(col_width, th, row.milk_collection_time, border=1)
                pdf.ln(th)

            pdf.ln(10)

            pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')

            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=milk_collection.pdf'})
        flash("oops not allowed")
        return render_template('errors/error1.html')
    flash("oops not allowed")
    return render_template('errors/error1.html')


@app.route('/insemination_report', methods=['GET', 'POST'])
def inseminations_report():
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        if request.method == 'POST':
            if 'admin' in session or 'superadmin' in session or 'manager' in session:
                if request.method == 'POST':
                    results = None
                    startdate = request.form['start']
                    enddate = request.form['end']
                    if not startdate or not enddate:
                        results = inseminations.query.order_by(
                            inseminations.date_of_insemination.asc())
                    elif startdate and enddate:
                        results = inseminations.query.filter(inseminations.date_of_insemination.between(
                            startdate, enddate)).order_by(inseminations.date_of_insemination.asc())
                    if results.count() == 0:
                        flash("oops no records found for that period")
                        return render_template('errors/error.html', messages='adminlogin')
                    pdf = FPDF(orientation="l")
                    pdf.add_page()

                    page_width = pdf.w - 2 * pdf.l_margin

                    pdf.set_font('Times', 'B', 14.0)
                    pdf.cell(page_width, 0.0, 'Insemination Report', align='C')
                    pdf.ln(10)

                    col_width = page_width/7

                    pdf.ln(1)
                    pdf.cell(col_width, 4, "Cow Tag Id", border=1)
                    pdf.cell(col_width, 4, "Insemination Date", border=1)
                    pdf.cell(col_width, 4, "breed", border=1)
                    pdf.cell(col_width, 4, "Sperm Dose", border=1)
                    pdf.cell(col_width, 4, "Insem Officer", border=1)
                    pdf.cell(col_width, 4, "Number", border=1)
                    pdf.cell(col_width, 4, "Insemination Age", border=1)
                    pdf.ln(4)
                    pdf.set_font('Courier', '', 12)

                    th = pdf.font_size

                    for row in results:
                        date = str(row.date_of_insemination)
                        pdf.cell(col_width, th, row.cow_tag_id, border=1)
                        pdf.cell(col_width, th, date[:10], border=1)
                        pdf.cell(col_width, th, row.breed, border=1)
                        pdf.cell(col_width, th, str(row.sperm_dose), border=1)
                        pdf.cell(col_width, th,
                                 row.insemination_officer, border=1)
                        pdf.cell(col_width, th, str(
                            row.no_of_inseminations), border=1)
                        pdf.cell(col_width, th, str(
                            row.age_at_insemination), border=1)
                        pdf.ln(th)

                    pdf.ln(10)

                    pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')

            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=insemination.pdf'})
        flash("oops not allowed")
        return render_template('errors/error1.html')
    flash("oops not allowed")
    return render_template('errors/error1.html')


@app.route('/cowsfeedinventory_report', methods=['GET', 'POST'])
def cowsfeedinventory_report():
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        if request.method == 'POST':
            results = None
            startdate = request.form['start']
            enddate = request.form['end']
            if not startdate or not enddate:
                results = cowfeedinventory.query.order_by(
                    cowfeedinventory.date_in.asc())
            elif startdate and enddate:
                results = cowfeedinventory.query.filter(cowfeedinventory.date_in.between(
                    startdate, enddate)).order_by(cowfeedinventory.date_in.asc())
            if results.count() == 0:
                flash("oops no records found for that period")
                return render_template('errors/error.html', messages='adminlogin')
            pdf = FPDF(orientation="l")
            pdf.add_page()

            page_width = pdf.w - 2 * pdf.l_margin

            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(page_width, 0.0, 'Cows Feed Inventory Report', align='C')
            pdf.ln(10)

            col_width = page_width/6

            pdf.ln(1)
            pdf.cell(col_width, 4, "Food Name", border=1)
            pdf.cell(col_width, 4, "Food Type", border=1)
            pdf.cell(col_width, 4, "Quantity(kg)", border=1)
            pdf.cell(col_width, 4, "Supplier Name", border=1)
            pdf.cell(col_width, 4, "Supplier Contact", border=1)
            pdf.cell(col_width, 4, "Date in", border=1)
            pdf.ln(4)
            pdf.set_font('Courier', '', 12)

            th = pdf.font_size

            for row in results:
                date = row.date_in
                pdf.cell(col_width, th, row.food_name, border=1)
                pdf.cell(col_width, th, row.type_of_food, border=1)
                pdf.cell(col_width, th, row.feed_quantity, border=1)
                pdf.cell(col_width, th, row.supplier_name, border=1)
                pdf.cell(col_width, th, row.supplier_contact, border=1)
                pdf.cell(col_width, th, date[:10], border=1)
                pdf.ln(th)

            pdf.ln(10)

            pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')

            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=cowfeedinventory.pdf'})
        flash("oops not allowed")
        return render_template('errors/error1.html')
    flash("oops not allowed")
    return render_template('errors/error1.html')


@app.route('/cowsfeeding_report', methods=['GET', 'POST'])
def cowsfeeding_report():
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        if request.method == 'POST':
            results = None
            startdate = request.form['start']
            enddate = request.form['end']
            if not startdate or not enddate:
                results = cowfeeds.query.order_by(
                    cowfeeds.date_of_feeding.asc())
            elif startdate and enddate:
                results = cowfeeds.query.filter(cowfeeds.date_of_feeding.between(
                    startdate, enddate)).order_by(cowfeeds.date_of_feeding.asc())
            if results.count() == 0:
                flash("oops no records found for that period")
                return render_template('errors/error.html', messages='adminlogin')

            pdf = FPDF(orientation="l")
            pdf.add_page()

            page_width = pdf.w - 2 * pdf.l_margin

            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(page_width, 0.0, 'Cow Feeding Report', align='C')
            pdf.ln(10)

            col_width = page_width/6

            pdf.ln(1)
            pdf.cell(col_width, 4, "Cow Tag Id", border=1)
            pdf.cell(col_width, 4, "Feed Type", border=1)
            pdf.cell(col_width, 4, "Quantity given(kg)", border=1)
            pdf.cell(col_width, 4, "Feeding Time", border=1)
            pdf.cell(col_width, 4, "Feeding Personel(ID)", border=1)
            pdf.cell(col_width, 4, "Date of feeding", border=1)
            pdf.ln(4)
            pdf.set_font('Courier', '', 12)

            th = pdf.font_size

            for row in results:
                date = row.date_of_feeding
                pdf.cell(col_width, th, row.cow_tag_id, border=1)
                pdf.cell(col_width, th, row.type_of_food, border=1)
                pdf.cell(col_width, th, row.quantity_given, border=1)
                pdf.cell(col_width, th, row.time_of_feeding, border=1)
                pdf.cell(col_width, th, row.feeding_personel_id, border=1)
                pdf.cell(col_width, th, date[:10], border=1)
                pdf.ln(th)
            pdf.ln(10)

            pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')

            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=cowfeeding.pdf'})
        flash("oops not allowed")
        return render_template('errors/error1.html')
    flash("oops not allowed")
    return render_template('errors/error1.html')


@app.route('/vaccineinventory_report', methods=['GET', 'POST'])
def vaccineinventory_report():
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        if request.method == 'POST':
            results = None
            startdate = request.form['start']
            enddate = request.form['end']

            print(startdate)
            print(enddate)
            if not startdate or not enddate:
                results = vaccineinventories.query.order_by(
                    vaccineinventories.date_in.asc())
            elif startdate and enddate:
                results = vaccineinventories.query.filter(vaccineinventories.date_in.between(
                    startdate, enddate)).order_by(vaccineinventories.date_in.asc())
            if results.count() == 0:
                flash("oops no records found for that period")
                return render_template('errors/error.html', messages='adminlogin')
            pdf = FPDF(orientation="l")
            pdf.add_page()

            page_width = pdf.w - 2 * pdf.l_margin

            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(page_width, 0.0, 'Vaccine Inventory Report', align='C')
            pdf.ln(10)

            col_width = page_width/6

            pdf.ln(1)
            pdf.cell(col_width, 4, "Vaccine Name", border=1)
            pdf.cell(col_width, 4, "Disease Treated", border=1)
            pdf.cell(col_width, 4, "Doses available", border=1)
            pdf.cell(col_width, 4, "Date In", border=1)
            pdf.cell(col_width, 4, "Supplier\'s Name", border=1)
            pdf.cell(col_width, 4, "Reciever\'s ID", border=1)
            pdf.ln(4)
            pdf.set_font('Courier', '', 12)

            th = pdf.font_size

            for row in results:
                date = str(row.date_in)
                pdf.cell(col_width, th, row.vaccine_name, border=1)
                pdf.cell(col_width, th, row.disease_treated, border=1)
                pdf.cell(col_width, th, str(
                    row.available_vaccine_quantity), border=1)
                pdf.cell(col_width, th, date[:10], border=1)
                pdf.cell(col_width, th, row.supplier_name, border=1)
                pdf.cell(col_width, th, str(row.admin_national_id), border=1)
                pdf.ln(th)
            pdf.ln(10)

            pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')

            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=vaccineinventory.pdf'})
        flash("oops not allowed")
        return render_template('errors/error1.html')
    flash("oops not allowed")
    return render_template('errors/error1.html')


@app.route('/healthinfo_report', methods=['GET', 'POST'])
def healthinfo_report():
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        if request.method == 'POST':
            results = None
            startdate = request.form['start']
            enddate = request.form['end']
            if not startdate or not enddate:
                results = healthinfo.query.order_by(
                    healthinfo.date_of_vaccination.asc())
            elif startdate and enddate:
                results = healthinfo.query.filter(healthinfo.date_of_vaccination.between(
                    startdate, enddate)).order_by(healthinfo.date_of_vaccination)

            if results.count() == 0:
                flash("oops no records found for that period")
                return render_template('errors/error.html', messages='adminlogin')
            pdf = FPDF(orientation="l")
            pdf.add_page()

            page_width = pdf.w - 2 * pdf.l_margin

            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(page_width, 0.0, 'Cow Treatment Report', align='C')
            pdf.ln(10)

            col_width = page_width/8

            pdf.ln(1)
            pdf.cell(col_width, 4, "Cow Tag Id", border=1)
            pdf.cell(col_width, 4, "Vaccine Name", border=1)
            pdf.cell(col_width, 4, "Date", border=1)
            pdf.cell(col_width, 4, "Vet Name", border=1)
            pdf.cell(col_width, 4, "Weight", border=1)
            pdf.cell(col_width, 4, "Prescription", border=1)
            pdf.cell(col_width, 4, "Disease", border=1)
            pdf.cell(col_width, 4, "Duration", border=1)
            pdf.ln(4)
            pdf.set_font('Courier', '', 12)

            th = pdf.font_size

            for row in results:
                date = str(row.date_of_vaccination)
                pdf.cell(col_width, th, row.cow_tag_id, border=1)
                pdf.cell(col_width, th, row.vaccine_name, border=1)
                pdf.cell(col_width, th, date[:10], border=1)
                pdf.cell(col_width, th, row.vet_name, border=1)
                pdf.cell(col_width, th, row.weight, border=1)
                pdf.cell(col_width, th, row.prescription, border=1)
                pdf.cell(col_width, th, row.disease_treated, border=1)
                pdf.cell(col_width, th, row.treatment_duration, border=1)
                pdf.ln(th)
            pdf.ln(10)

            pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')

            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=healthinfo.pdf'})
        flash("oops not allowed")
        return render_template('errors/error1.html')
    flash("oops not allowed")
    return render_template('errors/error1.html')


@app.route('/calving_report', methods=['GET', 'POST'])
def calving_report():
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        if request.method == 'POST':
            results = None
            startdate = request.form['start']
            enddate = request.form['end']
            if not startdate or not enddate:
                results = calvings.query.order_by(
                    calvings.date_of_birth.asc())
            elif startdate and enddate:
                results = calvings.query.filter(calvings.date_of_birth.between(
                    startdate, enddate)).order_by(calvings.date_of_birth.asc())
            if results.count() == 0:
                flash("oops no records found for that period")
                return render_template('errors/error.html', messages='adminlogin')
            pdf = FPDF(orientation="l")
            pdf.add_page()

            page_width = pdf.w - 2 * pdf.l_margin

            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(page_width, 0.0, 'Calving Report', align='C')
            pdf.ln(10)

            col_width = page_width/7

            pdf.ln(1)
            pdf.cell(col_width, 4, "Cow Tag Id", border=1)
            pdf.cell(col_width, 4, "Gender", border=1)
            pdf.cell(col_width, 4, "Breed", border=1)
            pdf.cell(col_width, 4, "Weight", border=1)
            pdf.cell(col_width, 4, "anomalies", border=1)
            pdf.cell(col_width, 4, "DOB", border=1)
            pdf.cell(col_width, 4, "TOB", border=1)
            pdf.ln(4)
            pdf.set_font('Courier', '', 12)

            th = pdf.font_size

            for row in results:
                date = row.date_of_birth
                pdf.cell(col_width, th, row.cow_tag_id, border=1)
                pdf.cell(col_width, th, row.gender, border=1)
                pdf.cell(col_width, th, row.breed, border=1)
                pdf.cell(col_width, th, str(row.weight), border=1)
                pdf.cell(col_width, th, row.anomalies, border=1)
                pdf.cell(col_width, th, date[:10], border=1)
                pdf.cell(col_width, th, row.time_of_birth, border=1)
                pdf.ln(th)
            pdf.ln(10)

            pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')

            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=calving.pdf'})
        flash("oops not allowed")
        return render_template('errors/error1.html')
    flash("oops not allowed")
    return render_template('errors/error1.html')


@app.route('/death_report', methods=['GET', 'POST'])
def death_report():
    if 'admin' in session or 'superadmin' in session or 'manager' in session:
        if request.method == 'POST':
            results = None
            startdate = request.form['start']
            enddate = request.form['end']
            print(startdate)
            print(enddate)
            if not startdate or not enddate:
                results = deathrecords.query.order_by(
                    deathrecords.date_of_death.asc())
            elif startdate and enddate:
                results = deathrecords.query.filter(deathrecords.date_of_death.between(
                    startdate, enddate)).order_by(deathrecords.date_of_death)
            if results.count() == 0:
                flash("oops no records found for that period")
                return render_template('errors/error.html', messages='adminlogin')
            pdf = FPDF(orientation="l")
            pdf.add_page()

            page_width = pdf.w - 2 * pdf.l_margin

            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(page_width, 0.0, 'Death Report', align='C')
            pdf.ln(10)

            col_width = page_width/3

            pdf.ln(1)
            pdf.cell(col_width, 4, "Cow Tag Id", border=1)
            pdf.cell(col_width, 4, "Cause of Death", border=1)
            pdf.cell(col_width, 4, "Date of Death", border=1)
            pdf.ln(4)
            pdf.set_font('Courier', '', 12)

            th = pdf.font_size

            for row in results:
                pdf.cell(col_width, th, row.cow_tag_id, border=1)
                pdf.cell(col_width, th, row.cause_of_death, border=1)
                pdf.cell(col_width, th, row.date_of_death, border=1)
                pdf.ln(th)
            pdf.ln(10)

            pdf.set_font('Times', '', 10.0)
            pdf.cell(page_width, 0.0, '- end of report -', align='C')

            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=deathrecord.pdf'})
        flash("oops not allowed")
        return render_template('errors/error1.html')
    flash("oops not allowed")
    return render_template('errors/error1.html')
