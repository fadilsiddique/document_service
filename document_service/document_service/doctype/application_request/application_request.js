// Copyright (c) 2023, Upscape Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Application Request", {
    refresh(frm) {
        frm.add_custom_button('Create Sales Invoice', () => {
            frappe.call({
                method: 'document_service.api.make_sales_invoice',
                args: {
                    customer: frm.doc.customer,
                    request_name: frm.doc.name,
                    items: frm.doc.application_type
                },
                freeze: true,
                callback: (r) => {
                    frappe.set_route('Form', 'Sales Invoice', r.message.name)
                }
            })
        })

    },
});
