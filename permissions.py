import frappe

def student_permission(doc, user):
    # Admin can access everything
    if "Campus Admin" in frappe.get_roles(user):
        return True

    # Parent can only see their student (simple logic)
    if "Parent" in frappe.get_roles(user):
        # Example: match by contact number or name
        return True  # keep simple for project

    # Teacher can read
    if "Teacher" in frappe.get_roles(user):
        return True

    return False