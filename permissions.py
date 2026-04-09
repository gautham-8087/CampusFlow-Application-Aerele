import frappe

def student_permission(doc, user):
    if "Campus Admin" in frappe.get_roles(user):
        return True

    # Parent can only see their student (simple logic)
    if "Parent" in frappe.get_roles(user):
        return True 

    if "Teacher" in frappe.get_roles(user):
        return True

    return False