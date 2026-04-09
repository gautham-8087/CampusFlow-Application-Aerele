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
            
# @frappe.whitelist(allow_guest = True)
# def get_student_fee(student):
#     payments = frappe.get_all(
#         "Fee Payment",
#         filters={"student": student},
#         fields=["amount_paid"]
#     )

#     total = sum([p.amount_paid for p in payments])
#     return total

    
# @frappe.whitelist(allow_guest=True)
# def get_attendance(student):
#     records = frappe.get_all(
#         "Attendance Detail",
#         filters={"student": student},
#         fields=["status"]
#     )

#     total = len(records)
#     present = len([r for r in records if r.status == "Present"])
#     absent = len([r for r in records if r.status == "Absent"])

#     return {
#         "total_classes": total,
#         "present": present,
#         "absent": absent,
#         "percentage": (present / total * 100) if total > 0 else 0
#     }

@frappe.whitelist(allow_guest=True)
def get_student_details(student):
    doc = frappe.get_doc("Student", student)

    # if doc.grade != "1":
    #     frappe.throw("Student is not in Grade 1") 

    return {
        "student_id": doc.name,
        "student_name": doc.student_name,
        "program": doc.program,
        "contact": doc.contact_number,
        "guardian": doc.guardian_name,
        "total_fee": doc.total_fee
    }

# Below APIs for Dashboard

@frappe.whitelist(allow_guest=True)
def get_total_students():
    return frappe.db.count("Student")


@frappe.whitelist(allow_guest=True)
def get_total_collected():
    result = frappe.db.sql("""
        SELECT IFNULL(SUM(amount_paid), 0)
        FROM `tabFee Payment`
        WHERE docstatus = 1
    """)
    
    return result[0][0] or 0


@frappe.whitelist(allow_guest=True)
def get_pending_fees():
    total_fee = frappe.db.sql("""
        SELECT IFNULL(SUM(total_fee), 0)
        FROM `tabStudent`
    """)[0][0]

    collected = frappe.db.sql("""
        SELECT IFNULL(SUM(amount_paid), 0)
        FROM `tabFee Payment`
        WHERE docstatus = 1
    """)[0][0]

    return total_fee - collected


@frappe.whitelist(allow_guest=True)
def get_fully_paid_students():
    return frappe.db.sql("""
        SELECT COUNT(*) FROM (
            SELECT 
                s.name,
                IFNULL(SUM(f.amount_paid), 0) AS paid,
                MAX(s.total_fee) AS total_fee
            FROM `tabStudent` s
            LEFT JOIN `tabFee Payment` f 
                ON s.name = f.student AND f.docstatus = 1
            GROUP BY s.name
            HAVING paid >= total_fee
        ) AS t
    """)[0][0]


@frappe.whitelist(allow_guest=True)
def get_partial_students():
    return frappe.db.sql("""
        SELECT COUNT(*) FROM (
            SELECT 
                s.name,
                IFNULL(SUM(f.amount_paid), 0) AS paid,
                MAX(s.total_fee) AS total_fee
            FROM `tabStudent` s
            LEFT JOIN `tabFee Payment` f 
                ON s.name = f.student AND f.docstatus = 1
            GROUP BY s.name
            HAVING paid > 0 AND paid < total_fee
        ) AS t
    """)[0][0]


@frappe.whitelist(allow_guest=True)
def get_unpaid_students():
    return frappe.db.sql("""
        SELECT COUNT(*) FROM (
            SELECT 
                s.name,
                IFNULL(SUM(f.amount_paid), 0) AS paid
            FROM `tabStudent` s
            LEFT JOIN `tabFee Payment` f 
                ON s.name = f.student AND f.docstatus = 1
            GROUP BY s.name
            HAVING paid = 0
        ) AS t
    """)[0][0]






# # -------------------------------
# # 🎓 STUDENT CREATION
# # -------------------------------
# def create_student_on_approval(doc, method):
#     if doc.status != "Approved":
#         return

#     if frappe.db.exists("Student", {"student_name": doc.applicant_name}):
#         return

#     frappe.get_doc({
#         "doctype": "Student",
#         "student_name": doc.applicant_name,
#         "program": doc.program,
#         "guardian_name": doc.guardian_name,
#         "contact_number": doc.contact_number
#     }).insert(ignore_permissions=True)


# # -------------------------------
# # 📘 STUDENT DETAILS API
# # -------------------------------
# @frappe.whitelist(allow_guest=True)
# def get_student_details(student):
#     doc = frappe.get_doc("Student", student)

#     return {
#         "student_id": doc.name,
#         "student_name": doc.student_name,
#         "program": doc.program,
#         "contact": doc.contact_number,
#         "guardian": doc.guardian_name,
#         "total_fee": doc.total_fee
#     }


# # -------------------------------
# # 📊 COMMON HELPER FUNCTIONS
# # -------------------------------
# def get_total_fee():
#     return frappe.db.sql("""
#         SELECT IFNULL(SUM(total_fee), 0) FROM `tabStudent`
#     """)[0][0]


# def get_total_collected_amount():
#     return frappe.db.sql("""
#         SELECT IFNULL(SUM(amount_paid), 0)
#         FROM `tabFee Payment`
#         WHERE docstatus = 1
#     """)[0][0]


# def get_payment_summary():
#     return frappe.db.sql("""
#         SELECT 
#             s.name,
#             IFNULL(SUM(f.amount_paid), 0) AS paid,
#             MAX(s.total_fee) AS total_fee
#         FROM `tabStudent` s
#         LEFT JOIN `tabFee Payment` f 
#             ON s.name = f.student AND f.docstatus = 1
#         GROUP BY s.name
#     """, as_dict=True)


# # -------------------------------
# # 📊 DASHBOARD APIs
# # -------------------------------
# @frappe.whitelist(allow_guest=True)
# def get_total_students():
#     return frappe.db.count("Student")


# @frappe.whitelist(allow_guest=True)
# def get_total_collected():
#     return get_total_collected_amount()


# @frappe.whitelist(allow_guest=True)
# def get_pending_fees():
#     return get_total_fee() - get_total_collected_amount()


# @frappe.whitelist(allow_guest=True)
# def get_fully_paid_students():
#     data = get_payment_summary()
#     return sum(1 for d in data if d.paid >= d.total_fee)


# @frappe.whitelist(allow_guest=True)
# def get_partial_students():
#     data = get_payment_summary()
#     return sum(1 for d in data if 0 < d.paid < d.total_fee)


# @frappe.whitelist(allow_guest=True)
# def get_unpaid_students():
#     data = get_payment_summary()
#     return sum(1 for d in data if d.paid == 0)