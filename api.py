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
            
@frappe.whitelist(allow_guest = True)
def get_student_fee(student):
    payments = frappe.get_all(
        "Fee Payment",
        filters={"student": student},
        fields=["amount_paid"]
    )

    total = sum([p.amount_paid for p in payments])
    return total


import frappe

def process_fee_background(student):
    frappe.logger().info(f"Processing fee for {student}")

frappe.enqueue(
    "campusflow.api.process_fee_background",
    student=doc.student
)