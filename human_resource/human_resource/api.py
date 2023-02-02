from __future__ import unicode_literals

import frappe


@frappe.whitelist()
def get_all_employee_info(first_name = None):
    all_employee =[]
    if first_name:
        all_employee = frappe.db.sql(""" select * from `tabEmployee` where first_name like %s""",(first_name), as_dict=1)
    return all_employee