import frappe
from datetime import datetime

def notify():
    customer = frappe.db.get_list('Customer',fields=['name','custom_emailid'])

    for i in customer:
        email = i.custom_emailid
        check_document_expiry(i.name,email)

def check_document_expiry(customername,email):
    
    documents = frappe.db.get_all(
        'Document Table',
        filters = {'parent':customername,'parenttype':'Customer'},
        fields = ['name','document_type','expiry_date','attach_file']
    )

    for document in documents:
        if document.expiry_date:
            selected_date_obj = document.expiry_date
            current_date =  datetime.strptime(frappe.utils.nowdate(),'%Y-%m-%d').date() 
            seven_days = frappe.utils.add_days(current_date, 7)
            one_month = frappe.utils.add_months(current_date, 1)

            if selected_date_obj == seven_days:
                send_email_notification(customername,email,seven_days,document.document_type,document.attach_file)
            elif selected_date_obj == one_month:
                send_email_notification(customername,email,one_month,document.document_type,document.attach_file)
            elif selected_date_obj == current_date:
                send_email_notification(customername,email,current_date,document.document_type,document.attach_file)
            
def send_email_notification(customer,email,days, document_type,attachment):
    recipients = [email,'fadilsiddique@gmail.com']
    frappe.sendmail(
        recipients = recipients,
        subject = f"{document_type} Expiry In {days} days",
        message = f"Dear {customer},\n\nYour {document_type} will be expired in {days} days. Please Contact Alfaaj Businessmen Services For More",
        attachments = [{'file_url':attachment}]
    )
    
def notify_queue():
    frappe.enqueue(
        notify,
        queue="default"
    )