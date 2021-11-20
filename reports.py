from app import app
from models import *
from fpdf import FPDF
from flask.wrappers import Response

def test():
    #save the transaction code in the database
    data = {'Body': {'stkCallback': {'MerchantRequestID': '4827-3022771-1', 'CheckoutRequestID': 'ws_CO_201020211417243449', 'ResultCode': 0, 'ResultDesc': 'The service request is processed successfully.', 'CallbackMetadata': {'Item': [{'Name': 'Amount', 'Value': 1.0}, {'Name': 'MpesaReceiptNumber', 'Value': 'PJK9HS9EZV'}, {'Name': 'Balance'}, {'Name': 'TransactionDate', 'Value': 20211020141737}, {'Name': 'PhoneNumber', 'Value': 254702514570}]}}}}
    transction_code=data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    amount=data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
    return transction_code

@app.route('/cowinfo_report',methods=['GET','POST'])
def cowinfo_report():
    results = cowsinfo.query.all()
    pdf = FPDF()
    pdf.add_page()
    
    page_width = pdf.w - 2 * pdf.l_margin
    
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Cows information', align='C')
    pdf.ln(10)

    
    
    col_width = page_width/5
    
    pdf.ln(1)
    pdf.cell(col_width,4, "cow tag",border=1)
    pdf.cell(col_width,4, "cowbreed",border=1)
    pdf.cell(col_width,4, "gender", border=1)
    pdf.cell(col_width,4, "weight",border=1)
    pdf.cell(col_width,4, "date of birth", border=1)
    pdf.ln(4)
    pdf.set_font('Courier', '', 12)

    
    th = pdf.font_size

    for row in results:
        date=row.date_of_birth
        pdf.cell(col_width, th, row.cow_tag_id, border=1)
        pdf.cell(col_width, th, row.cow_breed, border=1)
        pdf.cell(col_width, th, row.cow_gender, border=1)
        pdf.cell(col_width, th, row.weight,border=1)
        pdf.cell(col_width, th, date[:10], border=1)
        pdf.ln(th)
    
    pdf.ln(10)
    
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=cow_info.pdf'})
@app.route('/milksale_report',methods=['GET','POST'])
def milksale_report():
    results = milk_sale.query.all()
    pdf = FPDF(orientation="l")
    pdf.add_page()
    
    page_width = pdf.w - 2 * pdf.l_margin
    
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Milk Sale Report', align='C')
    pdf.ln(10)

    
    
    col_width = page_width/6
    
    pdf.ln(1)
    pdf.cell(col_width,4, "ID of seller",border=1)
    pdf.cell(col_width,4, "milk_quantity",border=1)
    pdf.cell(col_width,4, "milk_price", border=1)
    pdf.cell(col_width,4, "buyer\'s_phone",border=1)
    pdf.cell(col_width,4, "transaction code",border=1)
    pdf.cell(col_width,4, "date of sale", border=1)
    pdf.ln(4)
    pdf.set_font('Courier', '', 12)

    
    th = pdf.font_size
    

    for row in results:
        quantity=str(row.milk_quantity)
        date= row.milk_sale_date
        processed_date = date[:4]+'/' + date[5:7]+ '/' + date[8:10]
        pdf.cell(col_width, th, str(row.admin_national_id), border=1)
        pdf.cell(col_width, th, quantity[:4], border=1)
        pdf.cell(col_width, th, str(row.milk_price), border=1)
        pdf.cell(col_width, th, row.farmer_phone_number,border=1)
        pdf.cell(col_width, th, row.transaction_code, border=1)
        pdf.cell(col_width, th, processed_date,border=1)
        pdf.ln(th)
    
    pdf.ln(10)
    
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=milk_sale.pdf'})

