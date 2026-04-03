import frappe

def create_student_on_approval(doc, method):
    if doc.status == "Approved":
        if not frappe.db.exists("Student", {"student_name": doc.applicant_name}):
            student = frappe.get_doc({
                "doctype": "Student",
                "student_name": doc.applicant_name,
                "program": doc.program,
                "guardian_name": doc.guardian_name,
                "contact_number": doc.contact_number
            })
            student.insert(ignore_permissions=True)

