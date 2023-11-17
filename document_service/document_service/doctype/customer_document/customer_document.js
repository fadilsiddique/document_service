// Copyright (c) 2023, Upscape Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Customer Document", {
    // refresh(frm) {

    // },
});

frappe.ui.form.on("Document Table", {

    download: function (frm, cdt, cdn) {

        let row = locals[cdt][cdn]
        let url = row.attach_file

        fetch(url)
        .then(response => response.blob())
        .then(blob => {
            const link = document.createElement('a')
            link.href = URL.createObjectURL(blob)

            const fileName = url.substring(url.lastIndexOf('/') + 1);
            link.download = fileName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        })
        .catch(error => {
            console.error('Error downloading file:', error);
        })

    }
})