@app.route('/milkcollection_report',methods=['GET','POST'])
def milkcollection_report():
    results = milk_collection.query.all()
    pdf = FPDF(orientation="l")
    pdf.add_page()
    
    page_width = pdf.w - 2 * pdf.l_margin
    
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Milk Collection Report', align='C')
    pdf.ln(10)

    
    
    col_width = page_width/6
    
    pdf.ln(1)
    pdf.cell(col_width,4, "Cow Tag Id",border=1)
    pdf.cell(col_width,4, "milk_quantity",border=1)
    pdf.cell(col_width,4, "milk_quality", border=1)
    # pdf.cell(col_width,4, "Milking Personel",border=1)
    pdf.cell(col_width,4, "Admin National Id",border=1)
    pdf.cell(col_width,4, "date of collection", border=1)
    pdf.cell(col_width,4, "time of collection", border=1)
    pdf.ln(4)
    pdf.set_font('Courier', '', 12)

    
    th = pdf.font_size
    

    for row in results:
        pdf.cell(col_width, th, row.cow_tag_id, border=1)
        pdf.cell(col_width, th, str(row.milk_quantity), border=1)
        pdf.cell(col_width, th, row.milk_quality, border=1)
        # pdf.cell(col_width, th, row.milking_personel,border=1)
        pdf.cell(col_width, th, str(row.admin_national_id),border=1)
        pdf.cell(col_width, th, row.milk_collection_date, border=1)
        pdf.cell(col_width, th, row.milk_collection_time,border=1)
        pdf.ln(th)
    
    pdf.ln(10)
    
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=milk_collection.pdf'})
@app.route('/insemination_report',methods=['GET','POST'])
def inseminations_report():
    results = inseminations.query.all()
    pdf = FPDF(orientation="l")
    pdf.add_page()
    
    page_width = pdf.w - 2 * pdf.l_margin
    
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Insemination Report', align='C')
    pdf.ln(10)

    
    
    col_width = page_width/7
    
    pdf.ln(1)
    pdf.cell(col_width,4, "Cow Tag Id",border=1)
    pdf.cell(col_width,4, "Insemination Date",border=1)
    pdf.cell(col_width,4, "breed", border=1)
    pdf.cell(col_width,4, "Sperm Dose",border=1)
    pdf.cell(col_width,4, "Insem Officer",border=1)
    pdf.cell(col_width,4, "Number", border=1)
    pdf.cell(col_width,4, "Insemination Age", border=1)
    pdf.ln(4)
    pdf.set_font('Courier', '', 12)

    
    th = pdf.font_size
    

    for row in results:
        date = str(row.date_of_insemination)
        pdf.cell(col_width, th, row.cow_tag_id, border=1)
        pdf.cell(col_width, th, date[:10], border=1)
        pdf.cell(col_width, th, row.breed, border=1)
        pdf.cell(col_width, th, str(row.sperm_dose),border=1)
        pdf.cell(col_width, th, row.insemination_officer,border=1)
        pdf.cell(col_width, th, str(row.no_of_inseminations), border=1)
        pdf.cell(col_width, th, str(row.age_at_insemination),border=1)
        pdf.ln(th)
    
    pdf.ln(10)
    
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=insemination.pdf'})
@app.route('/cowsfeedinventory_report',methods=['GET','POST'])
def cowsfeedinventory_report():
    results = cowfeedinventory.query.all()
    pdf = FPDF(orientation="p")
    pdf.add_page()
    
    page_width = pdf.w - 2 * pdf.l_margin
    
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Cows Feed Inventory Report', align='C')
    pdf.ln(10)

    
    
    col_width = page_width/5
    
    pdf.ln(1)
    pdf.cell(col_width,4, "Feed Name",border=1)
    pdf.cell(col_width,4, "Feed Type",border=1)
    pdf.cell(col_width,4, "Quantity(kg)", border=1)
    pdf.cell(col_width,4, "Supplier Name",border=1)
    pdf.cell(col_width,4, "Supplier Contact",border=1)
    pdf.ln(4)
    pdf.set_font('Courier', '', 12)

    
    th = pdf.font_size
    

    for row in results:
        pdf.cell(col_width, th, row.feed_name, border=1)
        pdf.cell(col_width, th, row.type_of_feed, border=1)
        pdf.cell(col_width, th, row.feed_quantity, border=1)
        pdf.cell(col_width, th, row.supplier_name,border=1)
        pdf.cell(col_width, th, row.supplier_contact,border=1)
        pdf.ln(th)
    
    pdf.ln(10)
    
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=cowfeedinventory.pdf'})
@app.route('/cowsfeeding_report',methods=['GET','POST'])
def cowsfeeding_report():
    results = cowfeeds.query.all()
    pdf = FPDF(orientation="l")
    pdf.add_page()
    
    page_width = pdf.w - 2 * pdf.l_margin
    
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Cow Feeding Report', align='C')
    pdf.ln(10)

    
    
    col_width = page_width/5
    
    pdf.ln(1)
    pdf.cell(col_width,4, "Cow Tag Id", border=1)
    pdf.cell(col_width,4, "Feed Type",border=1)
    pdf.cell(col_width,4, "Quantity given(kg)",border=1)
    pdf.cell(col_width,4, "Feeding Time", border=1)
    pdf.cell(col_width,4, "Feeding Personel(ID)",border=1)
    pdf.ln(4)
    pdf.set_font('Courier', '', 12)

    
    th = pdf.font_size
    

    for row in results:
        pdf.cell(col_width, th, row.cow_tag_id, border=1)
        pdf.cell(col_width, th, row.feed_type, border=1)
        pdf.cell(col_width, th, row.quantity_given, border=1)
        pdf.cell(col_width, th, row.time_of_feeding, border=1)
        pdf.cell(col_width, th, row.feeding_personel_id,border=1)
        pdf.ln(th)
    pdf.ln(10)
    
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=cowfeeding.pdf'})
@app.route('/vaccineinventory_report',methods=['GET','POST'])
def vaccineinventory_report():
    results = vaccineinventories.query.all()
    pdf = FPDF(orientation="l")
    pdf.add_page()
    
    page_width = pdf.w - 2 * pdf.l_margin
    
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Vaccine Inventory Report', align='C')
    pdf.ln(10)

    
    
    col_width = page_width/6
    
    pdf.ln(1)
    pdf.cell(col_width,4, "Vaccine Name", border=1)
    pdf.cell(col_width,4, "Disease Treated",border=1)
    pdf.cell(col_width,4, "Doses available",border=1)
    pdf.cell(col_width,4, "Date In", border=1)
    pdf.cell(col_width,4, "Supplier\'s Name",border=1)
    pdf.cell(col_width,4, "Reciever\'s ID",border=1)
    pdf.ln(4)
    pdf.set_font('Courier', '', 12)

    
    th = pdf.font_size
    

    for row in results:
        date = str(row.date_in)
        pdf.cell(col_width, th, row.vaccine_name, border=1)
        pdf.cell(col_width, th, row.disease_treated, border=1)
        pdf.cell(col_width, th, str(row.available_vaccine_quantity), border=1)
        pdf.cell(col_width, th, date[:10], border=1)
        pdf.cell(col_width, th, row.supplier_name,border=1)
        pdf.cell(col_width, th, str(row.admin_national_id),border=1)
        pdf.ln(th)
    pdf.ln(10)
    
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=vaccineinventory.pdf'})
@app.route('/healthinfo_report',methods=['GET','POST'])
def healthinfo_report():
    results = healthinfo.query.all()
    pdf = FPDF(orientation="l")
    pdf.add_page()
    
    page_width = pdf.w - 2 * pdf.l_margin
    
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Cow Treatment Report', align='C')
    pdf.ln(10)

    
    
    col_width = page_width/8
    
    pdf.ln(1)
    pdf.cell(col_width,4, "Cow Tag Id", border=1)
    pdf.cell(col_width,4, "Vaccine Name",border=1)
    pdf.cell(col_width,4, "Date",border=1)
    pdf.cell(col_width,4, "Vet Name", border=1)
    pdf.cell(col_width,4, "Weight", border=1)
    pdf.cell(col_width,4, "Prescription",border=1)
    pdf.cell(col_width,4, "Disease",border=1)
    pdf.cell(col_width,4, "Duration",border=1)
    pdf.ln(4)
    pdf.set_font('Courier', '', 12)

    
    th = pdf.font_size
    

    for row in results:
        date=str(row.date_of_vaccination)
        pdf.cell(col_width, th, row.cow_tag_id, border=1)
        pdf.cell(col_width, th, row.vaccine_name, border=1)
        pdf.cell(col_width, th, date[:10], border=1)
        pdf.cell(col_width, th, row.vet_name, border=1)
        pdf.cell(col_width, th, row.weight,border=1)
        pdf.cell(col_width, th, row.prescription,border=1)
        pdf.cell(col_width, th, row.disease_treated,border=1)
        pdf.cell(col_width, th, row.treatment_duration,border=1)
        pdf.ln(th)
    pdf.ln(10)
    
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=healthinfo.pdf'})
@app.route('/calving_report',methods=['GET','POST'])
def calving_report():
    results = calvings.query.all()
    pdf = FPDF(orientation="l")
    pdf.add_page()
    
    page_width = pdf.w - 2 * pdf.l_margin
    
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Calving Report', align='C')
    pdf.ln(10)

    
    
    col_width = page_width/7
    
    pdf.ln(1)
    pdf.cell(col_width,4, "Cow Tag Id", border=1)
    pdf.cell(col_width,4, "Gender",border=1)
    pdf.cell(col_width,4, "Breed",border=1)
    pdf.cell(col_width,4, "Weight", border=1)
    pdf.cell(col_width,4, "anomalies", border=1)
    pdf.cell(col_width,4, "DOB",border=1)
    pdf.cell(col_width,4, "TOB",border=1)
    pdf.ln(4)
    pdf.set_font('Courier', '', 12)

    
    th = pdf.font_size
    

    for row in results:
        date = row.date_of_birth
        pdf.cell(col_width, th, row.cow_tag_id, border=1)
        pdf.cell(col_width, th, row.gender, border=1)
        pdf.cell(col_width, th, row.breed, border=1)
        pdf.cell(col_width, th, str(row.weight), border=1)
        pdf.cell(col_width, th, row.anomalies,border=1)
        pdf.cell(col_width, th, date[:10],border=1)
        pdf.cell(col_width, th, row.time_of_birth,border=1)
        pdf.ln(th)
    pdf.ln(10)
    
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=calving.pdf'})
@app.route('/death_report',methods=['GET','POST'])
def death_report():
    results = deathrecords.query.all()
    pdf = FPDF(orientation="l")
    pdf.add_page()
    
    page_width = pdf.w - 2 * pdf.l_margin
    
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Death Report', align='C')
    pdf.ln(10)

    
    
    col_width = page_width/3
    
    pdf.ln(1)
    pdf.cell(col_width,4, "Cow Tag Id", border=1)
    pdf.cell(col_width,4, "Cause of Death",border=1)
    pdf.cell(col_width,4, "Date of Death",border=1)
    pdf.ln(4)
    pdf.set_font('Courier', '', 12)

    
    th = pdf.font_size
    

    for row in results:
        pdf.cell(col_width, th, row.cow_tag_id, border=1)
        pdf.cell(col_width, th, row.cause_of_death, border=1)
        pdf.cell(col_width, th, row.date_of_death, border=1)
        pdf.ln(th)
    pdf.ln(10)
    
    pdf.set_font('Times','',10.0) 
    pdf.cell(page_width, 0.0, '- end of report -', align='C')
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=deathrecord.pdf'})