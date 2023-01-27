import frappe

def get_context(context):
    context["leave_applications"] = get_leave_apleacations()


def get_leave_apleacations():
    leave_doc = frappe.db.sql(""" select employee_name, leave_type, total_leave_days from 'tabLeave Application' """, as_dict=1)
    return leave_doc