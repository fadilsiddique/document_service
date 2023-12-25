import frappe
import json

@frappe.whitelist()
def make_sales_invoice(customer,request_name,items):
    
    items = json.loads(items)
    doc = frappe.get_doc({
        'doctype':'Sales Invoice',
        'customer':customer,
        'custom_application_request':request_name,
    })

    for item in items:
        doc.append("items",{
            'item_code':item['application_type'],
            'qty':1
        })

    doc.insert()
    doc.save()

    return doc

def update_request_status_after_invoice_generated(doc,event):

    if doc.custom_application_request:

        frappe.db.set_value('Application Request',doc.custom_application_request,'status','Invoice Generated')

def update_request_status_after_payment(doc,event):

    if doc.custom_application_request:

        if doc.status == 'Paid':
            frappe.db.set_value('Application Request',doc.custom_application_request,'status','Payment Received')
        elif doc.status == 'Partly Paid':
            frappe.db.set_value('Application Request',doc.custom_application_request,'status','Partial Payment Received')


