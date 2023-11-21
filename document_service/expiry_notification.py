import frappe

def notify(doc,method):
    customer = frappe.get_doc('Customer',doc.name)
    documents = customer.custom_document_table
    email = customer.custom_emailid

    for document in documents:
        
        if document.expiry_date:
            selected_date_obj = frappe.utils.getdate(document.expiry_date)
            current_date = frappe.utils.nowdate()
            seven_days = frappe.utils.add_days(current_date, 7)
            one_month = frappe.utils.add_months(current_date, 1)

            if selected_date_obj == seven_days:
                send_email_notification(doc.name,email,seven_days,document.document_type,document.attach_file)
            if selected_date_obj == one_month:
                send_email_notification(doc.name,email,one_month,document.document_type,document.attach_file)
            if selected_date_obj == current_date:
                send_email_notification(doc.name,email,"Today",document.document_type,document.attach_file)



def send_email_notification(customer,email,days, document_type,attachment):
    recipients = [email,'fadilsiddique@gmail.com']
    frappe.sendmail(
        recipients = recipients,
        subject = f"{document_type} Expiry In {days} days",
        message = f"Dear {customer},\n\nYour {document_type} will be expired in days. Please Contact Alfaaj Businessmen Services For More",
        attachments = [{'file_url':attachment}]
    )
    
def notify_queue():
    
    frappe.enqueue(
        notify,
        queue="default"
    )